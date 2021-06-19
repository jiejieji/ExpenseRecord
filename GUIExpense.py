from tkinter import *
from tkinter import ttk, messagebox
import csv
from datetime import datetime 
GUI = Tk()
GUI.title('โปรแกรมบันทึกค่าใช้จ่าย')
# GUI.geometry('720x700+500+50')

w = 720
h = 700

ws = GUI.winfo_screenwidth() #screen width
hs = GUI.winfo_screenheight() #screen height


x = (ws/2) - (w/2)
y = (hs/2) - (h/2) - 70

GUI.geometry(f'{w}x{h}+{x:.0f}+{y:.0f}')


##########MENU###########
menubar = Menu(GUI)
GUI.config(menu=menubar)

#file menu 

filemenu = Menu(menubar,tearoff=0)
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
def Donate():
	 messagebox.showinfo('Donate','BCH Address: xr1234')
donatemenu = Menu(menubar,tearoff=0)
menubar.add_cascade(label='Donate',menu=donatemenu)
donatemenu.add_command(label='Donate',command=Donate)

########################

Tab = ttk.Notebook(GUI)
T1 = Frame(Tab) 
T2 = Frame(Tab)
Tab.pack(fill=BOTH, expand=1)

expenseicon = PhotoImage(file='cash.png').subsample(5)
listicon = PhotoImage(file='list.png').subsample(1)
Tab.add(T1, text='Add expense',image=expenseicon,compound='top')
Tab.add(T2, text='Expense List',image=listicon,compound='top')

F1 = Frame(T1)

F1.place(x=200,y=50)
 
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
		stamp = datetime.now()
		dt = stamp.now().strftime('%Y-%m-%d %H:%M:%S')
		transactionid = stamp.strftime('%Y%m%d%H%M%f')
		dt = days[today] + '-' + dt
		with open ('savedata.csv','a',encoding='utf-8',newline='') as f:
			fw = csv.writer(f)
			data = [transactionid,dt,expense,price,quantity,total]
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

header = ['รหัสรายการ','วัน-เวลา','รายการ','ค่าใช้จ่าย','จำนวน','รวม']
resulttable = ttk.Treeview(T2, columns=header, show='headings',height=12)
resulttable.pack()

#for i in range(len(header)):
 #   resulttable.heading(header[i],text=header[i])

for hd in header:
	resulttable.heading(hd,text=hd)
headerwidth = [120,150,170,80,80,80]
for hd,W in zip(header,headerwidth):
	resulttable.column(hd,width=W)

#resulttable.insert('','end',value=['จันทร์','น้ำดื่ม',30,5,150])
alltransaction = {}

def UpdateCSV():
	with open('savedata.csv','w',newline='',encoding='utf-8') as f:
		fw = csv.writer(f)
		data = list(alltransaction.values())
		fw.writerows(data)
		print('Table was update')
		

def DeleteRecord(event=None):
	check = messagebox.askyesno('Confirm?','คุณต้องการลบข้อมูลใช่หรือไม่?')
	print('YES/NO:',check)

	if check == True:
		print('delete')
		select = resulttable.selection()
		#print(select)
		data = resulttable.item(select)
		data = data['values']
		transactionid = data[0]
		#print(transactionid)
		#print(type(transactionid))
		del alltransaction[str(transactionid)] # delete data in dict
		#print(alltransaction)
		UpdateCSV()
		update_table()

	else:
		print('cancel')

BDelete = ttk.Button(T2,text='delete',command=DeleteRecord)
BDelete.place(x=50,y=550)
resulttable.bind('<Delete>',DeleteRecord)

def update_table():
	resulttable.delete(*resulttable.get_children())
	try:

		data = read_csv()
		for d in data:
			#creat transaction data
			alltransaction[d[0]] = d # d[0] = transactionid
			resulttable.insert('',0,value=d)
		print(alltransaction)
	except Exception as e:
		print('No File')
		print('ERROR:',e)

##########Right Click Menu##########

def EditRecord():
	POPUP = Toplevel() # คล้ายๆกับ Tk()
	POPUP.title('Edit Record') 
	POPUP.geometry('500x400')

	# GUI.geometry('720x700+500+50')
	w = 500
	h = 400

	ws = POPUP.winfo_screenwidth() #screen width
	hs = POPUP.winfo_screenheight() #screen height


	x = (ws/2) - (w/2)
	y = (hs/2) - (h/2) - 70

	POPUP.geometry(f'{w}x{h}+{x:.0f}+{y:.0f}')

	#-------text1----------
	L = ttk.Label(POPUP,text='รายการค่าใช้จ่าย',font=FONT1).pack()
	v_expense = StringVar()
	E1 = ttk.Entry(POPUP,textvariable=v_expense,font=FONT1)
	E1.pack()
	#-----------------------

	#---------text2---------
	L = ttk.Label(POPUP,text='ราคา (บาท)',font=FONT1).pack()
	v_price = StringVar()
	E2 = ttk.Entry(POPUP,textvariable=v_price,font=FONT1)
	E2.pack()
	#-----------------------

	#---------text3---------
	L = ttk.Label(POPUP,text='จำนวน (ชิ้น)',font=FONT1).pack()
	v_quantity = StringVar()
	E3 = ttk.Entry(POPUP,textvariable=v_quantity,font=FONT1)
	E3.pack()
	#-----------------------
	def Edit():
		#print(transactionid)
		#print(alltransaction)
		olddata = alltransaction[str(transactionid)]
		print('OLD:',olddata)
		v1 = v_expense.get()
		v2 = float(v_price.get())
		v3 = float(v_quantity.get())
		total = v2*v3
		newdata = [olddata[0],olddata[1],v1,v2,v3,total]
		alltransaction[str(transactionid)] = newdata
		UpdateCSV()
		update_table()
		POPUP.destroy() #สั่งปิด popup





	B2photo = PhotoImage(file='save.png').subsample(5)
	B2 = ttk.Button(POPUP,text='Save',image=B2photo,compound='top',command=Edit)

	B2.pack(ipadx=50,ipady=20,pady=20)

	v_result = StringVar()
	v_result.set('------ผลลัพธ์------')
	result = ttk.Label(F1, textvariable=v_result,font=FONT1,foreground='green')
	result.pack(pady=20)

	# get data in select record
	
	select = resulttable.selection()
	print(select)
	data = resulttable.item(select)
	data = data['values']

	print(data)
	transactionid = data[0]
	# สั่งเซ็ตค่าเก่าไว้ตรงช่องกรอก

	v_expense.set(data[2])
	v_price.set(data[3])
	v_quantity.set(data[4])

	POPUP.mainloop()



rightclick = Menu(GUI,tearoff=0)
rightclick.add_command(label='Edit',command=EditRecord)
rightclick.add_command(label='delete',command=DeleteRecord)


def menupopup(event):
	#print(event.x_root, event.y_root)
	rightclick.post(event.x_root,event.y_root)
resulttable.bind('<Button-3>',menupopup)





update_table()
print('GET CHILD:',resulttable.get_children())
GUI.bind('<Tab>',lambda x: E2.focus())
GUI.mainloop()