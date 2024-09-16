from PIL import Image,ImageTk
import tkinter as tk
import tkinter.ttk as ttk
from tkinter.ttk import Treeview
from tkinter import Canvas,Tk,Button,Label,Toplevel,Pack
import mysql.connector
from mysql.connector import errors

MainFrame = Tk()
MainFrame.geometry("800x500")
MainFrame.title("Employee management System")
MainFrame.configure(background="#121210")

#------------------------------------------------Find Employee--------------------------------------
def Btn1Frame():
    def search_employee():
        tree.pack()

        alterLab.pack_forget()
        connection = mysql.connector.connect( host='localhost',
                                                    user= 'root',
                                                    password= 'password',
                                                    database= 'pbl')
        cursor = connection.cursor()   
        employee_id = entry_employee_id.get() 
        if employee_id=="":
            alterLab.configure(text="Enter Employee Id")
            alterLab.pack(padx=50,pady=150)
            tree.pack_forget()
        else:
            cursor.execute("select e.EmpId,e.EmployeeName,e.Gender,e.Age,d.DepartName,j.jobname,e.DOJ,j.jobsal from employee e ,department d natural join job j where e.empid = %s and j.jobid=e.E_jobid and d.Departmentid=e.E_Departmentid", (employee_id,))
            employee = cursor.fetchone()

            if employee:
                clear_table()
                tree.insert("", "end", values=employee)
                tree.pack(padx=30,pady=100)

            else:
                clear_table()
                alterLab.configure(text="Record Not found!")
                alterLab.pack(padx=50,pady=150)
                tree.pack_forget()

        connection.close()

    def display_employee():
        tree.pack()
    # clear entry box

        alterLab.pack_forget()
        connection = mysql.connector.connect( host='localhost',
                                                    user= 'root',
                                                    password= 'password',
                                                    database= 'pbl')

        cursor = connection.cursor()

        cursor.execute("select e.EmpId,e.EmployeeName,e.Gender,e.Age,d.DepartName,j.jobname,e.DOJ,j.jobsal from employee e ,department d natural join job j where e.empid and j.jobid=e.E_jobid and d.Departmentid=e.E_Departmentid order by e.empid")
        employees = cursor.fetchall()
        clear_table()
        
        if employees:
            for employee in employees:
                tree.insert("", "end", values=employee)
                tree.pack(padx=25,pady=100)
        else:
            clear_table()
            alterLab.config(text="Empty records")
            alterLab.pack(padx=50,pady=150)
            tree.pack_forget()
                

        connection.close()

    def clear_table():
        for row in tree.get_children():
            tree.delete(row)

    window = Toplevel(MainFrame)
    window.title("Employee Search")
    window.geometry("800x500")
    window.configure(bg="#121210",height="500",width="800")
    def clickout(event):
        if entry_employee_id.get() == "":
            entry_employee_id.config(fg="gray")
            entry_employee_id.insert(0,"Enter Employee ID")

    def click(event):
        if entry_employee_id.get() == "Enter Employee ID":
            entry_employee_id.delete(0,"end")
            entry_employee_id.config(fg="black")
        entry_employee_id.bind("<FocusOut>",clickout)

    HeadImg = ImageTk.PhotoImage(Image.open(r"E:\pbl\pbl\frame0\EMHead.png"))
    SearchImg = ImageTk.PhotoImage(Image.open(r"E:\pbl\pbl\frame0\SBtn.png"))
    WholeTImg = ImageTk.PhotoImage(Image.open(r"E:\pbl\pbl\frame0\VAl.png"))

    EmpLabel = Label(window,image=HeadImg,background="#121210")
    EmpLabel.pack()

    entry_employee_id = tk.Entry(window,width="50",font=10,fg="gray")
    entry_employee_id.place(x=130,y=65)
    entry_employee_id.insert(0,"Enter Employee ID")
    entry_employee_id.bind("<FocusIn>", click)

    search_button = tk.Button(window, image=SearchImg, bg="#121210",command=search_employee,borderwidth=0,relief="flat",activebackground="#121210")
    search_button.place(x=580,y=64,width=28,height=24)

    display_button = tk.Button(window,image=WholeTImg, bg="#121210",borderwidth=0,relief="flat",activebackground="#121210", command=display_employee)
    display_button.place(x=30,y=50)

    tree = ttk.Treeview(window, columns=("ID", "Name", "Gender", "Age", "Department","Job Position" ,"Date of Joining", "Salary"),height=10)
    tree.heading("ID", text="ID")
    tree.heading("Name", text="Name")
    tree.heading("Gender", text="Gender")
    tree.heading("Age", text="Age")
    tree.heading("Department", text="Department")
    tree.heading("Job Position", text="Job Position")
    tree.heading("Date of Joining", text="Date of Joining")
    tree.heading("Salary", text="Salary")

    tree["show"]="headings"

    tree.column("ID",width=50,anchor='center')
    tree.column("Name",width=130,anchor='center')
    tree.column("Gender",width=70,anchor='center')
    tree.column("Age",width=50,anchor='center')
    tree.column("Department",width=100,anchor='center')
    tree.column("Job Position",width=150,anchor='center')
    tree.column("Date of Joining",width=70,anchor='center')
    tree.column("Salary",width=70,anchor='center')

    tree.pack()
    tree.pack_forget()

    alterLab = Label(window,text="Empty Table",height="10",width="100",font=('Arial',15),bg="#121210",fg="white")
    alterLab.pack()
    alterLab.pack_forget()

    window.resizable(False,False)
    window.mainloop()

#-------------------------------------------Add employee----------------------------------------------

def AddEmp():
    #btnState(AddBtn)
    def add_employee():
        label_result.place_forget()
        emp_id = entry_employee_id.get()
        emp_name = entry_employee_name.get()
        emp_age = entry_employee_age.get()
        emp_gender = entry_employee_gender.get()
        emp_address = entry_employee_address.get()
        emp_email = entry_employee_email.get()
        emp_doj = entry_employee_doj.get()
        dept_name = selected_dept.get()
        job_pos = entry_job_position.get()
        try:
            connection = mysql.connector.connect( host= 'localhost',
                                                user= 'root',
                                                password= 'password',
                                                database= 'pbl')

            cursor = connection.cursor()
            cursor1 = connection.cursor()
            cursor2 = connection.cursor()

            cursor1.execute("select departmentid from department where departname = %s",(dept_name,))
            deptID = cursor1.fetchone()
            val1=""
            for i in deptID:
                val1=val1+str(i)

            cursor2.execute("select jobid from job where jobname = %s", (job_pos,))
            jobid = cursor2.fetchone()
            val2=""
            for i in jobid:
                val2=val2+str(i)

            cursor.execute("insert into employee(Empid,EmployeeName,Age,Gender,Empemail,Empadd,DOJ,E_Departmentid,E_jobid)values(%s,%s,%s,%s,%s,%s,%s,%s,%s)",
                        (int(emp_id),emp_name,emp_age,emp_gender,emp_email,emp_address,emp_doj,int(val1),int(val2)))

            connection.commit()

            if cursor.rowcount:
                label_result.place(x=300,y=460)
                label_result.configure(text="Employee Successfully Added")
            else:
                label_result.place(x=300,y=460)
                label_result.configure(text="Employee Not Added")
            

            entry_employee_id.delete(0,tk.END)
            entry_employee_name.delete(0,tk.END)
            entry_employee_age.delete(0,tk.END)
            entry_employee_gender.selection_clear()
            entry_employee_address.delete(0,tk.END)
            entry_employee_email.delete(0,tk.END)
            entry_employee_doj.delete(0,tk.END)
            entry_employee_doj.config(fg="gray")
            entry_employee_doj.insert(0,"(YYYY-MM-DD)")
            entry_employee_doj.bind("<FocusIn>", click)
            entry_deparment_name.select_clear()
            entry_job_position.select_clear()
        except errors.Error as err:
            label_result.place(x=150,y=420)
            label_result.configure(text=str(err))
            print(err)

        cursor.close()
        cursor1.close()
        cursor2.close()
        connection.close()
        

    window = Toplevel(MainFrame)
    window.geometry("800x500")
    window.title("Add Employee")
    window.configure(background="#121210")

    def clickout(event):
        if entry_employee_doj.get() == "":
            entry_employee_doj.config(fg="gray")
            entry_employee_doj.insert(0,"(YYYY-MM-DD)")

    def click(event):
        if entry_employee_doj.get() == "(YYYY-MM-DD)":
            entry_employee_doj.delete(0,"end")
            entry_employee_doj.config(fg="black")
        entry_employee_doj.bind("<FocusOut>",clickout)

    label_employee_id = tk.Label(window, text="Enter Employee ID:",font=(15),bg="#121210",fg="white")
    label_employee_id.place(x=100,y=20)
    entry_employee_id = tk.Entry(window,width="30",font=(15))
    entry_employee_id.place(x=335,y=20)

    label_employee_name = tk.Label(window, text="Enter Employee Name:",font=(15),bg="#121210",fg="white")
    label_employee_name.place(x=100,y=60)
    entry_employee_name = tk.Entry(window,width="30",font=(15))
    entry_employee_name.place(x=335,y=60)

    label_employee_age = tk.Label(window, text="Enter Employee Age:",font=(15),bg="#121210",fg="white")
    label_employee_age.place(x=100,y=100)
    entry_employee_age = tk.Entry(window,width="30",font=(15))
    entry_employee_age.place(x=335,y=100)

    label_employee_gender = tk.Label(window, text="Select Employee Gender:",font=(15),bg="#121210",fg="white")
    label_employee_gender.place(x=100,y=140)
    select_gender = tk.StringVar()
    entry_employee_gender = ttk.Combobox(window, textvariable=select_gender, font=(8),state="readonly")
    entry_employee_gender["values"] = ("MALE","FEMALE")
    entry_employee_gender.place(x=335,y=140)

    label_employee_email = tk.Label(window, text="Enter Employee Email:",font=(15),bg="#121210",fg="white")
    label_employee_email.place(x=100,y=180)
    entry_employee_email = tk.Entry(window,width="30",font=(15))
    entry_employee_email.place(x=335,y=180)

    label_employee_address = tk.Label(window, text="Enter Employee Address:",font=(15),bg="#121210",fg="white")
    label_employee_address.place(x=100,y=220)
    entry_employee_address = tk.Entry(window,width="30",font=(15))
    entry_employee_address.place(x=335,y=220)

    label_employee_doj = tk.Label(window, text="Enter Date of Joining:",font=(15),bg="#121210",fg="white")
    label_employee_doj.place(x=100,y=260)
    entry_employee_doj = tk.Entry(window,width="30",font=(18),fg="gray")
    entry_employee_doj.insert(0,"(YYYY-MM-DD)")
    entry_employee_doj.bind("<FocusIn>", click)
    entry_employee_doj.place(x=335,y=260)

    label_deparment_name = tk.Label(window, text="Select Deparment Name:",font=(15),bg="#121210",fg="white")
    label_deparment_name.place(x=100,y=300)
    selected_dept = tk.StringVar()
    entry_deparment_name = ttk.Combobox(window,textvariable=selected_dept,font=(8))

    connection = mysql.connector.connect( host= 'localhost',
                                                user= 'root',
                                                password= 'password',
                                                database= 'pbl')

    cursor = connection.cursor()
    cursor.execute("select DepartName from department")
    DeptVal = cursor.fetchall()
    entry_deparment_name["values"] = DeptVal
    entry_deparment_name['state'] = "readonly"
    entry_deparment_name.place(x=335,y=302)

    label_job_position = tk.Label(window, text="Select Job Role:",font=(15),bg="#121210",fg="white")
    label_job_position.place(x=100,y=340)
    selected_role = tk.StringVar()
    entry_job_position = ttk.Combobox(window,textvariable=selected_role,font=(8))

    cursor.execute("select jobname from job")
    JobVal = cursor.fetchall()
    entry_job_position['values'] = JobVal
    entry_job_position['state'] = "readonly"
    entry_job_position.place(x=335,y=345)

    InsBtnImg = ImageTk.PhotoImage(Image.open(r"E:\pbl\pbl\frame0\ABtn.png"))
    add_button = tk.Button(window, image=InsBtnImg, bg="#121210",command=add_employee,borderwidth=0,activebackground="#121210")
    add_button.place(x=300,y=390)

    label_result = tk.Label(window, text="",font=(18),bg="#121210",fg="white")
    label_result.place(x=300,y=420)

    window.resizable(False,False)
    window.mainloop()

#---------------------------------------Remove button function--------------------------------------------

def RmBtn():
    global employee_id
    def search_employee():
        global employee_id
        employee_id = entry_employee_id.get()
        connection = mysql.connector.connect( host='localhost',
                                            user= 'root',
                                            password= 'password',
                                            database= 'pbl')
        cursor = connection.cursor()

        cursor.execute("select e.EmpId,e.EmployeeName,e.Gender,e.Age,d.DepartName,j.jobname,e.DOJ,j.jobsal from employee e ,department d natural join job j where e.empid = %s and j.jobid=e.E_jobid and d.Departmentid=e.E_Departmentid",(employee_id,))
        employee = cursor.fetchone()

        if employee:
            clear_table()
            tree.insert("", "end", values=employee)
            tree.pack(padx=30,pady=50)
            text_employee_details.configure(text = "Employee Found")
            text_employee_details.pack(padx=30,pady=50)
            delete_button.place(x=325,y=300)

        else:
            clear_table()
            tree.pack_forget()
            text_employee_details.configure(text="Employee not Found")
            text_employee_details.pack(padx=30,pady=200)
            delete_button.place_forget()

        connection.close()

    def delete_employee():
        global employee_id
        employee_id = entry_employee_id.get()
        tree.pack_forget()
        connection = mysql.connector.connect( host='localhost',
                                            user= 'root',
                                            password= 'password',
                                            database= 'pbl')
        cursor = connection.cursor()
        
        if employee_id=="":
            text_employee_details.configure(text="Enter Employee ID")
            text_employee_details.pack(pady=200)
        else:
            cursor.execute("delete from employee where empID = %s",(employee_id,))
            connection.commit()
            
            # clear_table()
            if cursor.rowcount:
                text_employee_details.configure(text = f"Employee with ID: {employee_id} is deleted")
                text_employee_details.pack(padx=30,pady=50)
                delete_button.place_forget()
            else:
                text_employee_details.configure(text="Employee not Found")
                text_employee_details.pack(padx=30,pady=50)
                delete_button.place_forget()
            

        connection.close()

    def clear_table():
        for row in tree.get_children():
            tree.delete(row)

    window = Toplevel(MainFrame)
    window.title("Employee Remove")
    window.configure(bg="#121210")
    window.geometry("800x500")
    def clickout(event):
        if entry_employee_id.get() == "":
            entry_employee_id.config(fg="gray")
            entry_employee_id.insert(0,"Enter Employee ID")

    def click(event):
        if entry_employee_id.get() == "Enter Employee ID":
            entry_employee_id.delete(0,"end")
            entry_employee_id.config(fg="black")
        entry_employee_id.bind("<FocusOut>",clickout)

    HeadImg = ImageTk.PhotoImage(Image.open(r"E:\pbl\pbl\frame0\EMHead.png"))

    label_employee_id = tk.Label(window, image=HeadImg,bg="#121210")
    label_employee_id.pack()
    entry_employee_id = tk.Entry(window,width="50",font=10,fg="gray")
    entry_employee_id.place(x=130,y=65)
    entry_employee_id.insert(0,"Enter Employee ID")
    entry_employee_id.bind("<FocusIn>", click)


    SearchImg = ImageTk.PhotoImage(Image.open(r"E:\pbl\pbl\frame0\SBtn.png"))
    search_button = tk.Button(window, image=SearchImg, bg="#121210",activebackground="#121210",borderwidth=0,command=search_employee)
    search_button.place(x=580,y=64,width=28,height=24)
    delImg = ImageTk.PhotoImage(Image.open(r"E:\pbl\pbl\frame0\RBtn.png"))
    delete_button = tk.Button(window,image=delImg, bg="#121210", activebackground="#121210",borderwidth=0, command=delete_employee)
    delete_button.place(x=325,y=300)

    tree = ttk.Treeview(window, columns=("ID", "Name", "Gender", "Age", "Department","Job Position" ,"Date of Joining", "Salary"),height=1)
    tree.heading("ID", text="ID")
    tree.heading("Name", text="Name")
    tree.heading("Gender", text="Gender")
    tree.heading("Age", text="Age")
    tree.heading("Department", text="Department")
    tree.heading("Job Position", text="Job Position")
    tree.heading("Date of Joining", text="Date of Joining")
    tree.heading("Salary", text="Salary")

    tree["show"]="headings"

    tree.column("ID",width=50,anchor='center')
    tree.column("Name",width=130,anchor='center')
    tree.column("Gender",width=70,anchor='center')
    tree.column("Age",width=50,anchor='center')
    tree.column("Department",width=100,anchor='center')
    tree.column("Job Position",width=150,anchor='center')
    tree.column("Date of Joining",width=70,anchor='center')
    tree.column("Salary",width=70,anchor='center')

    tree.pack_forget()

    text_employee_details = tk.Label(window,background="#121210",font=('Arial',15),fg="white")
    text_employee_details.pack_forget()
    window.resizable(False,False)
    window.mainloop()

#-------------------------UPDATE FUNCTION-------------------------------

def UpdFun():
    employee_id=''
    # ------------------------------------------BUTTON FUNCTIONS DEFINITIONS -----------------------------------------------------------------------------------------------------
    def search_employee():
        tree.pack()
        
        
        alterLab.pack_forget()
        connection = mysql.connector.connect( host='localhost',
                                                user= 'root',
                                                password= 'password',
                                                database= 'pbl') 
        cursor = connection.cursor()   
        employee_id = entry_employee_id.get() 
        if employee_id=="":
            alterLab.configure(text="Enter Employee Id")
            alterLab.pack(pady=50)
            tree.pack_forget()
            search_button['state']=tk.ACTIVE
            
        else:
            cursor.execute("select e. EmpId,EmployeeName,Age,Empemail,EmpAdd,d. DepartName,j. jobname,jobsal from employee e natural join department d natural join job j where e.EmpId = %s and e.E_Departmentid = d.Departmentid and e.E_jobid = j.jobid", (employee_id,))
            employee = cursor.fetchone()

            if employee:
                clear_table()
                tree.insert("", "end", values=employee)
                tree.pack(padx=30,pady=50)
                PerBtn.place(x=100,y=200)
                ProfBtn.place(x=550,y=200)
                
            else:
                clear_table()
                alterLab.configure(text="Record Not found!")
                alterLab.pack(pady=50)
                tree.pack_forget()
                search_button['state'] = tk.ACTIVE
                PerBtn.place_forget()
                ProfBtn.place_forget()

        if PerBtn['state'] == tk.DISABLED or ProfBtn['state']==tk.DISABLED:
            search_button['state'] = tk.DISABLED
        else:
            search_button['state'] = tk.ACTIVE

        connection.close()

    def clear_table():
        for row in tree.get_children():
            tree.delete(row)

    # Personal btn: 
    def PerUpd():
        alterLab.pack_forget()
        PerBtn.place_forget()
        ProfBtn.place_forget()

        empNameLab.place(x=90,y=220)
        empName.place(x=100,y=250)
        empAddressLab.place(x=90,y=280)
        empAddress.place(x=100,y=310)
        empAgeLab.place(x=490,y=220)
        AgeCombo.place(x=500,y=250)
        empMailLab.place(x=490,y=280)
        empMail.place(x=500,y=310)
        UpdBtn1.place(x=300,y=400)

        employee_id = entry_employee_id.get() 
        connection = mysql.connector.connect( host='localhost',
                                                        user= 'root',
                                                        password= 'password',
                                                        database= 'pbl')
            
        cursor = connection.cursor()
        cursor.execute("select EmployeeName,EmpAdd,Age,Empemail from employee where empid = %s",(employee_id,))

        EmpDetails = cursor.fetchall()
        print(EmpDetails[0][0])
        empName.insert(0,EmpDetails[0][0])
        empAddress.insert(0,EmpDetails[0][1])
        selected_Age.set(EmpDetails[0][2])
        empMail.insert(0,EmpDetails[0][3])

        search_button['state'] = tk.DISABLED
        ProfBtn['state'] = tk.ACTIVE
        PerBtn.configure(state=tk.DISABLED)

    # Professional btn:

    def ProfUpd():
        ProfBtn.place_forget()
        alterLab.pack_forget()
        PerBtn.place_forget()
        empRoleLab.place(x=100,y=250)
        empRole.place(x=100,y=280)
        empDeptLab.place(x=500,y=250)
        DeptCombo.place(x=500,y=280)
        UpdBtn2.place(x=300,y=400)

        employee_id = entry_employee_id.get() 
        connection = mysql.connector.connect( host='localhost',
                                                        user= 'root',
                                                        password= 'password',
                                                        database= 'pbl')
            
        cursor = connection.cursor()
        cursor.execute("select e.EmpId, d. DepartName,j. jobname from employee e natural join department d natural join job j where e.EmpId = %s and e.E_Departmentid = d.Departmentid and e.E_jobid = j.jobid;",(employee_id,))
        ProfDetails = cursor.fetchall()


        selected_dept.set(ProfDetails[0][1])
        selected_jobs.set(ProfDetails[0][2])

        search_button['state'] = tk.DISABLED
        ProfBtn.configure(state=tk.DISABLED)
        PerBtn['state'] = tk.ACTIVE
      
    def updBtnF1():
        search_button['state'] = tk.ACTIVE

        empNameLab.place_forget()
        empName.place_forget()
        empAddressLab.place_forget()
        empAddress.place_forget()
        empAgeLab.place_forget()
        AgeCombo.place_forget()
        empMailLab.place_forget()
        empMail.place_forget()
        UpdBtn1.place_forget()

        EmpName = empName.get()
        EmpAdd = empAddress.get()
        EmpAge = selected_Age.get()
        EmpMail = empMail.get()
        employee_id = entry_employee_id.get() 
        try:
            connection = mysql.connector.connect( host='localhost',
                                                        user= 'root',
                                                        password= 'password',
                                                        database= 'pbl')
            
            cursor = connection.cursor()
            cursor1 = connection.cursor()
            cursor2 = connection.cursor()
            cursor3 = connection.cursor()


            
            cursor.execute("update employee set EmployeeName = %s where empid = %s",(EmpName,employee_id))
            cursor1.execute("update employee set EmpAdd = %s where empid = %s",(EmpAdd,employee_id))
            cursor2.execute("update employee set Age = %s where empid = %s",(EmpAge,employee_id))
            cursor3.execute("update employee set Empemail = %s where empid = %s",(EmpMail,employee_id))
            connection.commit()

            alterLab.configure(text=f"Data updated!")
            alterLab.pack()
            PerBtn.configure(state=tk.ACTIVE)
        except errors.Error as err:
            alterLab.configure(text=err)
            alterLab.pack()

 
    def updBtnF2():
        search_button['state'] = tk.ACTIVE
        empRoleLab.place_forget()
        empRole.place_forget()
        empDeptLab.place_forget()
        DeptCombo.place_forget()
        UpdBtn2.place_forget()

        jobRole = selected_jobs.get()
        empDept = selected_dept.get()
        employee_id = entry_employee_id.get()

        try:
            connection = mysql.connector.connect( host='localhost',
                                                        user= 'root',
                                                        password= 'password',
                                                        database= 'pbl')
    
            cursor1 = connection.cursor()
            cursor2 = connection.cursor()
            cursor = connection.cursor()
            cursor1.execute("select jobid from job where jobname=%s",(jobRole,))
            jobId = cursor1.fetchone()
            cursor1.execute("select Departmentid from department where DepartName = %s",(empDept,))
            deptId = cursor1.fetchone()
            print("deptId , JobId ,EMpId ",deptId,jobId,employee_id)
            cursor.execute("update employee set E_departmentid = %s where EmpId = %s",(deptId[0],employee_id,))
            cursor2.execute("update employee set E_jobid = %s where EmpId = %s",(jobId[0],employee_id,))
            connection.commit()
            alterLab.configure(text="data updated")
            alterLab.pack()
            ProfBtn.configure(state=tk.ACTIVE)
        
        except errors.Error as err:
            alterLab.configure(text=err)
            alterLab.pack()
            print(err)

    connection = mysql.connector.connect( host='localhost',
                                                    user= 'root',
                                                    password= 'password',
                                                    database= 'pbl')

    cursor = connection.cursor()

    cursor.execute("select DepartName from department")
    employees = cursor.fetchall()

    cursor.execute("select jobname from job")
    jobs = cursor.fetchall()


    # -----------------------------------------UPDATE BUTTONS GUI Structure from here----------------------------------------------------------------------------

    UpdWin = Toplevel(MainFrame)
    UpdWin.geometry("800x500")
    UpdWin.title("Update Employee Details")
    UpdWin.configure(bg="#121210")
    def clickout(event):
        if entry_employee_id.get() == "":
            entry_employee_id.config(fg="gray")
            entry_employee_id.insert(0,"Enter Employee ID")

    def click(event):
        if entry_employee_id.get() == "Enter Employee ID":
            entry_employee_id.delete(0,"end")
            entry_employee_id.config(fg="black")
        entry_employee_id.bind("<FocusOut>",clickout)

    HeadImg = ImageTk.PhotoImage(Image.open(r"E:\pbl\pbl\frame0\EMHead.png"))
    EmpLabel = Label(UpdWin,image=HeadImg,background="#121210")
    EmpLabel.pack()
    entry_employee_id = tk.Entry(UpdWin,width="50",font=10,fg="gray")
    entry_employee_id.place(x=130,y=65)
    entry_employee_id.insert(0,"Enter Employee ID")
    entry_employee_id.bind("<FocusIn>", click)

    SearchImg = ImageTk.PhotoImage(Image.open(r"E:\pbl\pbl\frame0\SBtn.png"))
    search_button = tk.Button(UpdWin, image=SearchImg, bg="#121210",command=search_employee,borderwidth=0,relief="flat",activebackground="#121210")
    search_button.place(x=580,y=64,width=28,height=24)



    tree = ttk.Treeview(UpdWin, columns=("ID", "Name", "Age","Email","Address", "Dept", "Job"),height=1)
    tree.heading("ID", text="ID")
    tree.heading("Name", text="Name")
    tree.heading("Age", text="Age")
    tree.heading("Email", text="Email")
    tree.heading("Address", text="Address")
    tree.heading("Dept", text="Dept")
    tree.heading("Job",text="Job role")



    tree["show"]="headings"

    tree.column("ID",width=50,anchor='center')
    tree.column("Name",width=100,anchor='center')
    tree.column("Age",width=50,anchor='center')
    tree.column("Email",width=100,anchor='center')
    tree.column("Address",width=100,anchor='center')
    tree.column("Dept",width=100,anchor='center')
    tree.column("Job",width=100,anchor='center')



    tree.pack()
    tree.pack_forget()

    alterLab = Label(UpdWin,text="Empty Table",font=('Arial',18),bg="#121210",fg="white")
    alterLab.pack()
    alterLab.pack_forget()
    # personal btn declaring
    PerImg = ImageTk.PhotoImage(Image.open(r"E:\pbl\pbl\frame0\PerDtl.png"))
    PerBtn = tk.Button(UpdWin,image=PerImg,activebackground="#121210",borderwidth=0,command=PerUpd,background="#121210")
    PerBtn.place(x=100,y=200)
    PerBtn.place_forget()
    # professional btn declaring
    ProfImg = ImageTk.PhotoImage(Image.open(r"E:\pbl\pbl\frame0\ProDtl.png"))
    ProfBtn = tk.Button(UpdWin,image=ProfImg,activebackground="#121210",command=ProfUpd,borderwidth=0,background="#121210")
    ProfBtn.place(x=550,y=200)
    ProfBtn.place_forget()
    # Personal btn define
    empNameLab = tk.Label(UpdWin,text="Enter Employee Name:",background="#121210",font=(15),fg="white")
    empNameLab.pack_forget()

    empName = tk.Entry(UpdWin,width=20,font=(16))
    empName.pack_forget()

    empAddressLab = tk.Label(UpdWin,text="Enter Employee Address:",background="#121210",font=(15),fg="white")
    empAddressLab.pack_forget()

    empAddress = tk.Entry(UpdWin,width=20,font=(16))
    empAddress.pack_forget()

    empMailLab = tk.Label(UpdWin,text="Enter Employee Email:",background="#121210",font=(15),fg="white")
    empMailLab.pack_forget()

    empMail = tk.Entry(UpdWin,width=20,font=(16))
    empMail.pack_forget()

    empAgeLab = tk.Label(UpdWin,text="Enter Employee Age:",background="#121210",font=(15),fg="white")
    empAgeLab.pack_forget()
    selected_Age = tk.IntVar()
    AgeCombo = ttk.Combobox(UpdWin,textvariable=selected_Age)
    value=[]
    for i in range(20,51):
        value.append(i)
    AgeCombo["values"] = value
    AgeCombo['state'] = "readonly"

    #Professional btn define

    empDeptLab = tk.Label(UpdWin,text="Enter Employee Department:",background="#121210",font=(15),fg="white")

    selected_dept = tk.StringVar()
    DeptCombo = ttk.Combobox(UpdWin,textvariable=selected_dept)
    DeptCombo["values"] = employees
    DeptCombo['state'] = "readyonly"


    empRoleLab = tk.Label(UpdWin,text="Enter Employee Job role:",background="#121210",font=(15),fg="white")
    empRoleLab.place_forget()

    selected_jobs = tk.StringVar()
    empRole  =ttk.Combobox(UpdWin,textvariable=selected_jobs)
    empRole['values'] = jobs
    empRole['state'] = "readonly"
    empRole.pack_forget()

    #Update buttons
    UpdImg = ImageTk.PhotoImage(Image.open(r"E:\pbl\pbl\frame0\UBtn.png"))
    UpdBtn1 = tk.Button(UpdWin,image=UpdImg,background="#121210",activebackground="#121210",command=updBtnF1,borderwidth=0)
    UpdBtn2 = tk.Button(UpdWin,image=UpdImg,background="#121210",activebackground="#121210",command=updBtnF2,borderwidth=0)
    UpdWin.resizable(False,False)
    UpdWin.mainloop()

# -------------------------------------SALARY CALCULATE FUNCTION---------------------------------------------

def SalCalFun():
    def search_employee():
        tree.pack()
        alterLab.pack_forget()
        connection = mysql.connector.connect( host='localhost',
                                                user= 'root',
                                                password= 'password',
                                                database= 'pbl') 
        cursor = connection.cursor()   
        employee_id = entry_employee_id.get() 
        if employee_id=="":
            alterLab.configure(text="Enter Employee Id",bg="#121210",fg="white")
            alterLab.pack(padx=300,pady=150)
            tree.pack_forget()
            search_button['state']=tk.ACTIVE
            
        else:
            cursor.execute("select e. EmpId,EmployeeName,j. jobname,jobsal from employee e natural join department d natural join job j where e.EmpId = %s and e.E_Departmentid = d.Departmentid and e.E_jobid = j.jobid", (employee_id,))
            employee = cursor.fetchone()

            if employee:
                clear_table()
                tree.insert("", "end", values=employee)
                tree.pack(padx=25,pady=50)
                CalBtn.place(x=325,y=300)
                TotalWorkLab.place(x=50,y=180)
                TotalCombo.place(x=450,y=180)
                PresentWorkLab.place(x=50,y=230)
                WorkDay.place(x=350,y=230)
                
            else:
                clear_table()
                alterLab.configure(text="Record Not found!",bg="#121210",fg="white")
                alterLab.pack(padx=300,pady=150)
                tree.pack_forget()
                search_button['state'] = tk.ACTIVE
                CalBtn.place_forget()
                TotalWorkLab.place_forget()
                TotalCombo.place_forget()
                PresentWorkLab.place_forget()
                WorkDay.place_forget()

        connection.close()

    def clear_table():
        for row in tree.get_children():
            tree.delete(row)


    def CalBtnFun():
        connection = mysql.connector.connect( host='localhost',
                                                user= 'root',
                                                password= 'password',
                                                database= 'pbl') 
        cursor = connection.cursor()   
        employee_id = entry_employee_id.get()
        TotalDays = selectedTDays.get() 
        
        cursor.execute("select j.jobsal from employee e natural join job j where e.empid = %s and j.jobid=e.E_jobid",(employee_id,))
        sal = (cursor.fetchone())
        salStr=""
        for i in sal:
            salStr+=str(i)

        Salary = int(salStr)
        try:
            PresentDays = int(WorkDay.get())
            if PresentDays > TotalDays:
                alterLab.config(text=f"Enter valid Days",font=('Arial',15),bg="#121210",fg="white")
                alterLab.place(x=300,y=400)
            else:
                DaySal = Salary/TotalDays
                outStr = (round(DaySal*PresentDays,2),"₹")
                alterLab.configure(text=outStr,font=('Arial',20),bg="#121210",fg="white")
                alterLab.place(x=330,y=400)
                WorkDay.delete(0,tk.END)
                
            
        except ValueError:
            alterLab.config(text=f"Enter Employee Present Days",font=('Arial',15))
            alterLab.place(x=280,y=400)
        except ZeroDivisionError:
            alterLab.configure(text="0.0 ₹",font=('Arial',20))
            alterLab.place(x=330,y=400)



    SalWin = Toplevel(MainFrame)
    SalWin.title("Salary Calculator")
    SalWin.geometry("800x500")
    SalWin.configure(background="#121210")
    def clickout(event):
        if entry_employee_id.get() == "":
            entry_employee_id.config(fg="gray")
            entry_employee_id.insert(0,"Enter Employee ID")

    def click(event):
        if entry_employee_id.get() == "Enter Employee ID":
            entry_employee_id.delete(0,"end")
            entry_employee_id.config(fg="black")
        entry_employee_id.bind("<FocusOut>",clickout)
    HeadImg = ImageTk.PhotoImage(Image.open(r"E:\pbl\pbl\frame0\EMHead.png"))
    EmpLabel = Label(SalWin,image=HeadImg,background="#121210")
    EmpLabel.pack()
    entry_employee_id = tk.Entry(SalWin,width="50",font=10,fg="gray")
    entry_employee_id.place(x=130,y=65)
    entry_employee_id.insert(0,"Enter Employee ID")
    entry_employee_id.bind("<FocusIn>", click)

    SearchImg = ImageTk.PhotoImage(Image.open(r"E:\pbl\pbl\frame0\SBtn.png"))
    CalImg = ImageTk.PhotoImage(Image.open(r"E:\pbl\pbl\frame0\Cal.png"))
    selectedTDays = tk.IntVar()
    TotalCombo = ttk.Combobox(SalWin,textvariable=selectedTDays)
    TotalDay=[]
    for i in range(15,28):
        TotalDay.append(i)
    TotalCombo["values"]=TotalDay
    TotalCombo["state"]="readonly"

    WorkDay = tk.Entry(SalWin,font=(18),width=10)

    search_button = tk.Button(SalWin, image=SearchImg, bg="#121210",command=search_employee,borderwidth=0,relief="flat",activebackground="#121210")
    search_button.place(x=580,y=64,width=28,height=24)
    
    CalBtn = tk.Button(SalWin, image=CalImg, bg="#121210",command=CalBtnFun,borderwidth=0,relief="flat",activebackground="#121210")


    TotalWorkLab = tk.Label(SalWin,text="Enter Total working Days(for this Month):",font=(15),bg="#121210",fg="white")
    PresentWorkLab = tk.Label(SalWin,text="Enter Employee Present Days:",font=(15),bg="#121210",fg="white")

    tree = ttk.Treeview(SalWin, columns=("ID", "Name", "Job" ,"Salary"),height=1)
    tree.heading("ID", text="ID")
    tree.heading("Name", text="Name")
    tree.heading("Job",text="Job role")
    tree.heading("Salary", text="Salary")


    tree["show"]="headings"

    tree.column("ID",width=50)
    tree.column("Name",width=100)
    tree.column("Job",width=100)
    tree.column("Salary",width=100)




    tree.pack()
    tree.pack_forget()

    alterLab = tk.Label(SalWin,text="Empty Table",font=('Arial',18),bg="#121210",fg="white")
    alterLab.pack()
    alterLab.pack_forget()
    SalWin.resizable(False,False)
    SalWin.mainloop()

# -------------------------------------HOME PAGE GUID STRUCTURE-----------------------------------------------

HeadImage = ImageTk.PhotoImage(Image.open(r"E:\pbl\pbl\frame0\EMHead.png"))
HeadLabel = Label(MainFrame,image= HeadImage,background="#121210")
HeadLabel.pack()
#button(side)
BtnImg1 = ImageTk.PhotoImage(Image.open(r"E:\pbl\pbl\frame0\FEmp.png"))
FindEmp = Button(MainFrame,background="#121210",image=BtnImg1,relief="flat",borderwidth=0,command=Btn1Frame,state=tk.NORMAL,activebackground="#121210")
FindEmp.place(x=300.0,y=100.0,width=200.0,height=55)

BtnImg2 = ImageTk.PhotoImage(Image.open(r"E:\pbl\pbl\frame0\UDtl.png"))
UpdateBtn = Button(MainFrame,background="#121210",image=BtnImg2,relief="flat",borderwidth=0,state=tk.NORMAL,command=UpdFun,activebackground="#121210")
UpdateBtn.place(x=100,y=300,width=200,height=55)

BtnImg3 = ImageTk.PhotoImage(Image.open(r"E:\pbl\pbl\frame0\SCal.png"))
SalCalBtn = Button(MainFrame,background="#121210",image=BtnImg3,relief="flat",borderwidth=0,state=tk.NORMAL,command=SalCalFun,activebackground="#121210")
SalCalBtn.place(x=500,y=300,width=200,height=55)

#Button(RSide)
BtnImg4 = ImageTk.PhotoImage(Image.open(r"E:\pbl\pbl\frame0\AEmp.png"))
AddBtn = Button(MainFrame,background="#121210",image=BtnImg4,relief="flat",borderwidth=0,state=tk.NORMAL,command=AddEmp,activebackground="#121210")
AddBtn.place(x=100,y=200,width=200,height=55)

BtnImg5 = ImageTk.PhotoImage(Image.open(r"E:\pbl\pbl\frame0\REmp.png"))
RmBtn = Button(MainFrame,background="#121210",image=BtnImg5,relief="flat",borderwidth=0,state=tk.NORMAL,command=RmBtn,activebackground="#121210")
RmBtn.place(x=500,y=200,width=200,height=55)


MainFrame.resizable(False,False)
MainFrame.mainloop()
