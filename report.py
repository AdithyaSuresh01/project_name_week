from __future__ import annotations

from dataclasses import dataclass
from typing import Iterable, List, Dict, Any

from calculator import StudyStatsCalculator


@dataclass
class ReportGenerator:
    """Generate textual reports for StudyStats.

    This class is separate from user interaction so it can be reused in
    other interfaces (e.g., GUI, web, notebooks).
    """

    calculator: StudyStatsCalculator

    # Example of a more structured report API, not used by main.py yet but
    # available for future extensions.

    def summarize_sessions(
        self,
        durations: Iterable[float],
        pages: Iterable[float],
        focus_ratings: Iterable[float],
    ) -> Dict[str, Any]:
        """Return a dictionary with aggregate statistics across sessions."""
        dur_list: List[float] = [float(d) for d in durations]
        pages_list: List[float] = [float(p) for p in pages]
        focus_list: List[float] = [float(f) for f in focus_ratings]

        total_minutes = sum(dur_list)
        total_hours = total_minutes / 60.0
        total_pages = sum(pages_list)

        return {
            "sessions": len(dur_list),
            "total_minutes": total_minutes,
            "total_hours": total_hours,
            "avg_duration": self.calculator.mean(dur_list),
            "median_duration": self.calculator.median(dur_list),
            "total_pages": total_pages,
            "pages_per_hour": self.calculator.pages_per_hour(total_pages, total_minutes),
            "avg_focus": self.calculator.mean(focus_list) if focus_list else 0.0,
        }

    def format_summary(self, summary: Dict[str, Any]) -> str:
        """Format the dictionary from ``summarize_sessions`` into text."""
        lines = [
            "Study Stats Summary",
            "-------------------",
            f"Sessions:               {summary.get('sessions', 0)}",
            f"Total time:             {summary.get('total_minutes', 0.0):.1f} minutes"
            f" ({summary.get('total_hours', 0.0):.2f} h)",
            f"Average session length: {summary.get('avg_duration', 0.0):.1f} minutes",
            f"Median session length:  {summary.get('median_duration', 0.0):.1f} minutes",
            f"Total pages:            {int(summary.get('total_pages', 0))}",
            f"Pages per hour:         {summary.get('pages_per_hour', 0.0):.2f}",
            f"Average focus rating:   {summary.get('avg_focus', 0.0):.2f} / 10",
        ]
        return "\n".join(lines)
