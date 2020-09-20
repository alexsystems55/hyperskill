from datetime import datetime, timedelta
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, Date
from sqlalchemy.orm import sessionmaker

engine = create_engine("sqlite:///todo.db?check_same_thread=False")
Base = declarative_base()


class Task(Base):
    __tablename__ = "task"
    id = Column(Integer, primary_key=True)
    task = Column(String)
    deadline = Column(Date, default=datetime.today())

    def __repr__(self):
        return self.task


def add_task():
    """
    Requests user for a task and puts it to the DB
    :return:
    """
    print("Enter task")
    task_text = input()
    print("Enter deadline")
    task_deadline = datetime.strptime(input(), "%Y-%m-%d")
    row = Task(task=task_text, deadline=task_deadline)
    session.add(row)
    session.commit()
    print("The task has been added!\n")


def print_tasks(header: str, rows):
    """
    Prints tasks selected from the DB
    :param header: Header to print
    :param rows: Selected rows from the DB
    :return:
    """
    print(f"{header}:")
    if rows.all():
        for num, row in enumerate(rows, start=1):
            line = f"{num}. {row.task}"
            if "task" in header:
                line += f". {row.deadline.strftime('%d %b')}"
            print(line)
    else:
        print("Nothing to do!")
    print()


def get_tasks(mode: str = "all"):
    """
    Selects tasks from the DB
    :param mode: What tasks to get (today, week, missed or all)
    :return:
    """
    today = datetime.today().date()
    if mode == "today":
        rows = (
            session.query(Task).filter(Task.deadline == today).order_by(Task.deadline)
        )
        day_str = f"Today {today.strftime('%d %b')}"
        print_tasks(day_str, rows)
    elif mode == "week":
        for week_day in range(7):
            day = today + timedelta(days=week_day)
            rows = (
                session.query(Task).filter(Task.deadline == day).order_by(Task.deadline)
            )
            day_str = f"{day.strftime('%A %d %b')}"
            print_tasks(day_str, rows)
    elif mode == "missed":
        rows = session.query(Task).filter(Task.deadline < today).order_by(Task.deadline)
        print_tasks("Missed tasks", rows)
    else:
        rows = session.query(Task).order_by(Task.deadline)
        print_tasks("All tasks", rows)


def delete_tasks():
    """
    Deletes selected task from the DB
    :return:
    """
    rows = session.query(Task).order_by(Task.deadline)
    if rows.all():
        print_tasks("Choose the number of the task you want to delete", rows)
        task = int(input())
        task_id = rows[task - 1].id
        session.query(Task).filter(Task.id==task_id).delete()
        session.commit()
        print("The task has been deleted!")
    else:
        print("Nothing to delete!")
    print()


def menu():
    """
    Main menu
    :return:
    """
    while True:
        print("1) Today's tasks")
        print("2) Week's tasks")
        print("3) All tasks")
        print("4) Missed tasks")
        print("5) Add task")
        print("6) Delete task")
        print("0) Exit")
        choice = input()
        print()
        if choice == "1":
            get_tasks(mode="today")
        elif choice == "2":
            get_tasks(mode="week")
        elif choice == "3":
            get_tasks()
        elif choice == "4":
            get_tasks(mode="missed")
        elif choice == "5":
            add_task()
        elif choice == "6":
            delete_tasks()
        elif choice == "0":
            print("Bye!")
            exit()


Base.metadata.create_all(engine)
Session = sessionmaker(bind=engine)
session = Session()
menu()
