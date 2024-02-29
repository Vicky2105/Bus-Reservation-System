from logging import exception
from tkinter import *
from tkcalendar import Calendar
import calendar
from tkinter import messagebox
import mysql.connector
from email.message import EmailMessage
import ssl
import smtplib
from datetime import datetime
import datetime as dt

global final_date
final_date=None
#Ticket Booking method 
def booking():
    def check_available():
        def book():
            passenger = name_entry.get()
            phone = mob_entry.get()
            mail = mail_ent.get()
            cur = selected_option.get()
            dest = dest_option.get()
            gender = ""
            if v.get() == 1:
                gender = "male"
            elif v.get() == 2:
                gender = "Female"
            else:
                messagebox.showinfo("Information", "Please select Gender")
            if passenger == "" or phone == "" or mail == "":
                messagebox.showinfo("Information", "Please fill your details properly")
            elif len(phone) != 10:
                messagebox.showinfo("Information", "Mobile number incorrect")
            else:
                qur = "insert into reserved values(%s,%s,%s,%s,%s,%s,%s,%s)"
                val = (cur, dest, final_date, passenger, gender,mail,reg_id,ticket_price)
                db = mysql.connector.connect(
                host="localhost",
                username="root",
                password="Vicky@123",
                database="busreserve"
                )
                cursor = db.cursor()
                cursor.execute(qur, val)
                db.commit()
                messagebox.showinfo("Information", "Your Reservation is successfull")
                sender = "pillivikas2105@gmail.com"
                rec = "218r1a05e8@cmrec.ac.in"
                password = "odkh xvhi uvbj odgh"
                subject = "Your Bus Reservation Confirmation and Best Wishes for a Happy Journey!"
                body = """
            Dear {passenger},
                We are thrilled to inform you that your reservation for a seat on our bus service has been
successfully processed! Your comfort and satisfaction are our top priorities, and
we're delighted to have you on board for your upcoming journey.
        Regestration ID:{reg}
        Bus Route: {cur} To {dest}
        Date of Journey: {final_date}
        Departure Time: 9:00AM

    Thank you for choosing VTravels. We greatly appreciate your trust in us
    and look forward to serving you again in the future.
        Wishing you a safe, comfortable, and happy journey!

        
    warm regards,
    Manager VTravels."""
                formatted = body.format(passenger=passenger, reg=reg_id, cur=cur, dest=dest, final_date=final_date)
                em = EmailMessage()
                em['From'] = sender
                em['To'] = mail
                em['Subject'] = subject
                em.set_content(formatted, )
                context = ssl.create_default_context()
                try:
                    with smtplib.SMTP_SSL("smtp.gmail.com", 465, "context") as sm:
                        sm.login(sender, password)
                        sm.send_message(em)
                except exception as e:
                    messagebox.showinfo("Information", "Enter Valid Email Address")

        cur = selected_option.get()
        dest = dest_option.get()
        if final_date==None:
            messagebox.showinfo("Information","Please select a date")
        elif cur not in avl_cities or dest not in avl_cities:
            messagebox.showinfo("Information","Please select current and destination cities")
        else:    
            db = mysql.connector.connect(
                host="localhost",
                username="root",
                password="Vicky@123",
                database="busreserve"
            )
            cursor = db.cursor()
            query = "select count(*)from reserved where journeydate=%s and current=%s and destination=%s"
            dateq=(final_date,cur,dest)
            cursor.execute(query, dateq)
            result = cursor.fetchall()
            count = result[0]
            bus_capacity = 2
            if count[0] == bus_capacity:
                messagebox.showinfo("Information", "Sorry we are full on that day")
            else:
                price = [[0, 170, 250, 300, 490, 420, 220, 380, 150, 360],
                 [170, 0, 120, 220, 320, 300, 120, 280, 120, 320],
                 [250, 120, 0, 230, 120, 240, 120, 250, 190, 180],
                 [120, 450, 170, 0, 140, 240, 280, 320, 100, 240],
                 [120, 280, 230, 240, 0, 220, 230, 220, 240, 180],
                 [250, 120, 255, 230, 120, 0, 120, 250, 190, 180],
                 [120, 450, 170, 280, 140, 240, 0, 320, 100, 240],
                 [120, 280, 230, 240, 250, 220, 230, 0, 240, 180],
                 [250, 120, 255, 230, 120, 360, 120, 250, 0, 180],
                 [120, 450, 170, 140, 140, 240, 280, 320, 100, 0]]
                global reg_id
                reg_id = str(final_date).replace("-", "")
                reg_id = reg_id.replace("2024","")
                reg_id = int(reg_id) +(count[0] + 1)
                femalebtn.place(x=325, y=475)
                name_lab.place(x=175, y=395)
                name_entry.place(x=255, y=395)
                mob_lab.place(x=175, y=435)
                mail_ent.place(x=255, y=515)
                malebtn.place(x=255, y=475)
                mail_lab.place(x=175, y=515)
                ticket_price = price[avl_cities.index(selected_option.get())][avl_cities.index(dest_option.get())]
                amt = "The amount to be paid : " + str(ticket_price)
                price_lab.config(text=amt)
                gen_lab.place(x=175, y=475)
                mob_entry.place(x=255, y=435)
                label.place(x=155, y=355)
                confirm = Button(wind, text="Confirm Ticket", font=("Arial", 15), command=book)
                confirm.place(x=215, y=595)
    def fun():
        cur = selected_option.get()
        dest = dest_option.get()
        if cur == "" or dest == "" or cur == " " or dest == " ":
            messagebox.showinfo("warning", "fill all fields")
        elif cur == dest:
            messagebox.showinfo("Information", "please select different destination")
        elif cur not in avl_cities or dest not in avl_cities:
            messagebox.showinfo("Information", "please select current city and destination city")
        else:
            sel_date = Calendar(wind, selectmode="day", date_pattern='y-mm-dd')
            sel_date.place(x=450, y=150)
            def closeCal():
                global final_date
                final_date = sel_date.get_date()
                comp=datetime.strptime(sel_date.get_date(), "%Y-%m-%d").date()
                #print(type(comp))
                if comp<=dt.date.today():
                    messagebox.showinfo("Information","please select Valid Date")
                else:
                    date_field.config(text="Your journey is on " + final_date)
                    sel_date.place(x=-1000,y=100)
                    okay.place(x=-1000,y=100)
            okay = Button(wind, text="ok", font=("Arial", 15), command=closeCal)
            okay.place(x=555, y=350)
    wind = Toplevel(root)
    wind.geometry("800x750")
    wind.configure(bg="#F7E464")
    wind.title("Ticket Booking")
    wind.grab_set()
    wind.protocol("WM_DELETE_WINDOW",lambda:wind.destroy())
    heading = Label(wind,text="BOOOK YOUR TICKET HERE", font=("Arial", 25),bg="#F7E464")
    heading.place(x=150,y=75)
    
    db = mysql.connector.connect(
        host="localhost",
        username="root",
        password="Vicky@123",
        database="busreserve"
    )
    cursor = db.cursor()
    # cities
    avl_cities = ["Adilabad", "Karimnagar", "Warangal", "Khammam", "Mahbubnagar", "Nalgonda", "Medak", "Rangareddy",
                  "Nizamabad", "Hyderabad"]

    # select route
    curr_lab = Label(wind,text="From:", font=("Arial", 15),bg="#F7E464")
    curr_lab.place(x=175, y=150)
    dest_lab = Label(wind,text="To:", font=("Arial", 15),bg="#F7E464")
    dest_lab.place(x=175, y=200)
    global selected_option
    global dest_option
    selected_option = StringVar(wind)
    selected_option.set("Select your city")
    dest_option = StringVar(wind)
    dest_option.set("Select your destination")
    cur_dropdown = OptionMenu(wind, selected_option, *avl_cities)
    cur_dropdown.place(x=235, y=150)
    dest_dropdown = OptionMenu(wind, dest_option, *avl_cities)
    dest_dropdown.place(x=235, y=200)

    sel_date = Button(wind, text="select date", font=("Arial", 15), command=fun)
    sel_date.place(x=175, y=250)

    date_field = Label(wind, text="", font=("Arial", 15),bg="#F7E464")
    date_field.place(x=300, y=255)

    # passenger details
    label = Label(wind,text="Seats are available fill details to book your seats", font=("Arial", 15),bg="#F7E464")
    name_lab = Label(wind, text="Name:", font=("Arial", 15),bg="#F7E464")
    name_entry = Entry(wind, font=("Arial", 15),bg="#CCE5FF")
    mob_lab = Label(wind, text="Mobile:", font=("Arial", 15),bg="#F7E464")
    mob_entry = Entry(wind, font=("Arial", 15),bg="#CCE5FF")
    gen_lab = Label(wind, text="Gender:", font=("Arial", 15),bg="#F7E464")
    v = IntVar()
    malebtn = Radiobutton(wind, text="Male", variable=v, value=1, font=("Arial", 15),bg="#F7E464")
    femalebtn = Radiobutton(wind, text="Female", variable=v, value=2, font=("Arial", 15),bg="#F7E464")
    mail_lab = Label(wind, text="E-Mail:", font=("Arial", 15),bg="#F7E464")
    mail_ent = Entry(wind, font=("Arial", 15),bg="#CCE5FF")

    check = Button(wind, text="Check Availability", font=("Arial", 15), command=check_available)
    check.place(x=205, y=300)
    price_lab = Label(wind, text="", font=("Arial", 15),bg="#F7E464")
    price_lab.place(x=175, y=555)

    wind.mainloop()  



#postpone method implementation
def post():
    def fetch():
        def okay():
            mydb=mysql.connector.connect(
            host="localhost",
            username="root",
            password="Vicky@123",
            database="busreserve"
            )
            cursor=mydb.cursor()
            name=temp[0][6]
            date=cal.get_date()
            comp=datetime.strptime(date, "%Y-%m-%d").date()
            cal.place(x=-1000,y=10)
            newdt="Your Journey is postponed to "+str(date)
            if comp<=dt.date.today():
                messagebox.showinfo("Information","Please select valid date")
            else:
                query="update reserved set journeydate=%s where reservationID=%s"
                val=(date,name)
                cursor.execute(query,val)
                mydb.commit()
                messagebox.showinfo("Information",newdt)
                post_wind.destroy()
        query="select *from reserved where reservationID=%s"
        val=reg_fld.get()
        mydb=mysql.connector.connect(
            host="localhost",
            username="root",
            password="Vicky@123",
            database="busreserve"
            )
        cursor=mydb.cursor()
        cursor.execute(query,(val,))
        global temp
        temp=cursor.fetchall()
        if len(temp)==0:
            messagebox.showinfo("Information","Please enter valid reservation ID")
        else:
            us_name="Name : "+temp[0][3]
            name=Label(post_wind,text=us_name,font=("Arial",15),bg="#8EE7FD")
            name.place(x=150,y=250)
            jrny="Journey :From "+temp[0][0]+" To "+temp[0][1]
            journey=Label(post_wind,text=jrny,font=("Arial",15),bg="#8EE7FD")
            journey.place(x=150,y=290)
            jrny_dt="Journey Date : "+str(temp[0][2])
            journey_date=Label(post_wind,text=jrny_dt,font=("Arial",15),bg="#8EE7FD")
            journey_date.place(x=150,y=330)
            tkt="Ticket Price is "
            price=Label(post_wind,text=tkt+temp[0][7],font=("Arial",15),bg="#8EE7FD")
            price.place(x=150,y=370)
            new=Label(post_wind,text="Select Your New Journey Date",font=("Arial",15),bg="#8EE7FD")
            new.place(x=130,y=370)
            cal=Calendar(post_wind,selectmode="day", date_pattern='y-mm-dd')
            cal.place(x=150,y=400)
            ok=Button(post_wind,text="Ok",font=("Arial",15),command=okay,bg="#FDCD8E")
            ok.place(x=450,y=450)
    post_wind=Toplevel(root)
    post_wind.geometry("800x750")
    post_wind.configure(bg="#8EE7FD")
    post_wind.grab_set()
    post_wind.protocol("WM_DELETE_WINDOW",lambda:post_wind.destroy())
    head=Label(post_wind,text="POSTPONE YOUR TICKET",font=("Arial",25),bg="#8EE7FD")
    head.place(x=200,y=75)
    reg=Label(post_wind,text="Enter your Reservation ID:",font=("Arial",15),bg="#8EE7FD")
    reg.place(x=100,y=150)
    reg_fld=Entry(post_wind,font=("Arial",15),bg="#FDCD8E")
    reg_fld.place(x=350,y=150)
    details=Button(post_wind,text="Fetch Details",font=("Arial",15),bg="#FDCD8E",command=fetch)
    details.place(x=275,y=200)
    post_wind.mainloop()

#cancel method implementation
def canc():
    def cfetch():
        def cokay():
            mydb=mysql.connector.connect(
            host="localhost",
            username="root",
            password="Vicky@123",
            database="busreserve"
            )
            cursor=mydb.cursor()
            name=temp[0][8]
            newdt="Your Ticket is cancelled successfully"
            confirmation=messagebox.askquestion("Confirmation","Do you really want to cancel the ticket")
            if confirmation=='yes':
                query="delete from reserved where reservationID=%s"
                cursor.execute(query,(name,))
                mydb.commit()
                messagebox.showinfo("Information",newdt)
                post_wind.destroy()
            else:
                print("okay")
        query="select *from reserved where reservationID=%s"
        val=reg_fld.get()
        mydb=mysql.connector.connect(
            host="localhost",
            username="root",
            password="Vicky@123",
            database="busreserve"
            )
        cursor=mydb.cursor()
        cursor.execute(query,(val,))
        global temp
        temp=cursor.fetchall()
        if len(temp)==0:
            messagebox.showinfo("Information","Please enter valid reservation ID")
        else:
            us_name="Name : "+temp[0][3]
            name=Label(post_wind,text=us_name,font=("Arial",15),bg="#8EE7FD")
            name.place(x=150,y=250)
            jrny="Journey :From "+temp[0][0]+" To "+temp[0][1]
            journey=Label(post_wind,text=jrny,font=("Arial",15),bg="#8EE7FD")
            journey.place(x=150,y=290)
            jrny_dt="Journey Date : "+str(temp[0][2])
            journey_date=Label(post_wind,text=jrny_dt,font=("Arial",15),bg="#8EE7FD")
            journey_date.place(x=150,y=330)
            tkt="Ticket Price is "
            price=Label(post_wind,text=tkt+temp[0][7],font=("Arial",15),bg="#8EE7FD")
            price.place(x=150,y=370)
            canc=Button(post_wind,text="Cancel Ticket",font=("Arial",15),command=cokay,bg="#FDCD8E")
            canc.place(x=450,y=450)
    post_wind=Toplevel(root)
    post_wind.title("Ticket Cancellation")
    post_wind.geometry("800x750")
    post_wind.configure(bg="#8EE7FD")
    post_wind.grab_set()
    post_wind.protocol("WM_DELETE_WINDOW",lambda:post_wind.destroy())
    reg=Label(post_wind,text="Enter your Reservation ID:",font=("Arial",15),bg="#8EE7FD")
    head=Label(post_wind,text="TICKET CANCELLATION",font=("Arial",25),bg="#8EE7FD")
    head.place(x=200,y=75)
    reg.place(x=100,y=150)
    reg_fld=Entry(post_wind,font=("Arial",15),bg="#FDCD8E")
    reg_fld.place(x=350,y=150)
    details=Button(post_wind,text="Fetch Details",font=("Arial",15),bg="#FDCD8E",command=cfetch)
    details.place(x=275,y=200)
#print(dt.date.today())
root=Tk()
root.geometry("800x750")
root.configure(bg="#F7E464")
root.title("Bus Reservation System")
welcome=Label(text="Welcome To VTravels",font=("Arial", 35),fg="black",bg="#F7E464")
welcome.place(x=170,y=150)

tcktbk=Button(root,text="Ticket Booking",font=("Arial", 15),command=booking)
tcktbk.place(x=300,y=250)
postpone=Button(root,text="Ticket Postpone",font=("Arial", 15),command=post)
postpone.place(x=300,y=320)
cancel=Button(root,text="Ticket Cancellation",font=("Arial", 15),command=canc)
cancel.place(x=300,y=390)
