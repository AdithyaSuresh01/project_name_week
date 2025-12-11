from __future__ import annotations

"""API playground module.

This module provides a small wrapper around :mod:`requests` to make it
simple to experiment with HTTP APIs. It focuses on clarity and
predictable behavior rather than feature completeness.
"""

from dataclasses import dataclass, field
from typing import Any, Dict, Mapping, Optional

import requests
from requests import Response

from .utils.logger import get_logger


logger = get_logger(__name__)


class ApiPlaygroundError(Exception):
    """Base exception for ApiPlayground-related errors."""


class HttpRequestError(ApiPlaygroundError):
    """Raised when an HTTP request fails or returns a bad status code."""

    def __init__(self, message: str, response: Optional[Response] = None) -> None:
        super().__init__(message)
        self.response = response


@dataclass
class ApiPlayground:
    """Simple HTTP API client.

    Parameters
    ----------
    base_url:
        The base URL for the API, e.g. ``"https://api.github.com"``.
        Trailing slashes are stripped.
    default_timeout:
        Timeout (in seconds) applied to all requests unless overridden.
    default_headers:
        Mapping of headers to send with every request. Per-request headers
        are merged on top of these.
    session:
        Optional preconfigured :class:`requests.Session` instance.
    """

    base_url: str
    default_timeout: int = 10
    default_headers: Mapping[str, str] = field(default_factory=dict)
    session: Optional[requests.Session] = None

    def __post_init__(self) -> None:
        # Normalize base_url (no trailing slash)
        self.base_url = self.base_url.rstrip("/")
        if self.session is None:
            self.session = requests.Session()
        logger.debug(
            "Initialized ApiPlayground",
            extra={
                "base_url": self.base_url,
                "default_timeout": self.default_timeout,
            },
        )

    # ------------------------------------------------------------------
    # Public HTTP methods
    # ------------------------------------------------------------------
    def get(
        self,
        path: str,
        params: Optional[Mapping[str, Any]] = None,
        headers: Optional[Mapping[str, str]] = None,
        timeout: Optional[int] = None,
    ) -> Any:
        """Perform a GET request and return decoded JSON or text.

        Parameters
        ----------
        path:
            API path appended to ``base_url``. May start with ``"/"``.
        params:
            Query parameters to send with the request.
        headers:
            Per-request headers (merged over ``default_headers``).
        timeout:
            Overrides ``default_timeout`` if provided.
        """

        return self._request(
            method="GET",
            path=path,
            params=params,
            headers=headers,
            timeout=timeout,
        )

    def post(
        self,
        path: str,
        json: Optional[Any] = None,
        data: Optional[Mapping[str, Any]] = None,
        headers: Optional[Mapping[str, str]] = None,
        timeout: Optional[int] = None,
    ) -> Any:
        """Perform a POST request and return decoded JSON or text."""

        return self._request(
            method="POST",
            path=path,
            json=json,
            data=data,
            headers=headers,
            timeout=timeout,
        )

    def _request(
        self,
        method: str,
        path: str,
        params: Optional[Mapping[str, Any]] = None,
        json: Optional[Any] = None,
        data: Optional[Mapping[str, Any]] = None,
        headers: Optional[Mapping[str, str]] = None,
        timeout: Optional[int] = None,
    ) -> Any:
        """Internal helper to perform an HTTP request.

        Raises
        ------
        HttpRequestError
            If the request fails at the network level or returns a
            non-success HTTP status code.
        """

        if not self.session:
            # Very defensive; should not normally happen.
            self.session = requests.Session()

        url = self._build_url(path)
        timeout_value = timeout if timeout is not None else self.default_timeout

        request_headers: Dict[str, str] = dict(self.default_headers)
        if headers:
            request_headers.update(headers)

        logger.info("Performing HTTP request", extra={"method": method, "url": url})

        try:
            response = self.session.request(
                method=method,
                url=url,
                params=params,
                json=json,
                data=data,
                headers=request_headers,
                timeout=timeout_value,
            )
        except requests.RequestException as exc:  # network/connection errors
            logger.error(
                "HTTP request failed at network level",
                extra={"method": method, "url": url, "error": str(exc)},
            )
            raise HttpRequestError(f"Network-level error during request: {exc}") from exc

        if not response.ok:
            logger.warning(
                "Received non-success status code",
                extra={"status_code": response.status_code, "url": url},
            )
            message = (
                f"Request to {url} failed with status "
                f"{response.status_code}: {response.text[:200]}"
            )
            raise HttpRequestError(message, response=response)

        return self._decode_response(response)

    # ------------------------------------------------------------------
    # Helpers
    # ------------------------------------------------------------------
    def _build_url(self, path: str) -> str:
        """Build a full URL from ``base_url`` and a relative path."""

        if not path:
            return self.base_url
        if not path.startswith("/"):
            path = "/" + path
        return f"{self.base_url}{path}"

    @staticmethod
    def _decode_response(response: Response) -> Any:
        """Decode an HTTP response.

        Attempts to parse JSON; if this fails, returns ``response.text``.
        """

        content_type = response.headers.get("Content-Type", "").lower()

        if "application/json" in content_type or "+json" in content_type:
            try:
                return response.json()
            except ValueError:
                logger.debug("Response declared JSON but failed to parse; falling back to text")
                return response.text

        # Fallback for other content types
        return response.text
