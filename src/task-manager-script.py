import os
import json
from datetime import datetime
import curses
from time import sleep

TASKS_FILE = "tasks.json"

class Task():
    def __init__(self, description, done, cdate, ddate):
        self.description = description
        self.done = done
        self.cdate = cdate
        self.ddate = ddate

    def toogleDone(self):
        self.done = not self.done

def load_tasks():
    if not os.path.exists(TASKS_FILE):
        return []
    with open(TASKS_FILE, "r") as f:
        return json.load(f)

def save_tasks(tasks):
    with open(TASKS_FILE, "w") as f:
        json.dump([task.__dict__ for task in tasks], f, default=str)

def display_menu(stdscr, current_row):
    stdscr.clear()
    menu = ["Display tasks", "Add task", "Toggle task status", "Delete task", "Save and quit"]
    height, width = stdscr.getmaxyx()
    for idx, row in enumerate(menu):
        x = width // 2 - len(row) // 2
        y = height // 2 - len(menu) // 2 + idx
        if idx == current_row:
            stdscr.addstr(y, x, row, curses.color_pair(1))
        else:
            stdscr.addstr(y, x, row)
    
    stdscr.addstr(height - 1, 0, "Press 'q' to quit")
    cdate = datetime.now().strftime("%Y-%m-%d %H:%M")
    stdscr.addstr(height - 1, width - (len(cdate) + 1) , f"{cdate}")
    stdscr.refresh()

def task_lenght(task, mode, idx):
    if mode == 1: 
        return len(f"{idx + 1}. {task.description} - {task.cdate} -> {task.ddate}")
    else: 
        return len(f"{idx + 1}. {task.description} - {task.cdate}")

def display_tasks(stdscr, tasks):
    stdscr.clear()
    height, width = stdscr.getmaxyx()
    done_tasks = [task for task in tasks if task.done == True]
    undone_tasks = [task for task in tasks if not task.done == True]
    if not tasks:
        stdscr.addstr(0, width//2 - len("No tasks created yet.")//2, "No tasks created yet.")
    else:
        stdscr.addstr(height//2 - len(undone_tasks), width//2 - 5, "[ ] tasks:")
        for idx, task in enumerate(undone_tasks):
            stdscr.addstr((height//2 - len(undone_tasks)) + idx + 1, width//2 - task_lenght(task, 1, idx)//2, 
                          f"{idx + 1}. {task.description} - {task.cdate} -> {task.ddate}")
        stdscr.addstr(height//2 + 2, width//2 - 5, "[x] tasks:")
        for idx, task in enumerate(done_tasks):
            stdscr.addstr(height//2 + idx + 3, width//2 - task_lenght(task, 2, idx)//2, 
                          f"{idx + 1}. {task.description} - {task.cdate}")

def display_all_tasks(stdscr, tasks, current_row):
    stdscr.clear()
    height, width = stdscr.getmaxyx()
    message = "No tasks created yet"
    if not tasks:
        stdscr.addstr(height//2 - len(message), width//2 - len(message), message)
    else:
        for idx, task in enumerate(tasks):
            status = "[x]" if task.done else "[ ]"
            height_print= (height//2 - len(tasks)) + idx + 1 
            width_print= width//2 - (len(status) + len(task.description) + 2)//2
            if idx == current_row:
                stdscr.addstr(height_print, width_print, f"{idx + 1}. {status} {task.description}", curses.color_pair(1))
            else:    
                stdscr.addstr(height_print, width_print, f"{idx + 1}. {status} {task.description}")
    stdscr.refresh()

def add_task(stdscr, tasks):
    stdscr.clear()
    stdscr.addstr(0, 0, "Enter task description: ")
    curses.echo()
    description = stdscr.getstr(1, 0).decode('utf-8')
    if description == "-1":
        return
    stdscr.addstr(10, 0, "Enter due date (dd-mm-yyyy): ")
    ddate_str = stdscr.getstr(11, 0).decode('utf-8')
    curses.noecho()
    cdate = datetime.now().strftime("%Y-%m-%d")
    new_task = Task(description, False, 
                    datetime.strptime(cdate, "%Y-%m-%d").date(), 
                    datetime.strptime(ddate_str, "%d-%m-%Y").date())
    tasks.append(new_task)

def toggle_task(stdscr, tasks):
    current_row = 0
    while True:
        display_all_tasks(stdscr, tasks,current_row)
        key = stdscr.getch()
        if(key == ord('j') or key == curses.KEY_DOWN) and current_row < len(tasks):
            current_row += 1
        elif(key == ord('k') or key == curses.KEY_UP) and current_row < len(tasks):
            current_row -= 1 
        elif key == curses.KEY_ENTER or key in [10,13]:
            if 0 <= current_row < len(tasks):
                tasks[current_row].toogleDone()
        elif key == ord('q'): 
            break

def delete_task(stdscr, tasks):
    current_row = 0
    while True:
        display_all_tasks(stdscr, tasks,current_row)
        key = stdscr.getch()
        if(key == ord('j') or key == curses.KEY_DOWN) and current_row < len(tasks):
            current_row += 1
        elif(key == ord('k') or key == curses.KEY_UP) and current_row < len(tasks):
            current_row -= 1 
        elif key == curses.KEY_ENTER or key in [10,13]:
            if 0 <= current_row < len(tasks):
                tasks.pop(current_row) 
        elif key == ord('q'): 
            break
                

def splash_screen(stdscr):
    stdscr.clear()
    height, width = stdscr.getmaxyx()
    message = [
        " __  __ _       _                 _   _____         _    ",
        "|  \\/  (_)_ __ (_)_ __ ___   __ _| | |_   _|_ _ ___| | __",
        "| |\\/| | | '_ \\| | '_ ` _ \\ / _` | |   | |/ _` / __| |/ /",
        "| |  | | | | | | | | | | | | (_| | |   | | (_| \\__ \\   < ",
        "|_|  |_|_|_| |_|_|_| |_| |_|\\__,_|_|   |_|\\__,_|___/_|\\_\\",
        "                                                         ",
        "  ___                        _          _             ",
        " / _ \\ _ __ __ _  __ _ _ __ (_)______ _| |_ ___  _ __ ",
        "| | | | '__/ _` |/ _` | '_ \\| |_  / _` | __/ _ \\| '__|",
        "| |_| | | | (_| | (_| | | | | |/ / (_| | || (_) | |   ",
        " \\___/|_|  \\__, |\\__,_|_| |_|_/___\\__,_|\\__\\___/|_|   ",
        "           |___/                                      "
    ]
    for i, line in enumerate(message):
        stdscr.addstr(height // 2 - len(message) // 2 + i, width // 2 - len(line) // 2, line)
    stdscr.refresh()
    stdscr.getch()

def quit_message(stdscr):
    stdscr.clear()
    height, width = stdscr.getmaxyx()
    box_height, box_width = 7, 50
    box_y, box_x = (height - box_height) // 2, (width - box_width) // 2

    # Draw box
    for i in range(box_height):
        for j in range(box_width):
            if i in [0, box_height - 1] or j in [0, box_width - 1]:
                stdscr.addch(box_y + i, box_x + j, curses.ACS_VLINE if j in [0, box_width - 1] else curses.ACS_HLINE)

    # Add message
    message = "Goodbye! Press any key to exit."
    stdscr.addstr(box_y + box_height // 2, box_x + (box_width - len(message)) // 2, message)
    stdscr.refresh()
    stdscr.getch()
    
def parse_date(date_str):
    try:
        return datetime.strptime(date_str, "%Y-%m-%d %H:%M:%S")
    except ValueError:
        return datetime.strptime(date_str, "%Y-%m-%d")

def set_tasks(loaded_tasks, tasks):
    for task_data in loaded_tasks:
        task = Task(description=task_data['description'], done=task_data['done'], 
                    cdate=parse_date(task_data['cdate']), 
                    ddate=parse_date(task_data['ddate']))
        tasks.append(task)

def main(stdscr):
    curses.curs_set(0)
    curses.init_pair(1, curses.COLOR_BLACK, curses.COLOR_WHITE)
    current_row = 0
    loaded_tasks = load_tasks()
    tasks = []
    set_tasks(loaded_tasks, tasks)

    splash_screen(stdscr)

    while True:
        display_menu(stdscr, current_row)
        key = stdscr.getch()
        
        if (key == ord('j') or key == curses.KEY_DOWN) and current_row < 4:
            current_row += 1
        elif (key == ord('k') or key == curses.KEY_UP) and current_row > 0:
            current_row -= 1
        elif key == curses.KEY_ENTER or key in [10, 13]:
            if current_row == 0:
                display_tasks(stdscr, tasks)
                stdscr.refresh()
                stdscr.getch()
            elif current_row == 1:
                add_task(stdscr, tasks)
            elif current_row == 2:
                toggle_task(stdscr, tasks)
            elif current_row == 3:
                delete_task(stdscr, tasks)
            elif current_row == 4:
                save_tasks(tasks)
                quit_message(stdscr)
                break
        elif key == ord('q'):
            save_tasks(tasks)
            quit_message(stdscr)
            break

if __name__ == "__main__":
    curses.wrapper(main)
