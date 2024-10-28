# model.py

from typing import List
from datetime import date, datetime, timedelta


# Status Constants
GREEN = 1    # Everything is on track
YELLOW = 2   # One missed track
RED = 3      # More than three missed tracks


class Habit:
    """
    The Habit class contains all methods regarding the habit itself.
    1. __init__  -> Initialising the habit
    2. complete_task -> adds a completion date when marked as complete
    3. get_total_completion -> calculates the total amount of completions
    4. update_longest_streak -> Calculates and updates the longest streak.
    5. get_streak -> Calculates the current streak based on completion dates.
    6. was_completed_on -> Checks if the habit was completed on a specific date.
    """
    def __init__(self, name: str, periodicity: str, creation_date: str = None, 
                 completed_dates: List[str] = None, goal_streak: int = 0, 
                 status: int = GREEN, position: int = 0, longest_streak: int = 0, target_per_week: int = 0):
        self.name = name
        self.periodicity = periodicity  # 'daily' or 'weekly'
        self.creation_date = creation_date if creation_date else str(date.today())
        self.completed_dates = completed_dates if completed_dates else [] #all completed dates
        self.goal_streak = goal_streak #how often the habit needs to be marked as done
        self.status = status  # 1=GREEN, 2=YELLOW, 3=RED
        self.position = position
        self.longest_streak = longest_streak  # Longest streak in habit history
        self.target_per_week = target_per_week  
    def complete_task(self, completion_date: str = None):
        """
        Adds a completion date if it doesn't already exist. 
        """
        if not completion_date:
            completion_date = str(date.today())
        if completion_date not in self.completed_dates:
            self.completed_dates.append(completion_date)
            print(f"Task completed on {completion_date}.")
            self.update_longest_streak()
        else:
            print(f"Task on {completion_date} has already been completed.")

    def get_total_completions(self) -> int:
        """Returns the total number of completions."""
        return len(self.completed_dates)
    
    def update_longest_streak(self):
        """
        Calculates and updates the longest streak if the the current streak is the longest. 
        Otherwise it stays the same.
        """
        if not self.completed_dates:
            self.longest_streak = 0
            return

        # Convert completion dates to datetime objects and sort them
        dates = sorted([datetime.strptime(d, '%Y-%m-%d') for d in self.completed_dates])
        current_streak = 1
        max_streak = 1

        for i in range(1, len(dates)):
            delta = dates[i] - dates[i-1]
            if self.periodicity.lower() == 'daily':
                expected_delta = timedelta(days=1)
            elif self.periodicity.lower() == 'weekly':
                expected_delta = timedelta(weeks=1)
            else:
                expected_delta = timedelta(0)  

            if delta == expected_delta:
                current_streak += 1
            else:
                current_streak = 1  

            if current_streak > max_streak:
                max_streak = current_streak

        self.longest_streak = max_streak

    def get_streak(self) -> int:
        """
        Calculates the current streak based on completion dates.
        """
        if not self.completed_dates:
            return 0

        # Convert completion dates to datetime objects and sort them in descending order
        dates = sorted([datetime.strptime(d, '%Y-%m-%d') for d in self.completed_dates], reverse=True)
        streak = 0
        today = date.today()

        for d in dates:
            if self.periodicity.lower() == 'daily':
                expected_date = today - timedelta(days=streak)
                if d.date() == expected_date:
                    streak += 1
                else:
                    break
            elif self.periodicity.lower() == 'weekly':
                expected_date = today - timedelta(weeks=streak)
                # Adjust expected_date to the start of the week (Monday)
                expected_date = expected_date - timedelta(days=expected_date.weekday())
                if d.date() == expected_date:
                    streak += 1
                else:
                    break
            else:
                break  
        return streak

    def was_completed_on(self, check_date: str) -> bool:
        """Checks if the habit was completed on a specific date."""
        return check_date in self.completed_dates

##############################################################################

from database import load_habits, save_habit, get_connection, DEFAULT_DATABASE
import sqlite3 

# In model.py

class HabitManager:
    """Manages habits including:
    1. create_habit -> Creates and saves a new habit.
    2. delete_habit -> Deletes a habit by its name.
    3. get_all_habits -> Returns a list of all habits.
    4. get_habits_by_periodicity -> Returns a list of habits with a specific periodicity.
    5. mark_habit_completed -> Marks a habit as completed by adding a completion date.
    6. get_status_text -> Returns the text representation of a given status.
    """

    def create_habit(name: str, periodicity: str, goal_streak: int, target_per_week: int = 0, db_path: str = DEFAULT_DATABASE):
        """Creates and saves a new habit."""
        habit = Habit(name=name, periodicity=periodicity, goal_streak=goal_streak, target_per_week=target_per_week)
        save_habit(habit, db_path)

    def delete_habit(name: str, db_path: str = DEFAULT_DATABASE):
        """Deletes a habit by its name."""
        habits = load_habits(db_path)
        habit_to_delete = None
        for habit in habits:
            if habit.name.lower() == name.lower():
                habit_to_delete = habit
                break
        if habit_to_delete:
            try:
                with get_connection(db_path) as conn:
                    c = conn.cursor()
                    c.execute('DELETE FROM habits WHERE name = ?', (name,))
                    conn.commit()
                print(f"Habit '{name}' successfully deleted from {db_path}.")
            except sqlite3.Error as e:
                print(f"An error occurred in {db_path}: {e}")
        else:
            print(f"Habit '{name}' not found in {db_path}.")


    def get_all_habits(db_path: str = DEFAULT_DATABASE) -> List[Habit]:
        """Returns a list of all habits."""
        return load_habits(db_path)


    def get_habits_by_periodicity(periodicity: str, db_path: str = DEFAULT_DATABASE) -> List[Habit]:
        """Returns a list of habits with a specific periodicity."""
        all_habits = load_habits(db_path)
        filtered_habits = [habit for habit in all_habits if habit.periodicity.lower() == periodicity.lower()]
        return filtered_habits


    def mark_habit_completed(habit_name: str, completion_date: str = None, db_path: str = DEFAULT_DATABASE):
        """Marks a habit as completed by adding a completion date."""
        habits = load_habits(db_path)
        for habit in habits:
            if habit.name.lower() == habit_name.lower():
                habit.complete_task(completion_date)
                save_habit(habit, db_path)
                print(f"Habit '{habit_name}' marked as completed on {completion_date if completion_date else date.today()} in {db_path}.")
                return
        print(f"Habit '{habit_name}' not found in {db_path}.")


    def get_status_text(status: int) -> str:
        """Returns the text representation of a given status."""
        if status == GREEN:
            return "Green (On Track)"
        elif status == YELLOW:
            return "Yellow (One Missed Track)"
        elif status == RED:
            return "Red (More than Three Missed Tracks)"
        else:
            return "Unknown Status"
