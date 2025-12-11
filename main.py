import sys
from calculator import StudyStatsCalculator
from report import ReportGenerator
from input_helpers import (
    prompt_int,
    prompt_float,
    prompt_choice,
    prompt_yes_no,
    print_header,
)


APP_TITLE = "StudyStats"


def analyze_single_session(calculator: StudyStatsCalculator) -> None:
    """Interactively collect data for a single study session and display stats."""

    print_header("Single Study Session Analysis")

    minutes = prompt_int("Minutes studied in this session", min_value=1)
    pages = prompt_int("Pages read (0 if none)", min_value=0)
    topics = prompt_int("Number of distinct topics (0 if not applicable)", min_value=0)

    focus_scale = prompt_int(
        "Self‑rated focus (1‑10)",
        min_value=1,
        max_value=10,
    )

    breaks = prompt_int("Number of breaks taken", min_value=0)
    break_minutes = 0
    if breaks > 0:
        break_minutes = prompt_int("Total minutes spent on breaks", min_value=0)

    effective_minutes = calculator.effective_study_time(minutes, break_minutes)
    pages_per_hour = calculator.pages_per_hour(pages, minutes)
    focus_score = calculator.focus_score(focus_scale, breaks)

    print("\n--- Session Stats ---")
    print(f"Total time:       {minutes} minutes")
    print(f"Break time:       {break_minutes} minutes")
    print(f"Effective time:   {effective_minutes:.1f} minutes")
    print(f"Pages read:       {pages}")
    print(f"Pages per hour:   {pages_per_hour:.2f}")
    print(f"Focus score:      {focus_score:.2f} / 10")
    print("--------------------\n")


def analyze_multiple_sessions(calculator: StudyStatsCalculator) -> None:
    """Collect and analyze stats across multiple study sessions."""

    print_header("Multi‑Session Study Analysis")

    n_sessions = prompt_int("How many sessions do you want to enter?", min_value=1)

    durations = []
    pages_list = []
    focus_list = []

    for i in range(1, n_sessions + 1):
        print_header(f"Session {i}/{n_sessions}")
        minutes = prompt_int("Minutes studied in this session", min_value=1)
        pages = prompt_int("Pages read (0 if none)", min_value=0)
        focus_scale = prompt_int(
            "Self‑rated focus (1‑10)",
            min_value=1,
            max_value=10,
        )

        durations.append(float(minutes))
        pages_list.append(float(pages))
        focus_list.append(float(focus_scale))

    avg_duration = calculator.mean(durations)
    median_duration = calculator.median(durations)
    total_minutes = sum(durations)
    total_hours = total_minutes / 60.0

    total_pages = sum(pages_list)
    avg_pages_per_hour = calculator.pages_per_hour(total_pages, total_minutes)

    avg_focus = calculator.mean(focus_list) if focus_list else 0.0

    print("\n--- Aggregate Stats ---")
    print(f"Sessions:               {n_sessions}")
    print(f"Total time:             {total_minutes:.1f} minutes ({total_hours:.2f} h)")
    print(f"Average session length: {avg_duration:.1f} minutes")
    print(f"Median session length:  {median_duration:.1f} minutes")
    print(f"Total pages:            {int(total_pages)}")
    print(f"Pages per hour:         {avg_pages_per_hour:.2f}")
    print(f"Average focus rating:   {avg_focus:.2f} / 10")
    print("------------------------\n")


def main() -> None:
    print_header(APP_TITLE)
    calculator = StudyStatsCalculator()

    while True:
        choice = prompt_choice(
            "What would you like to do?",
            options={
                "1": "Analyze a single study session",
                "2": "Analyze multiple sessions",
                "q": "Quit",
            },
        )

        if choice == "1":
            analyze_single_session(calculator)
        elif choice == "2":
            analyze_multiple_sessions(calculator)
        elif choice == "q":
            if prompt_yes_no("Are you sure you want to quit?"):
                print("Goodbye.")
                break
        else:
            print("Unknown choice. Please try again.\n")


if __name__ == "__main__":  # pragma: no cover
    try:
        main()
    except KeyboardInterrupt:
        print("\nInterrupted by user.")
        sys.exit(1)
