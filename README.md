# Task Manager Organizator

## Overview

This project is a terminal-based task manager application written in Python using the `curses` library. It allows users to manage tasks through a text-based user interface.

## Features

- **Display Tasks**: View all tasks, categorized by their completion status.
- **Add Task**: Add new tasks with descriptions.
- **Toggle Task Status**: Mark tasks as done or undone.
- **Delete Task**: Remove tasks from the list.
- **Save and Quit**: Save the current state of tasks to a JSON file and exit the application.

## File Structure

- **src/task-manager-script.py**: Main script containing the task manager logic.
- **tasks.json**: JSON file where tasks are saved.
- **tasks.txt**: Text file for additional task-related data (if needed).

## Key Functions

- `main`: Entry point of the application.
- `load_tasks`: Load tasks from `tasks.json`.
- `save_tasks`: Save tasks to `tasks.json`.
- `display_menu`: Display the main menu.
- `display_tasks`: Display tasks categorized by their status.
- `add_task`: Add a new task.
- `toggle_task`: Toggle the completion status of a task.
- `delete_task`: Delete a task.
- `quit_message`: Display a goodbye message and quit the application.

## Usage

1. **Run the script**:
    ```sh
    python src/task-manager-script.py
    ```
2. **Navigate the menu** using the arrow keys and select options with the Enter key.
3. **Press 'q'** to save tasks and quit the application.

## Dependencies
1. Python 3.x
2. **curses** library (included in the Python standard library)

## Conclusion
This task manager script provides a simple yet effective way to manage tasks directly from the terminal. It is a great example of using the curses library to create text-based user interfaces in Python.