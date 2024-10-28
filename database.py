# database.py
import sqlite3
from typing import List
from datetime import timedelta, datetime
from model import Habit

DEFAULT_DATABASE = 'main.db'

def get_connection(db_path: str = DEFAULT_DATABASE):

    """Establishes a connection to the specified database.
    Also accepts URIs to support in memmory database"""
    if db_path.startswith("file:") and "?mode=memory" in db_path:
        return sqlite3.connect(db_path, uri=True)
    else:
        return sqlite3.connect(db_path)


def create_table(db_path: str = DEFAULT_DATABASE):
    """Creates the 'habits' table if it does not exist."""
    with get_connection(db_path) as conn:
        c = conn.cursor()
        c.execute("""CREATE TABLE IF NOT EXISTS habits(
                  name TEXT UNIQUE,
                  periodicity TEXT,
                  creation_date TEXT,
                  completed_dates TEXT,  
                  goal_streak INTEGER,
                  status INTEGER,
                  position INTEGER,
                  longest_streak INTEGER,
                  target_per_week INTEGER
                  )""")
        conn.commit()
    print(f"Table 'habits' created or already exists in {db_path}.")

def save_habit(habit: Habit, db_path: str = DEFAULT_DATABASE):
    """Saves habit to the specified database."""

    try:
        with get_connection(db_path) as conn:
            c = conn.cursor()
            c.execute('SELECT COUNT(*) FROM habits')
            count = c.fetchone()[0]
            habit.position = count if count else 0
            completed_dates_str = ",".join(habit.completed_dates) if habit.completed_dates else ""
            c.execute('''
                INSERT INTO habits (name, periodicity, creation_date, completed_dates, goal_streak, status, position, longest_streak, target_per_week)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
            ''', (habit.name, 
                  habit.periodicity, 
                  habit.creation_date, 
                  completed_dates_str, 
                  habit.goal_streak, 
                  habit.status, 
                  habit.position,
                  habit.longest_streak,
                  habit.target_per_week))
            conn.commit()
        print(f"Habit '{habit.name}' successfully saved to {db_path}.")
    except sqlite3.IntegrityError:
        print(f"Habit with name '{habit.name}' already exists in {db_path}.")
    except sqlite3.Error as e:
        print(f"An error occurred in {db_path}: {e}")

def load_habits(db_path: str = DEFAULT_DATABASE) -> List[Habit]:
    """Loads all habits from the specified database."""

    habits = []
    try:
        with get_connection(db_path) as conn:
            c = conn.cursor()
            c.execute('SELECT * FROM habits')
            results = c.fetchall()
            for result in results:
                habit = Habit(
                    name=result[0],
                    periodicity=result[1],
                    creation_date=result[2],
                    completed_dates=result[3].split(',') if result[3] else [],
                    goal_streak=result[4],
                    status=result[5],
                    position=result[6],
                    longest_streak=result[7],  
                    target_per_week=result[8] 
                )
                habits.append(habit)
    except sqlite3.Error as e:
        print(f"An error occurred in {db_path}: {e}")
    return habits



def add_predefined_habits(db_path: str = DEFAULT_DATABASE):
    """Adds 5 predefined habits with dummy data from 4 weeks."""

    # Function to generate dummy dates for the last 4 weeks
    def generate_dummy_dates(start_date: datetime, days: int) -> List[str]:
        return [(start_date + timedelta(days=i)).strftime('%Y-%m-%d') for i in range(days)]

    today = datetime.today()
    four_weeks_ago = today - timedelta(weeks=4)

    predefined_habits = [
        {
            "name": "Read a book",
            "periodicity": "daily",
            "goal_streak": 30,
            "status": 1,
            "target_per_week": 0, 
            "longest_streak": 10,
            "completed_dates": generate_dummy_dates(four_weeks_ago, 28)
        },
        {
            "name": "Grocery shopping",
            "periodicity": "weekly",
            "goal_streak": 8,
            "status": 1,
            "target_per_week": 3,  
            "longest_streak": 4,           
            "completed_dates": [
                (four_weeks_ago + timedelta(weeks=i)).strftime('%Y-%m-%d') for i in range(4)
            ]  
        },
        {
            "name": "Exercise",
            "periodicity": "daily",
            "goal_streak": 20,
            "status": 1,
            "target_per_week": 0,
            "longest_streak": 20,            
            "completed_dates": generate_dummy_dates(four_weeks_ago, 20)
        },
        {
            "name": "House cleaning",
            "periodicity": "weekly",
            "goal_streak": 8,
            "status": 1,
            "target_per_week": 2,
            "longest_streak": 3,             
            "completed_dates": [
                (four_weeks_ago + timedelta(weeks=i*1)).strftime('%Y-%m-%d') for i in range(4)
            ] 
        },
        {
            "name": "Brush teeth",
            "periodicity": "daily",
            "goal_streak": 30,
            "status": 1,
            "target_per_week": 0,
            "longest_streak": 14,            
            "completed_dates": generate_dummy_dates(four_weeks_ago, 15)
        }
    ]

    for habit_data in predefined_habits:
        habit = Habit(
            name=habit_data["name"],
            periodicity=habit_data["periodicity"],
            creation_date=habit_data.get("creation_date", four_weeks_ago.strftime('%Y-%m-%d')),
            completed_dates=habit_data["completed_dates"],
            goal_streak=habit_data["goal_streak"],
            status=habit_data["status"],
            position=habit_data.get("position", 0),
            longest_streak=habit_data["longest_streak"],
            target_per_week=habit_data["target_per_week"]
        )
        save_habit(habit, db_path)
    print(f"Predefined habits have been added to {db_path}.")
