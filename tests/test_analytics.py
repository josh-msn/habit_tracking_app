# tests/test_analytics.py

import pytest
from analytics import Analytics
from database import create_table, add_predefined_habits
import os
import sqlite3

@pytest.fixture
def test_db(tmp_path):
    """
    Fixture for setting up and tearing down a temporary test database.
    """
    db_path = tmp_path / 'test_analytics.db'
    db_path = str(db_path)    

    create_table(db_path)
    add_predefined_habits(db_path)
    
    yield db_path  


class TestAnalytics:
    """
    Tests all methods of analytics.py
    1. get_habits_status_overview
    2. get_habit_with_longest_streak
    3. get_longest_streak_for_habit
    """

    def test_get_habits_status_overview(self, test_db):
        """Tests the method get_habits_status_overview."""

        status_overview = Analytics.get_habits_status_overview(db_path=test_db)
        assert isinstance(status_overview, dict)

        green_habits = status_overview["[bold green]Green[/bold green]"]
        assert len(green_habits) == 5  
        assert len(status_overview["[bold yellow]Yellow[/bold yellow]"]) == 0
        assert len(status_overview["[bold red]Red[/bold red]"]) == 0

    def test_get_habit_with_longest_streak(self, test_db):
        """Tests the method get_habit_with_longest_streak."""
        habit = Analytics.get_habit_with_longest_streak(db_path=test_db)
        assert habit is not None
        assert habit.name == "Exercise"
        assert habit.longest_streak == 20

    def test_get_longest_streak_for_habit(self, test_db):
        """Tests the method get_longest_streak_for_habit."""
        longest_streak = Analytics.get_longest_streak_for_habit("Read a book", db_path=test_db)
        assert longest_streak is not None
        assert longest_streak == 10
