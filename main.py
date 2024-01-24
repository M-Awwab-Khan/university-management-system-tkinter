import tkinter
from tkinter import ttk
import sv_ttk
import sqlite3
import random

class App:
    def __init__(self):
        self.window = tkinter.Tk()
        self.window.geometry('1280x720')

        self.con = sqlite3.connect('database.db')
        self.cur = self.con.cursor()

        self.cur.execute(
            """
            CREATE TABLE IF NOT EXISTS Teacher (
                tid INTEGER PRIMARY KEY, 
                name TEXT,
                designation TEXT,
                salary INTEGER,
                deptid INTEGER,
                FOREIGN KEY(deptid) REFERENCES Department(deptid)
            );
            """
        )
        self.cur.execute(
            """
            CREATE TABLE IF NOT EXISTS Department (
                deptid INTEGER PRIMARY KEY, 
                dname TEXT
            );
            """
        )
        self.cur.execute(
            """
            CREATE TABLE IF NOT EXISTS Course (
                ccode TEXT PRIMARY KEY, 
                cname TEXT,
                credithrs INTEGER,
                tid INTEGER,
                FOREIGN KEY(tid) REFERENCES Teacher(tid)

            );
            """
        )
        self.menu_page()

        sv_ttk.use_light_theme()
        self.window.mainloop()

    def menu_page(self):
        self.main_menu_page = ttk.Frame(self.window)
        self.main_menu_page.pack(fill='both', expand=True)
        ttk.Label(self.main_menu_page, text='University Management System', font=(None, 30)).pack(pady=50)
        self.menu_frame = ttk.Frame(self.main_menu_page, width=50)
        self.menu_frame.place(in_=self.main_menu_page, anchor='center', relx=0.5, rely=0.5)

        ttk.Button(self.menu_frame, text='Teacher', style="Accent.TButton", command=self.teacher_page).pack(pady=10)
        ttk.Button(self.menu_frame, text='Department', style="Accent.TButton", command=self.department_page).pack(pady=10)
        ttk.Button(self.menu_frame, text='Course', style="Accent.TButton", command=self.course_page).pack(pady=10)

    def teacher_page(self):
        self.switch_page(self.main_menu_page)

        self.main_teacher_page = ttk.Frame(self.window)
        self.main_teacher_page.pack(fill='both', expand=True)

        ttk.Button(self.main_teacher_page, text=" ← Back ", style="Accent.TButton", command=lambda x=self.main_teacher_page: self.back_to_menu(x)).pack(anchor='nw', pady=30, padx=30)
        ttk.Label(self.main_teacher_page, text='Manage Teachers', font=(None, 30)).pack()

        self.teacher_frame = ttk.Frame(self.main_teacher_page)
        self.teacher_frame.place(in_=self.main_teacher_page, anchor='center', relx=0.5, rely=0.5)

        ttk.Label(self.teacher_frame, text="Name").grid(row=0, column=0, pady=(10, 0))
        self.name_entry = ttk.Entry(self.teacher_frame) 
        self.name_entry.grid(row=1, column=0, pady=10)

        ttk.Label(self.teacher_frame, text="Designation").grid(row=0, column=2, pady=(10, 0))
        self.designation_entry = ttk.Entry(self.teacher_frame)
        self.designation_entry.grid(row=1, column=2, pady=10)

        ttk.Label(self.teacher_frame, text="Salary").grid(row=0, column=3, pady=(10, 0))
        self.salary_entry = ttk.Spinbox(self.teacher_frame, from_=1, to=100, width=12)
        self.salary_entry.grid(row=1, column=3, pady=10)

        ttk.Label(self.teacher_frame, text="Department ID").grid(row=0, column=4, pady=(10, 0))
        results = self.cur.execute("""SELECT deptid FROM Department""").fetchall()
        self.dept_id = ttk.Combobox(self.teacher_frame, state="readonly", values=[i[0] for i in results])
        self.dept_id.current(1)
        self.dept_id.grid(row=1, column=4)

        columns = ('tid', 'name', 'salary', 'designation', 'deptid')
        self.teacher_tree = ttk.Treeview(self.teacher_frame, columns=columns, show="headings")
        self.teacher_tree.heading('tid', text='Teacher ID')
        self.teacher_tree.heading('name', text='Name')
        self.teacher_tree.heading('designation', text="Designation")
        self.teacher_tree.heading('salary', text='Salary')
        self.teacher_tree.heading('deptid', text="Department ID")
        self.teacher_tree.grid(row=2, column=0, columnspan=5, padx=20, pady=10)
        self.update_tree_view(self.teacher_tree, 'Teacher')

        ttk.Button(self.teacher_frame, text="Create New Teacher", style="Accent.TButton", command=self.create_teacher).grid(row=3, column=2, columnspan=2, sticky="news", padx=20, pady=5)
        ttk.Button(self.teacher_frame, text="Delete Selected Teacher", command=self.delete_teacher).grid(row=4, column=2, columnspan=2, sticky="news", padx=20, pady=5)

    def create_teacher(self):
        data = {
            'tid': random.randint(100, 999),
            'name': self.name_entry.get(),
            'designation': self.designation_entry.get(),
            'salary': int(self.salary_entry.get()),
            'deptid': int(self.dept_id.get())
        }
        query = f"""INSERT INTO Teacher VALUES ({data['tid']}, '{data['name']}', '{data['designation']}', {data['salary']}, {data['deptid']})"""
        self.cur.execute(query)
        self.con.commit()
        self.update_tree_view(self.teacher_tree, 'Teacher')

    def delete_teacher(self):
        current_item = self.teacher_tree.focus()
        to_delete = self.teacher_tree.item(current_item)['values']

        query = f"""DELETE FROM Teacher WHERE tid={to_delete[0]}"""
        self.cur.execute(query)
        self.con.commit()
        self.update_tree_view(self.teacher_tree, 'Teacher')

    def update_tree_view(self, tree, table):
        res = self.cur.execute(f"""SELECT * FROM {table}""")
        results = res.fetchall()
        tree.delete(*tree.get_children())
        for entry in results:
            tree.insert('', tkinter.END, values=entry)

    def department_page(self):
        self.switch_page(self.main_menu_page)

        self.main_department_page = ttk.Frame(self.window)
        self.main_department_page.pack(fill='both', expand=True)

        ttk.Button(self.main_department_page, text=" ← Back ", style="Accent.TButton", command=lambda x=self.main_department_page: self.back_to_menu(x)).pack(anchor='nw', pady=30, padx=30)
        ttk.Label(self.main_department_page, text='Manage Departments', font=(None, 30)).pack()
        self.department_frame = ttk.Frame(self.main_department_page)
        self.department_frame.place(in_=self.main_department_page, anchor='center', relx=0.5, rely=0.5)

        ttk.Label(self.department_frame, text="Department ID").grid(row=0, column=0, pady=(10, 0))
        self.deptid_entry = ttk.Spinbox(self.department_frame, from_=1, to=100, width=12)
        self.deptid_entry.grid(row=1, column=0, pady=10)

        ttk.Label(self.department_frame, text="Department Name").grid(row=0, column=1, pady=(10, 0))
        self.dname_entry = ttk.Entry(self.department_frame) 
        self.dname_entry.grid(row=1, column=1, pady=10)

        columns = ('deptid', 'name')
        self.department_tree = ttk.Treeview(self.department_frame, columns=columns, show="headings")
        self.department_tree.heading('deptid', text="Department ID")
        self.department_tree.heading('name', text='Department Name')
        self.department_tree.grid(row=2, column=0, columnspan=2, padx=20, pady=10)
        self.update_tree_view(self.department_tree, 'Department')

        ttk.Button(self.department_frame, text="Create New Department", style="Accent.TButton", command=self.create_department).grid(row=3, column=0, columnspan=2, sticky="news", padx=20, pady=5)
        ttk.Button(self.department_frame, text="Delete Selected Department", command=self.delete_department).grid(row=4, column=0, columnspan=2, sticky="news", padx=20, pady=5)

    def create_department(self):
        data = {
            'deptid': int(self.deptid_entry.get()),
            'dname': self.dname_entry.get(),
        }
        query = f"""INSERT INTO Department VALUES ({data['deptid']}, '{data['dname']}')"""
        self.cur.execute(query)
        self.con.commit()
        self.update_tree_view(self.department_tree, 'Department')

    def delete_department(self):
        current_item = self.department_tree.focus()
        to_delete = self.department_tree.item(current_item)['values']

        query = f"""DELETE FROM Department WHERE deptid={to_delete[0]}"""
        self.cur.execute(query)
        self.con.commit()
        self.update_tree_view(self.department_tree, 'Department')

    def course_page(self):
        self.switch_page(self.main_menu_page)

        self.main_course_page = ttk.Frame(self.window)
        self.main_course_page.pack(fill='both', expand=True)

        ttk.Button(self.main_course_page, text=" ← Back ", style="Accent.TButton", command=lambda x=self.main_course_page: self.back_to_menu(x)).pack(anchor='nw', pady=30, padx=30)
        ttk.Label(self.main_course_page, text='Manage Courses', font=(None, 30)).pack()
        self.course_frame = ttk.Frame(self.main_course_page)
        self.course_frame.place(in_=self.main_course_page, anchor='center', relx=0.5, rely=0.5)

        ttk.Label(self.course_frame, text="Course Code").grid(row=0, column=0, pady=(10, 0))
        self.ccode_entry = ttk.Entry(self.course_frame) 
        self.ccode_entry.grid(row=1, column=0, pady=10)

        ttk.Label(self.course_frame, text="Course Name").grid(row=0, column=1, pady=(10, 0))
        self.cname_entry = ttk.Entry(self.course_frame) 
        self.cname_entry.grid(row=1, column=1, pady=10)

        ttk.Label(self.course_frame, text="Credit Hours").grid(row=0, column=2, pady=(10, 0))
        self.chrs_entry = ttk.Spinbox(self.course_frame, from_=1, to=100, width=12)
        self.chrs_entry.grid(row=1, column=2, pady=10)

        ttk.Label(self.course_frame, text="Teacher ID").grid(row=0, column=3, pady=(10, 0))
        results = self.cur.execute("""SELECT tid FROM Teacher""").fetchall()
        self.course_tid = ttk.Combobox(self.course_frame, state="readonly", values=[i[0] for i in results])
        self.course_tid.current(1)
        self.course_tid.grid(row=1, column=3)
        columns = ('ccode', 'cname', 'chrs', 'tid')
        self.course_tree = ttk.Treeview(self.course_frame, columns=columns, show="headings")
        self.course_tree.heading('ccode', text="Course Code")
        self.course_tree.heading('cname', text='Course Name')
        self.course_tree.heading('chrs', text='Credit Hours')
        self.course_tree.heading('tid', text='Teacher ID')
        self.course_tree.grid(row=2, column=0, columnspan=4, padx=20, pady=10)
        self.update_tree_view(self.course_tree, 'Course')

        ttk.Button(self.course_frame, text="Create New Course", style="Accent.TButton", command=self.create_course).grid(row=3, column=1, columnspan=2, sticky="news", padx=20, pady=5)
        ttk.Button(self.course_frame, text="Delete Selected Course", command=self.delete_course).grid(row=4, column=1, columnspan=2, sticky="news", padx=20, pady=5)

    def create_course(self):
        data = {
            'ccode': self.ccode_entry.get(),
            'cname': self.cname_entry.get(),
            'chrs': int(self.chrs_entry.get()),
            'tid': int(self.course_tid.get())
        }
        query = f"""INSERT INTO Course VALUES ('{data['ccode']}', '{data['cname']}', {data['chrs']}, {data['tid']})"""
        self.cur.execute(query)
        self.con.commit()
        self.update_tree_view(self.course_tree, 'Course')

    def delete_course(self):
        current_item = self.course_tree.focus()
        to_delete = self.course_tree.item(current_item)['values']

        query = f"""DELETE FROM Course WHERE ccode='{to_delete[0]}'"""
        self.cur.execute(query)
        self.con.commit()
        self.update_tree_view(self.course_tree, 'Course')

    def switch_page(self, old_page):
        old_page.pack_forget()

    def back_to_menu(self, onpage):
        onpage.pack_forget()
        self.main_menu_page.pack(fill='both', expand=True)

if __name__ == '__main__':
    app = App()