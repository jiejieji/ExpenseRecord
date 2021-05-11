from tkinter import *
from tkinter import ttk, messagebox
import csv
from datetime import datetime 
GUI = Tk()
GUI.title('โปรแกรมบัรทึกค่าใช้จ่าย')
GUI.geometry('500x600+500+50')

##########MENU###########
menubar = Menu(GUI)
GUI.config(menu=menubar)

#file menu 
filemenu = Menu(menubar,tearoff=0)
filemenu = Menu(menubar)
menubar.add_cascade(label='File',menu=filemenu)
filemenu.add_command(label='Import CSV')
filemenu.add_command(label='Export to googlesheet')
# help
def About():
    messagebox.showinfo('About','สวัสดี โปรแกรมนี้คือโปรแกรมบันทึกข้อมูล\nสนใจบริจาคเราไหม? ขอ 1 BCH ก็พอแล้ว\nBCH Address: xr1234')

helpmenu = Menu(menubar,tearoff=0)

menubar.add_cascade(label='help',menu=helpmenu)
helpmenu.add_command(label='About',command=About)
# donate
donatemenu = Menu(menubar,tearoff=0)
donatemenu = Menu(menubar)
menubar.add_cascade(label='Donate',menu=donatemenu)


########################

Tab = ttk.Notebook(GUI)
T1 = Frame(Tab) 
T2 = Frame(Tab)
Tab.pack(fill=BOTH, expand=1)

expenseicon = PhotoImage(file='cash.png').subsample(5)
listicon = PhotoImage(file='list.png').subsample(5)
Tab.add(T1, text='Add expense',image=expenseicon,compound='top')
Tab.add(T2, text='Expense List',image=listicon,compound='top')

F1 = Frame(T1)

F1.place(x=100,y=50)
 
F1photo = PhotoImage(file='wallet.png').subsample(2)

logo=ttk.Label(F1,image=F1photo)
logo.pack(pady=5)

days = {'Mon':'จันทร์',
        'Tue':'อังคาร',
        'Wed':'พุธ',
        'Thu':'พฤหัส',
        'Fri':'ศุกร์',
        'Sat':'เสาร์',
        'Sun':'อาทิตย์'}

def Save(event=None):   
    expense = v_expense.get()
    price = v_price.get()
    quantity = v_quantity.get()

    if expense =='':
        print('NO Data')
        messagebox.showwarning('ERROR','กรุณากรอกข้อมูลค่าใช้จ่าย')
        return
    elif price == '':
        messagebox.showwarning('ERROR','กรุณากรอกราคา')
        return
    elif quantity == '':
        quantity = 1
        
    try:
        total = int(price) * int(quantity)
            
        print('รายการ: {} ราคา: {} '.format(expense,price,))
        print('จำนวน: {} รวมทั้งหมด: {} บาท'.format(quantity,total))
        text = 'รายการ: {} ราคา: {}\n'.format(expense,price,)
        text = text + 'จำนวน: {} รวมทั้งหมด: {} บาท'.format(quantity,total)
        v_result.set(text)
        v_expense.set('')
        v_price.set('')
        v_quantity.set('')

        today = datetime.now().strftime('%a') 
        print(today)
        dt = datetime.now().strftime('%y-%m-%d-%H:%M:%S')
        dt = days[today] + '-' + dt
        with open ('savedata.csv','a',encoding='utf-8',newline='') as f:
            fw = csv.writer(f)
            data = [dt,expense,price,quantity,total]
            fw.writerow(data)

        E1.focus()
        update_table()     
    except Exception as e:

        print('ERROR:',e)
        messagebox.showwarning('ERROR','กรุณากรอกข้อมูลใหม่ คุณกรอกข้อมูลผิด')
        v_expense.set('')
        v_price.set('')
        v_quantity.set('')

GUI.bind('<Return>',Save) #ต้องเพิ่มใน def Save(event=None) ด้วย

FONT1 = (None,20)
#---------text1---------
L = ttk.Label(F1,text='รายการค่าใช้จ่าย',font=FONT1).pack()
v_expense = StringVar()
E1 = ttk.Entry(F1,textvariable=v_expense,font=FONT1)
E1.pack()
#-----------------------
#---------text2---------
L = ttk.Label(F1,text='ราคา (บาท)',font=FONT1).pack()
v_price = StringVar()
E2 = ttk.Entry(F1,textvariable=v_price,font=FONT1)
E2.pack()
#-----------------------
#---------text3---------
L = ttk.Label(F1,text='จำนวน (ชิ้น)',font=FONT1).pack()
v_quantity = StringVar()
E3 = ttk.Entry(F1,textvariable=v_quantity,font=FONT1)
E3.pack()
#-----------------------
B2photo = PhotoImage(file='save.png').subsample(5)
B2 = ttk.Button(F1,text='Save',image=B2photo,compound='top')

B2.pack(ipadx=50,ipady=20,pady=20)

v_result = StringVar()
v_result.set('------ผลลัพธ์------')
result = ttk.Label(F1, textvariable=v_result,font=FONT1,foreground='green')
result.pack(pady=20)
#####TAB2######

def read_csv():
    with open('savedata.csv',newline='',encoding='utf-8') as f:
        fr = csv.reader(f)
        data = list(fr)
    return data
#Table

L = ttk.Label(T2,text='ตารางแสดงผลลัพท์ทั้งหมด',font=FONT1).pack(pady=20)

header = ['วัน-เวลา','รายการ','ค่าใช้จ่าย','จำนวน','รวม']
resulttable = ttk.Treeview(T2, columns=header, show='headings',height=12)
resulttable.pack()

#for i in range(len(header)):
 #   resulttable.heading(header[i],text=header[i])

for hd in header:
    resulttable.heading(hd,text=hd)
headerwidth = [150,170,80,80,80]
for hd,W in zip(header,headerwidth):
    resulttable.column(hd,width=W)

#resulttable.insert('','end',value=['จันทร์','น้ำดื่ม',30,5,150])
def update_table():
    resulttable.delete(*resulttable.get_children())

    data = read_csv()
    for d in data:
        resulttable.insert('',0,value=d)


update_table()
print('GET CHILD:',resulttable.get_children())
GUI.bind('<Tab>',lambda x: E2.focus())
GUI.mainloop()
