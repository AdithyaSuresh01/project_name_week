from __future__ import annotations

from dataclasses import dataclass
from typing import Iterable, List


@dataclass
class StudyStatsCalculator:
    """Core calculation utilities for StudyStats.

    This class focuses on pure, testable computations and does not
    perform any input/output. All methods are deterministic and side‑effect free.
    """

    def effective_study_time(self, total_minutes: float, break_minutes: float) -> float:
        """Return effective study time in minutes after subtracting breaks.

        Args:
            total_minutes: Total minutes allocated for the session.
            break_minutes: Minutes spent on breaks.

        Returns:
            Effective study minutes (never negative).
        """
        total = max(float(total_minutes), 0.0)
        brk = max(float(break_minutes), 0.0)
        return max(total - brk, 0.0)

    def pages_per_hour(self, pages: float, minutes: float) -> float:
        """Compute reading speed as pages per hour.

        Returns 0.0 when minutes is not positive.
        """
        mins = float(minutes)
        if mins <= 0:
            return 0.0
        return float(pages) / (mins / 60.0)

    def focus_score(self, focus_rating: float, breaks: int) -> float:
        """Compute an adjusted focus score on a 0‑10 scale.

        The score is derived from the self‑reported focus rating (1‑10)
        and penalized slightly for additional breaks beyond the first.
        This is a simple heuristic for demonstration purposes.
        """
        base = max(min(float(focus_rating), 10.0), 0.0)
        extra_breaks = max(int(breaks) - 1, 0)
        penalty = 0.3 * extra_breaks
        return max(base - penalty, 0.0)

    # --------- Basic descriptive statistics ---------

    def mean(self, values: Iterable[float]) -> float:
        """Return the arithmetic mean of *values*.

        Returns 0.0 when the iterable is empty.
        """
        vals: List[float] = [float(v) for v in values]
        if not vals:
            return 0.0
        return sum(vals) / len(vals)

    def median(self, values: Iterable[float]) -> float:
        """Return the median of *values*.

        For an even number of items, the average of the two middle
        values is returned. Returns 0.0 when the iterable is empty.
        """
        vals: List[float] = sorted(float(v) for v in values)
        n = len(vals)
        if n == 0:
            return 0.0
        mid = n // 2
        if n % 2 == 1:
            return vals[mid]
        return (vals[mid - 1] + vals[mid]) / 2.0
