# tests/test_model.py

import pytest
from model import Habit, HabitManager
from database import create_table, add_predefined_habits, load_habits, save_habit
import os
import sqlite3

@pytest.fixture
def test_db(tmp_path):
    """
    Fixture for setting up and tearing down a temporary test database.
    """
    db_path = tmp_path / 'test_model.db'
    db_path = str(db_path)

    create_table(db_path)
    add_predefined_habits(db_path)
    
    yield db_path  



class TestModel:
    """
    Tests various functions of model.py
    1. load_habits
    2. predefined_habits
    3. habit_completion
    4. longest_streak
    5. mark_habit_completed_duplicate
    6. create_habit
    7. delete_habit
    8. get_status_text

    """

    def test_load_habits(self, test_db):
        """Tests loading habits from the database."""
        habits = load_habits(test_db)
        assert len(habits) == 5 

    def test_predefined_habits(self, test_db):
        """Checks if predefined habits are present."""
        habits = load_habits(test_db)
        habit_names = [habit.name for habit in habits]
        assert "Read a book" in habit_names
        assert "Grocery shopping" in habit_names
        assert "Exercise" in habit_names
        assert "House cleaning" in habit_names
        assert "Brush teeth" in habit_names

    def test_habit_completion(self, test_db):
        """Tests completing a habit."""
        habits = load_habits(test_db)
        habit = next((h for h in habits if h.name == "Read a book"), None)
        assert habit is not None
        initial_completions = len(habit.completed_dates)
        
        # Mark task as completed
        HabitManager.mark_habit_completed("Read a book", "2024-10-11", db_path=test_db)
        
        # Check if the change was saved
        habits = load_habits(test_db)
        habit = next((h for h in habits if h.name == "Read a book"), None)
        assert "2024-10-11" in habit.completed_dates

    def test_longest_streak(self, test_db):
        """Tests the longest streak of a habit."""
        habits = load_habits(test_db)
        habit = next((h for h in habits if h.name == "Exercise"), None)
        assert habit is not None
        assert habit.longest_streak == 20  # Based on predefined data

    def test_mark_habit_completed_duplicate(self, test_db):
        """Tests marking a habit as completed on the same day."""
        habits = load_habits(test_db)
        habit = next((h for h in habits if h.name == "Read a book"), None)
        assert habit is not None
        
        # Attempt to complete the same task again
        HabitManager.mark_habit_completed("Read a book", "2024-10-11", db_path=test_db)
        HabitManager.mark_habit_completed("Read a book", "2024-10-11", db_path=test_db)
        
        # Check if the change was saved
        habits = load_habits(test_db)
        habit = next((h for h in habits if h.name == "Read a book"), None)
        assert habit.completed_dates.count("2024-10-11") == 1 

    def test_create_habit(self, test_db):
        """Tests creating a habit"""
        HabitManager.create_habit(
            name="clean bathroom", 
            periodicity="weekly", 
            goal_streak=8,
            target_per_week=1,
            db_path=test_db
        )
        habits = load_habits(test_db)
        habit_names = [habit.name for habit in habits]
        assert "clean bathroom" in habit_names

    def test_delete_habit(self, test_db):
        """Tests deleting the previous created habit"""
        HabitManager.delete_habit(name="clean bathroom", db_path=test_db)
        habits = load_habits(test_db)
        habit_names = [habit.name for habit in habits]
        assert "clean bathroom" not in habit_names

    def test_get_status_text(self, test_db):
        """Tests if status texts are dislpayed correctly"""
        habits = load_habits(test_db)
        test_habit = next((habit for habit in habits if habit.name == "Exercise"), None)
        assert test_habit is not None, "Habit 'Exercise' not found in test_db"
        test_habit_status = test_habit.status
        status_text = HabitManager.get_status_text(test_habit_status)
        assert status_text == "Green (On Track)"
