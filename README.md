# Habit Tracking App

## What is it?

The Habit Tracking App is a Python-based backend application designed to help users create, manage, and analyze their daily and weekly habits. Whether you're aiming to build new positive routines or break old ones, this app provides the essential functionality to track your progress and maintain consistency.

## Features

- Create Multiple Habits: Define and manage multiple habits with specific tasks and periodicities (daily or weekly).
- Mark Tasks as Completed: Easily check off tasks as you complete them.
- Streak Tracking: Monitor consecutive periods of habit completion to maintain and build streaks.
- Analytics Module: Analyze your habits to gain insights, such as your longest streak or habits you struggled with.
- Data Persistence: All habit data is stored persistently using SQLite, ensuring your progress is saved between sessions.
- Predefined Habits: Start with 5 predefined habits, each with 4 weeks of example tracking data.
- Command Line Interface (CLI): Interact with the app through an intuitive CLI for creating, deleting, and analyzing habits.
- Unit Testing: Comprehensive test suite using pytest to ensure reliability and correctness of the application.

## Installation

### Prerequisites

- Python 3.7 or later: Ensure you have Python installed. You can download it from Python's official website.

### Steps

1. Close the repository

```shell
git clone https://github.com/josh-msn/habit_tracking_app.git
```

2. Navigate to the Project Directory

```shell
cd habit-tracking-app
```

3. Create a virtual environment (optional)

```shell
python -m venv venv
```

4. Activate the virtual environment

- Windows:

```shell
venv\Scripts\activate
```

- macOS/Linux:

```shell
source venv/bin/activate
```

5. Install dependencies

```shell
pip install -r requirements.txt
```

## How to use it?

### Running the application

1. Navigate to the project directory

```shell
cd path/to/habit-tracking-app
```

2. Run the application

```shell
python main.py
```

### Creating, managing and analyzing habits

Just follow the instructions on the screen. Everything is described clearly.

### Using predefined habits

At the beginning the database is empty. You can create sample data by selecting "Option 9" from the main menu.

### Delete all habits

To delete all habits at the same time and start from sratch you have to delete the "main.db" file.

## Testing

1. Navigate to the project directory (as described above)
2. Acitvate virtual environment (as described above)
3. Run pytest

```shell
   pytest .
```

## Contact

For any questions, feedback or suggestions, please reach out on GitHub
