# main.py

from rich.console import Console
from rich.table import Table
import questionary
from model import HabitManager
from analytics import Analytics
import database
from datetime import datetime

console = Console()

def display_habits(habits: list):
    """
    Displays all habits in a table with the following columns: 
    Name, Periodicity, Creation date, Last completed, Goal streak, Longest streak, Status, Target per week
    """
    if not habits:
        console.print("No habits found.", style="bold red")
    else:
        # Create a new table with Rich
        table = Table(title="All Habits", show_lines=True)
        table.add_column("Name", style="cyan", no_wrap=True)
        table.add_column("Periodicity", style="magenta")
        table.add_column("Creation date", style="green")
        table.add_column("Last completed", style="yellow")  # New Column
        table.add_column("Goal streak", style="blue", justify="right")
        table.add_column("Longest streak", style="blue", justify="right")  # New Column
        table.add_column("Status", style="bold")
        table.add_column("Target per week", style="dim", justify="right")


        for habit in habits:
            status_color = {
                1: "[bold green]Green[/bold green]",
                2: "[bold yellow]Yellow[/bold yellow]",
                3: "[bold red]Red[/bold red]"
            }.get(habit.status, "Unknown")
            
            # Find last completion date. 
            if habit.completed_dates:
                dates = [datetime.strptime(d, '%Y-%m-%d') for d in habit.completed_dates] # Convert completion dates to datetime objects
                last_completed = max(dates).strftime('%Y-%m-%d')   # Find the most recent date
            else:
                last_completed = "None"

            longest_streak = habit.longest_streak  

            target_per_week = habit.target_per_week if habit.periodicity.lower() == 'weekly' else "-"

            # Add a new row to the table
            table.add_row(
                habit.name,
                habit.periodicity.capitalize(),
                habit.creation_date,
                last_completed,         
                str(habit.goal_streak),
                str(longest_streak),    
                status_color,
                str(target_per_week)
            )
        
        console.print(table)

def display_status_overview():
    """
    Displays a status (green, yellow, red) overview of habits. Habits are grouped by status.
    """
    overview = Analytics.get_habits_status_overview()
    if not overview:
        console.print("No habits found.", style="bold red")
    else:
        table = Table(title="Habits Status Overview", show_lines=True)
        table.add_column("Status", style="bold")
        table.add_column("Habits", style="cyan")

        for status_color, habits in overview.items():
            habits_list = ", ".join(habits) if habits else "None"
            table.add_row(status_color, habits_list)
        
        console.print(table)

def main():
    """
    Main menu for the habit tracker. Navigation is guided with questionary. The user is able to abort every step.
    The menu has 10 predefined options. Some options are multi steps like creating a new habit.
                "1. List All Habits",
                "2. List Habits by Periodicity",
                "3. Mark Habit as Completed",
                "4. Find Habit with Longest Streak",
                "5. Find Longest Streak for a Specific Habit",
                "6. Show Habits Status Overview",
                "7. Create New Habit",
                "8. Delete Habit",
                "9. Add Predefined Habits",
                "10. Exit"
    """
    database.create_table()
    
    while True:
        choice = questionary.select(
            "=== Habit Tracker ===",
            choices=[
                "1. List All Habits",
                "2. List Habits by Periodicity",
                "3. Mark Habit as Completed",
                "4. Find Habit with Longest Streak",
                "5. Find Longest Streak for a Specific Habit",
                "6. Show Habits Status Overview",
                "7. Create New Habit",
                "8. Delete Habit",
                "9. Add Predefined Habits",
                "10. Exit"
            ]
        ).ask()

        if choice is None:
            console.print("No selection made. Exiting...", style="bold yellow")
            break

        try:
            # 1. List all habits
            if choice == "1. List All Habits":
                habits = HabitManager.get_all_habits()
                display_habits(habits)

             # 2. List habits by periodicity
            elif choice == "2. List Habits by Periodicity":
                periodicity = questionary.select(
                    "Select periodicity to filter by:",
                    choices=["daily", "weekly", "Cancel"]
                ).ask()
                if periodicity == "Cancel":
                    console.print("Operation cancelled.", style="bold yellow")
                    continue
                habits = HabitManager.get_habits_by_periodicity(periodicity)
                display_habits(habits)

            # 3. Mark habit as completed
            elif choice == "3. Mark Habit as Completed":
                habits = HabitManager.get_all_habits()
                if not habits:
                    console.print("No habits available to mark as completed.", style="bold yellow")
                    continue
                habit_names = [habit.name for habit in habits]
                habit_names.append("Cancel")
                selected_habit = questionary.select(
                    "Select the habit to mark as completed:",
                    choices=habit_names
                ).ask()
                if selected_habit == "Cancel":
                    console.print("Operation cancelled.", style="bold yellow")
                    continue
                HabitManager.mark_habit_completed(selected_habit)

            # 4. Find habit with longest streak
            elif choice == "4. Find Habit with Longest Streak":
                habit = Analytics.get_habit_with_longest_streak()
                if habit:
                    console.print(f"\nHabit with the longest streak: [bold green]{habit.name}[/bold green] with a streak of [bold blue]{habit.longest_streak}[/bold blue] days/weeks.\n")
                else:
                    console.print("No habits found.", style="bold red")

            # 5. Find Longest Streak for a Specific Habit
            elif choice == "5. Find Longest Streak for a Specific Habit":
                habits = HabitManager.get_all_habits()
                if not habits:
                    console.print("No habits available.", style="bold yellow")
                    continue
                habit_names = [habit.name for habit in habits]
                habit_names.append("Cancel")
                selected_habit = questionary.select(
                    "Select the habit to find its longest streak:",
                    choices=habit_names
                ).ask()
                if selected_habit == "Cancel":
                    console.print("Operation cancelled.", style="bold yellow")
                    continue
                longest_streak = Analytics.get_longest_streak_for_habit(selected_habit)
                if longest_streak is not None:
                    console.print(f"\nThe longest streak for habit '{selected_habit}' is [bold blue]{longest_streak}[/bold blue] days/weeks.\n")
                else:
                    console.print(f"Habit '{selected_habit}' not found.", style="bold red")

            # 6. Show habits status overview
            elif choice == "6. Show Habits Status Overview":
                display_status_overview()

            # 7. Create new habit
            elif choice == "7. Create New Habit":
                try:
                    name = questionary.text(
                        "Enter the name of the habit (or type 'Cancel' to abort):"
                    ).ask()
                    if name is None or name.strip().lower() == 'cancel':
                        console.print("Operation cancelled.", style="bold yellow")
                        continue

                    periodicity = questionary.select(
                        "Select periodicity:",
                        choices=["daily", "weekly", "Cancel"]
                    ).ask()
                    if periodicity == "Cancel":
                        console.print("Operation cancelled.", style="bold yellow")
                        continue

                    goal_streak = questionary.text(
                        "Enter goal streak (number of consecutive days/weeks):",
                        validate=lambda val: val.isdigit() or "Please enter a valid number."
                    ).ask()
                    if goal_streak is None or goal_streak.strip() == '':
                        console.print("Operation cancelled.", style="bold yellow")
                        continue
                    goal_streak = int(goal_streak)

                    target_per_week = 0
                    if periodicity.lower() == 'weekly':
                        target_per_week_input = questionary.text(
                            "How many times per week do you want to complete this habit? (or type 'Cancel' to abort):",
                            validate=lambda val: val.isdigit() or "Please enter a valid number."
                        ).ask()
                        if target_per_week_input is None or target_per_week_input.strip().lower() == 'cancel':
                            console.print("Operation cancelled.", style="bold yellow")
                            continue
                        target_per_week = int(target_per_week_input)

                    HabitManager.create_habit(name, periodicity, goal_streak, target_per_week)
                except KeyboardInterrupt:
                    console.print("\nOperation aborted by user.", style="bold yellow")

            # 8. Delete habit
            elif choice == "8. Delete Habit":
                try:
                    habits = HabitManager.get_all_habits()
                    if not habits:
                        console.print("No habits available to delete.", style="bold yellow")
                        continue
                    habit_names = [habit.name for habit in habits]
                    habit_names.append("Cancel")
                    selected_habit = questionary.select(
                        "Select the habit to delete:",
                        choices=habit_names
                    ).ask()
                    if selected_habit == "Cancel":
                        console.print("Operation cancelled.", style="bold yellow")
                        continue
                    HabitManager.delete_habit(selected_habit)
                except KeyboardInterrupt:
                    console.print("\nOperation aborted by user.", style="bold yellow")

            # 9. Add predefined habits
            elif choice == "9. Add Predefined Habits":
                confirm = questionary.confirm(
                    "Are you sure you want to add predefined habits? This may create duplicates."
                ).ask()
                if confirm:
                    database.add_predefined_habits()
                else:
                    console.print("Predefined habits were not added.", style="bold yellow")

            # 10. Exit
            elif choice == "10. Exit":
                console.print("Exiting...", style="bold green")
                break

            else:
                console.print("Invalid option. Please choose a valid number.", style="bold red")

        except KeyboardInterrupt:
            console.print("\nOperation aborted by user.", style="bold yellow")
            continue

if __name__ == "__main__":
    main()
