import getpass
import sqlite3
import pyzbar.pyzbar as pyzbar
import pyqrcode
import cv2
import os
import pywhatkit
import hashlib
import win10toast
from win10toast import ToastNotifier
import colorama 
from colorama import Back, Style
colorama.init(autoreset=True)

#----------For Notification after Successfull scan of QR-------
Notify = ToastNotifier()

#------ScanningFromWebCamera---------------------
def scan():
	i = 0
	cap = cv2.VideoCapture(0,cv2.CAP_DSHOW)
	font = cv2.FONT_HERSHEY_PLAIN
	while i<1:		
		ret, frame=cap.read()
		decode = pyzbar.decode(frame)
		for obj in decode:
			name=obj.data
			name2= name.decode()
			nn,ii,pp,dd = name2.split(' ')
			db = sqlite3.connect('StudentDatabase.db')
			c = db.cursor()
			c.execute('''CREATE TABLE IF NOT EXISTS Record(name TEXT, iid TEXT,phone_no TEXT, dept TEXT, TimeofMArk TIMESTAMP DEFAULT CURRENT_TIMESTAMP NOT NULL )''')
			c.execute("INSERT INTO Record(name, iid, phone_no, dept) VALUES (?,?,?,?)", (nn,ii,pp,dd))
			db.commit()
#database portions--------------------------------
			i=i+1
		cv2.imshow("QRCode",frame)
		cv2.waitKey(2)
	cap.release()
	Notify.show_toast("QRAS","Attendance is marked successfully!")
	cv2.destroyAllWindows()


#------CreateDatabaseForStudent------------------
def database():
	conn = sqlite3.connect('StudentDatabase.db')
	c = conn.cursor()
	c.execute("CREATE TABLE IF NOT EXISTS all_record(student_name TEXT, student_id TEXT, student_contact, student_department TEXT)")
	conn.commit()
	conn.close()
database()


#-------------------------FunctionsForGettingInputWithValidation------------------
def getName():
	global S_name
	S_name = input("Please enter Student Name\n")
	while not S_name.isalpha():
		print("Please enter valid Student Name")
		S_name = input()
	return (S_name)

def getContact():
	global S_contac
	S_contac = input("Please enter Student Contact No\n")
	while not S_contac.isnumeric(): 
		print("Please enter valid Student Contact No")
		S_contac = input()
	return int(S_contac)

    
#------AddingNewUsers/Student---------------------
def add_User():
	Li = []
    # S_name=str(input("Please Enter Student Name\n"))
	getName()
	S_id=str(input("Please Enter Student Id\n"))
	# S_contac= input("Please enter Student Contact No\n")
	getContact()
	S_dept= input("Please enter Student Department\n")
	Li.extend((S_name,S_id,S_contac,S_dept))
#-----using List Compression to convert a list to str--------------
	listToStr = ' '.join([str(elem) for elem in Li])
	#print(listToStr)
	print(Back.YELLOW + "Please Verify the Information")
	print("Student Name       = "+ S_name)
	print("Student ID         = "+ S_id)
	print("Student Contact    = "+ S_contac)
	print("Student Department = "+ S_dept)
	input("Press Enter to continue or CTRL+C to Break Operation")
	conn = sqlite3.connect('StudentDatabase.db')
	c = conn.cursor()
	c.execute("INSERT INTO all_record(student_name, student_id, student_contact, student_department) VALUES (?,?,?,?)", (S_name,S_id,S_contac,S_dept))
	conn.commit()
	conn.close()
	qr= pyqrcode.create(listToStr)
	if not os.path.exists('./QrCodes'):
		os.makedirs('./QRCodes')
	qr.png("./QRCodes/" +S_name+ ".png",scale=8)
	pywhatkit.sendwhats_image("+91"+S_contac+"", "./QRCodes/" +S_name+ ".png",""+S_name+"")


#--------------ViewDatabase------------------------
def viewdata():
	conn = sqlite3.connect('StudentDatabase.db')
	c = conn.cursor()
	c.execute("SELECT * FROM Record")
	rows = c.fetchall()
	for row in rows:
		print(row)
	conn.close()


#----------AdminScreen-----------------------
def afterlogin():
	print(Back.MAGENTA+"     Admin Menu     ")
	print("+------------------------------+")
	print("|  1- Add New Student          |")
	print("|  2- View Record              |")
	print("+------------------------------+")
	user_input = input("")
	if user_input == '1':
		add_User()

	if user_input == '2':
		viewdata()
    

#login----------------------------------------------------------

# def signup():
# 	print(Back.BLUE+"     Signup     ")
# 	email = input("Enter email address: ")
# 	pwd = getpass.getpass(prompt = 'Enter the password: ')
# 	conf_pwd = getpass.getpass(prompt = 'Confirm password: ')
    
# 	if conf_pwd == pwd:
# 		enc = conf_pwd.encode()
# 		hash1 = hashlib.sha256(enc).hexdigest()
# 		with open("credentials.txt", "w") as f:
# 			f.write(email + "\n")
# 			f.write(hash1)
# 		f.close()
			
# 		print("You have registered successfully!")
		
# 	else:
# 		print("Password is not same as above!\n")


def login():
	print(Back.BLUE+"     Login     ")
	id = input("Enter the id: ")
	pwd = getpass.getpass(prompt = 'Enter the password: ')
	auth = pwd.encode()
	auth_hash = hashlib.sha256(auth).hexdigest()
	with open("credentials.txt", "r") as f:
		stored_id, stored_pwd = f.read().split("\n")
	f.close()
	if id == stored_id and auth_hash == stored_pwd:
		print("Logged in Successfully!")
		afterlogin()

	else:
		print("Login failed! \n")



#-------MainPage----------------------------
def markattendance():
	print(Back.GREEN+" QR Code based Attendace System ")
	print("+------------------------------+")
	print("|  1- Mark Attendance          |")
	print("|  2- Admin Login              |")
	print("+------------------------------+")
	user_input2 = input("")
	if user_input2 == '1':
		scan()
	if user_input2 == '2':
		login()
markattendance()