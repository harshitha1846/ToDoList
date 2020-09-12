from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine,Column, Integer, String, Date
from datetime import datetime,timedelta
from sqlalchemy.orm import sessionmaker

engine = create_engine('sqlite:///todo.db?check_same_thread=False')
Base = declarative_base()

class Table(Base):
    __tablename__ = 'task'
    id = Column(Integer, primary_key=True, autoincrement=True)
    task = Column(String, default='default_value')
    deadline = Column(Date, default=datetime.today().date())

    def __repr__(self):
        return self.task

Base.metadata.create_all(engine)
Session = sessionmaker(bind=engine)
session =Session()

def print_data(r,f=None):
    if r:
        for j in range(0, len(r)):
            print(f'{j+1}. {r[j].task}')
        print()
    elif f == 'm':
        print('Nothing is missed!\n')
    else:
        print('Nothing to do!\n')

def all_tasks(rows, f=None):
    if rows:
        for j in range(0, len(rows)):
            print(f'{j + 1}. {rows[j].task}. {rows[j].deadline.strftime("%d %b").lstrip("0").replace(" 0", " ")}')
        print()
    elif f == 'd':
        print('Nothing to delete\n')
        return 0

def today_task():
    rows = session.query(Table).filter(Table.deadline == datetime.today().date()).all()
    print(f'Today {datetime.now().strftime("%d %b")}:')
    print_data(rows)

def weekly_task():
    for i in range(7):
        weekdays = datetime.today().date() + timedelta(days=i)
        rows = session.query(Table).filter(Table.deadline == weekdays).all()
        print(f'{weekdays.strftime("%A %d %b")}:')
        print_data(rows)

def delete_task():
    rows = session.query(Table).order_by(Table.deadline).all()
    if all_tasks(rows, 'd') != 0:
        print('Choose the number of the task you want to delete:')
        index = int(input())
        deleterow = rows[index - 1]
        session.delete(deleterow)
        session.commit()
        print('The task has been deleted!')

def add_task():
    content = input('Enter task\n')
    time = input('Enter deadline\n')
    new_row = Table(task=content, deadline=datetime.strptime(time, '%Y-%m-%d'))
    session.add(new_row)
    session.commit()
    print('The task has been added!')

while True:
    choice = input("1) Today's tasks\n2) Week's tasks\n3) All tasks\n4) Missed tasks"
                   "\n5) Add task\n6) Delete task\n0) Exit\n")
    if choice == '1':
        today_task()
    elif choice == '2':
        weekly_task()
    elif choice == '3':
        print('All tasks:')
        rows = session.query(Table).order_by(Table.deadline).all()
        all_tasks(rows)
    elif choice == '4':
        rows = session.query(Table).filter(Table.deadline < datetime.today().date()).all()
        print('Missed tasks:')
        print_data(rows,'m')
    elif choice == '5':
        add_task()
    elif choice == '6':
        delete_task()
    elif choice == '0':
        print('Bye!')
        break
    else:
        print("Invalid choice")
