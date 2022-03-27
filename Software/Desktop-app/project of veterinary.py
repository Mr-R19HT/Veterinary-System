from tkinter import *
from tkinter import ttk
import tkinter.messagebox
import pymysql




class ConnectorDB:

    def __init__(self, root):
        self.root = root
        titlespace = " "
        self.root.title(150 * titlespace + "Veterinary Clinic")
        self.root.geometry("1250x800+0+0")
        self.root.resizable(width=False, height=False)

        mainFrame = Frame(self.root, bd=10, width=770, height=700, relief=RIDGE, bg='cadet blue')
        mainFrame.grid()

        titleFrame = Frame(mainFrame, bd=7, width=770, height=100, relief=RIDGE)
        titleFrame.grid(row=0, column=0)

        topFrame = Frame(mainFrame, bd=5, width=770, height=500, relief=RIDGE)
        topFrame.grid(row=1, column=0)

        leftFrame = Frame(topFrame, bd=5, width=770, height=400, padx=2, bg="cadet blue", relief=RIDGE)
        leftFrame.pack(side=LEFT)
        leftFrame1 = Frame(leftFrame, bd=5, width=600, height=180, padx=12, pady=9, relief=RIDGE)
        leftFrame1.pack(side=TOP)

        rightFrame = Frame(topFrame, bd=5, width=100, height=400, padx=2, bg="cadet blue", relief=RIDGE)
        rightFrame.pack(side=RIGHT)
        rightFrame1 = Frame(rightFrame, bd=5, width=90, height=300, padx=2, pady=2, relief=RIDGE)
        rightFrame1.pack(side=TOP)
        #==================================================================================================

        employeeID = StringVar()
        firstName = StringVar()
        midName = StringVar()
        lastName = StringVar()
        city = StringVar()
        street = StringVar()
        gender = StringVar()
        zipCode = StringVar()
        birthDate = StringVar()
        #==================================================================================================

        def iExit():
            iExit = tkinter.messagebox.askyesno("MySQL Conection", "Confirm if You want to exit")
            if iExit > 0:
                root.destroy()
                return

        def Reset():
            self.entEmployeeID.delete(0, END)
            self.entFirstName.delete(0, END)
            self.entMidName.delete(0, END)
            self.entLastName.delete(0, END)
            self.entStreet.delete(0, END)
            self.entCity.delete(0, END)
            self.entGender.set("")
            self.entZipCode.delete(0, END)
            self.entBirthDate.delete(0, END)

        def addData():
            if employeeID.get() == "" or firstName.get() == "" or lastName.get() == "":
                tkinter.messagebox.showerror("MySQL Connection", "Enter Correct Details")
            else:
                sqlCon = pymysql.connect(host="localhost", user="root", password="MyNewPass", database="mydb")
                cur = sqlCon.cursor()
                cur.execute("insert into employee(ssn, F_name, M_name, L_name, City, Street, Zip_code, Emp_Gender, Emp_Bdata)"
                            " values (%s,%s,%s,%s,%s,%s,%s,%s,%s)", (
                    employeeID.get(),
                    firstName.get(),
                    midName.get(),
                    lastName.get(),
                    city.get(),
                    street.get(),
                    zipCode.get(),
                    gender.get(),
                    birthDate.get()
                ))
                sqlCon.commit()
                sqlCon.close()
                tkinter.messagebox.showinfo("MySQL Connection", "Data Inserted Success")
                Reset()

        def display():
            sqlCon = pymysql.connect(host="localhost", user="root", password="MyNewPass", database="mydb")
            cur = sqlCon.cursor()
            cur.execute("select ssn, F_name, M_name, L_name, City, Street, Zip_code, Emp_Gender, Emp_Bdata from employee")
            result = cur.fetchall()
            if len(result) !=0:
                self.employee_record.delete(*self.employee_record.get_children())
                for row in result:
                    self.employee_record.insert('', END, values=row)
            sqlCon.commit()
            sqlCon.close()

        def employeeInfo(ev):
            viewInfo = self.employee_record.focus()
            employeesData = self.employee_record.item(viewInfo)
            row = employeesData['values']
            employeeID.set(row[0]),
            firstName.set(row[1]),
            midName.set(row[2]),
            lastName.set(row[3]),
            city.set(row[4]),
            street.set(row[5]),
            zipCode.set(row[6]),
            gender.set(row[7]),
            birthDate.set(row[8])

        def update():
            sqlCon = pymysql.connect(host="localhost", user="root", password="MyNewPass", database="mydb")
            cur = sqlCon.cursor()
            cur.execute("update employee set F_name = %s, M_name = %s, L_name = %s, City = %s,"
                        " Street = %s, Zip_code = %s,Emp_Gender = %s, Emp_Bdata = %s where ssn = %s", (
                            firstName.get(),
                            midName.get(),
                            lastName.get(),
                            city.get(),
                            street.get(),
                            zipCode.get(),
                            gender.get(),
                            birthDate.get(),
                            employeeID.get()
                        ))
            sqlCon.commit()
            sqlCon.close()
            tkinter.messagebox.showinfo("MySQL Connection", "Data Updated Successfully")

        def delete():
            sqlCon = pymysql.connect(host="localhost", user="root", password="MyNewPass", database="mydb")
            cur = sqlCon.cursor()
            cur.execute("delete from employee where ssn = %s", employeeID.get())
            sqlCon.commit()
            sqlCon.close()
            tkinter.messagebox.showinfo("MySQL Connection", "Data Deleted Successfully")
            Reset()

        def search():
            try:
                sqlCon = pymysql.connect(host="localhost", user="root", password="MyNewPass", database="mydb")
                cur = sqlCon.cursor()
                cur.execute("select ssn, F_name, M_name, L_name , City , Street , Zip_code ,Emp_Gender, Emp_Bdata from employee where ssn = %s"%(employeeID.get()))
                row = cur.fetchone()

                employeeID.set(row[0]),
                firstName.set(row[1]),
                midName.set(row[2]),
                lastName.set(row[3]),
                city.set(row[4]),
                street.set(row[5]),
                zipCode.set(row[6]),
                gender.set(row[7]),
                birthDate.set(row[8])


                sqlCon.commit()

            except:
                tkinter.messagebox.showinfo("Data Entry Form", "No Such Record Found")
                Reset()
            sqlCon.close()

        #==================================================================================================

        self.lbltitle=Label(titleFrame, font=('arial', 40, 'bold'), text="Veterinary Clinic", bd=7)
        self.lbltitle.grid(row=0, column=0, padx=123)

        self.lblEmployeeID = Label(leftFrame1, font=('arial', 12, 'bold'), text="Employee ID", bd=7)
        self.lblEmployeeID.grid(row=1, column=0, sticky=W, padx=5)
        self.entEmployeeID = Entry(leftFrame1, font=('arial', 12, 'bold'), bd=5, width=44, justify='left', textvariable=employeeID)
        self.entEmployeeID.grid(row=1, column=1, sticky=W, padx=5)

        self.lblFirstName = Label(leftFrame1, font=('arial', 12, 'bold'), text="First Name", bd=7)
        self.lblFirstName.grid(row=2, column=0, sticky=W, padx=5)
        self.entFirstName = Entry(leftFrame1, font=('arial', 12, 'bold'), bd=5, width=44, justify='left', textvariable=firstName)
        self.entFirstName.grid(row=2, column=1, sticky=W, padx=5)

        self.lblMidName = Label(leftFrame1, font=('arial', 12, 'bold'), text="Mid Name", bd=7)
        self.lblMidName.grid(row=3, column=0, sticky=W, padx=5)
        self.entMidName = Entry(leftFrame1, font=('arial', 12, 'bold'), bd=5, width=44, justify='left',textvariable=midName)
        self.entMidName.grid(row=3, column=1, sticky=W, padx=5)

        self.lblLastName = Label(leftFrame1, font=('arial', 12, 'bold'), text="Last Name", bd=7)
        self.lblLastName.grid(row=4, column=0, sticky=W, padx=5)
        self.entLastName = Entry(leftFrame1, font=('arial', 12, 'bold'), bd=5, width=44, justify='left', textvariable=lastName)
        self.entLastName.grid(row=4, column=1, sticky=W, padx=5)

        self.lblCity = Label(leftFrame1, font=('arial', 12, 'bold'), text="City", bd=7)
        self.lblCity.grid(row=5, column=0, sticky=W, padx=5)
        self.entCity = Entry(leftFrame1, font=('arial', 12, 'bold'), bd=5, width=44, justify='left', textvariable=city)
        self.entCity.grid(row=5, column=1, sticky=W, padx=5)

        self.lblStreet = Label(leftFrame1, font=('arial', 12, 'bold'), text="Street", bd=7)
        self.lblStreet.grid(row=6, column=0, sticky=W, padx=5)
        self.entStreet = Entry(leftFrame1, font=('arial', 12, 'bold'), bd=5, width=44, justify='left', textvariable=street)
        self.entStreet.grid(row=6, column=1, sticky=W, padx=5)

        self.lblZipCode = Label(leftFrame1, font=('arial', 12, 'bold'), text="Zip Code", bd=5)
        self.lblZipCode.grid(row=7, column=0, sticky=W, padx=5)
        self.entZipCode = Entry(leftFrame1, font=('arial', 12, 'bold'), bd=5, width=44, textvariable=zipCode)
        self.entZipCode.grid(row=7, column=1, sticky=W, padx=5)

        self.lblGender = Label(leftFrame1, font=('arial', 12, 'bold'), text="Gender", bd=7)
        self.lblGender.grid(row=8, column=0, sticky=W, padx=5)
        self.entGender = ttk.Combobox(leftFrame1, font=('arial', 12, 'bold'), width=43, state='readonly', textvariable=gender)
        self.entGender['values']=(' ', 'Male', 'Female')
        self.entGender.current(0)
        self.entGender.grid(row=8, column=1, sticky=W, padx=5)

        self.lblBirthDate = Label(leftFrame1, font=('arial', 12, 'bold'), text="Birthday", bd=5)
        self.lblBirthDate.grid(row=9, column=0, sticky=W, padx=5)
        self.entBirthDate = Entry(leftFrame1, font=('arial', 12, 'bold'), bd=5, width=44, textvariable=birthDate)
        self.entBirthDate.grid(row=9, column=1, sticky=W, padx=5)


        #======================================================Table TreeView============================================
        scroll_y=Scrollbar(leftFrame, orient=VERTICAL)
        self.employee_record = ttk.Treeview(leftFrame, height=14, columns=("empID", "firstName", "midName", "lastName", "city",
        "street", "zipCode", "gender", "birthDate"), yscrollcommand=scroll_y.set)
        scroll_y.pack(side=RIGHT, fill=Y)

        self.employee_record.heading("empID", text="ID")
        self.employee_record.heading("firstName", text="First Name")
        self.employee_record.heading("midName", text="Mid Name")
        self.employee_record.heading("lastName", text="Last Name")
        self.employee_record.heading("city", text="City")
        self.employee_record.heading("street", text="Street")
        self.employee_record.heading("zipCode", text="Zip Code")
        self.employee_record.heading("gender", text="Gender")
        self.employee_record.heading("birthDate", text="Birthday")


        self.employee_record['show'] = 'headings'

        self.employee_record.column("empID", width=130)
        self.employee_record.column("firstName", width=110)
        self.employee_record.column("midName", width=110)
        self.employee_record.column("lastName", width=110)
        self.employee_record.column("city", width=100)
        self.employee_record.column("street", width=170)
        self.employee_record.column("zipCode", width=70)
        self.employee_record.column("gender", width=100)
        self.employee_record.column("birthDate", width=100)


        self.employee_record.pack(fill=BOTH, expand=1)
        self.employee_record.bind("<ButtonRelease-1>", employeeInfo)

        #display()

        #==================================================================================================
        self.btnAddNew=Button(rightFrame1, font=('arial', 16, 'bold'), text="Add new", bd=4, pady=1, padx=24,
                                width=8, height=2, command=addData).grid(row=0, column=0, padx=1)

        self.btnDisplay = Button(rightFrame1, font=('arial', 16, 'bold'), text="Report", bd=4, pady=1, padx=24,
                                width=8, height=2, command=display).grid(row=1, column=0, padx=1)

        self.btnUpdate = Button(rightFrame1, font=('arial', 16, 'bold'), text="Update", bd=4, pady=1, padx=24,
                                width=8, height=2, command=update).grid(row=2, column=0, padx=1)

        self.btnDelete = Button(rightFrame1, font=('arial', 16, 'bold'), text="Delete", bd=4, pady=1, padx=24,
                                width=8, height=2, command=delete).grid(row=3, column=0, padx=1)

        self.btnSearch = Button(rightFrame1, font=('arial', 16, 'bold'), text="Search", bd=4, pady=1, padx=24,
                                width=8, height=2, command=search).grid(row=4, column=0, padx=1)

        self.btnReset = Button(rightFrame1, font=('arial', 16, 'bold'), text="Reset", bd=4, pady=1, padx=24,
                               width=8, height=2, command=Reset).grid(row=5, column=0, padx=1)

        self.btnExit = Button(rightFrame1, font=('arial', 16, 'bold'), text="Exit", bd=4, pady=1, padx=24,
                                width=8, height=2, command=iExit).grid(row=7, column=0, padx=1)


if __name__=='__main__':
    root=Tk()
    application = ConnectorDB(root)
    root.mainloop()