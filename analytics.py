# analytics.py

from typing import Dict, List, Optional
from model import Habit
from database import load_habits, DEFAULT_DATABASE

class Analytics:
    """
    Responsible for handling data for analytic purposes including:
    1. get_habits_status_overview -> Returns a dictionary with status as keys and lists of habit names as values.
    2. get_habit_with_longest_streak -> Returns the habit with the longest streak.
    3. get_longest_streak_for_habit -> Returns the longest streak for a specific habit.
    """
    
    def get_habits_status_overview(db_path: str = DEFAULT_DATABASE) -> Dict[str, List[str]]:
        """
        Returns a dictionary with status as keys and lists of habit names as values.
        """
        status_overview = {
            "[bold green]Green[/bold green]": [],
            "[bold yellow]Yellow[/bold yellow]": [],
            "[bold red]Red[/bold red]": []
        }
        habits = load_habits(db_path=db_path)
        for habit in habits:
            if habit.status == 1:
                status_overview["[bold green]Green[/bold green]"].append(habit.name)
            elif habit.status == 2:
                status_overview["[bold yellow]Yellow[/bold yellow]"].append(habit.name)
            elif habit.status == 3:
                status_overview["[bold red]Red[/bold red]"].append(habit.name)
            else:
                status_overview.setdefault("Unknown Status", []).append(habit.name)
        return status_overview

    def get_habit_with_longest_streak(db_path: str = DEFAULT_DATABASE) -> Optional[Habit]:
        """
        Returns the habit with the longest streak.
        """
        habits = load_habits(db_path=db_path)
        if not habits:
            return None
        max_habit = max(habits, key=lambda habit: habit.longest_streak)
        return max_habit

    def get_longest_streak_for_habit(habit_name: str, db_path: str = DEFAULT_DATABASE) -> Optional[int]:
        """
        Returns the longest streak for a specific habit.
        """
        habits = load_habits(db_path=db_path)
        for habit in habits:
            if habit.name.lower() == habit_name.lower():
                return habit.longest_streak
        return None
