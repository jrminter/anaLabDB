#!/usr/bin/env python

"""
012345678901234567890123456789012345678901234567890123456789012345679012

anaLabDB Sample Manager Python 3.6 Version
Needs sqlite3

License: GPL (>=2) | BSD

J. R. Minter

   Date	 Version					 Comments
----------  -------  ---------------------------------------------------
2017-11-03   0.1.00  Port to sqlite3 and better handling of the query
                     strings. To Do: need to move database calls into
                     functions or perhaps a package. drop down menus
                     would be helpful.
"""

from tkinter import *
from tkinter import filedialog as fd
import sqlite3
import sys
import string
import os
import configparser



# instance = "anaLabDBprod"
instance = "anaLabDBtest"

dbRoot = os.getenv("ANA_DB_DIR")
wrkDir = dbRoot + '/' + instance
anaLabDB = wrkDir + '/anaLabDB.db'
iniDir = wrkDir + '/ini'


# Update samples query string

updateSampleQueryString = """
UPDATE samples
SET Client_Sample_ID = '%s',
Sample_Info = '%s',
Date_In = '%s',
Date_Out = '%s',
Project_ID = '%s',
Job_ID = '%s',
Submitter_ID = '%s',
Analyst_ID = '%s',
Hours = '%s'
WHERE LAB_ID='%s';
"""

# get num samples query 
getNumSamplesQueryString = "SELECT count(*) FROM samples"

# Insert sample query string

insertSampleQueryString = """
INSERT INTO
samples (ID, Lab_ID, Client_Sample_ID,
		 Sample_Info, Date_In, Date_Out, Project_ID,
		 Job_ID, Submitter_ID, Analyst_ID, Hours)
VALUES (NULL, '%s', '%s',
		'%s', '%s', '%s', '%s',
		'%s', '%s', '%s', '%s');
"""

# sample query string
queryAllSamplesLabIDString = "SELECT * FROM samples WHERE LAB_ID = '%s'"

# logout (set date) string
logOutSampleWithLabIDString ="""
UPDATE samples
SET Date_Out='%s'
WHERE Lab_ID = '%s'
"""

# logout (query date) string
loggedOutSamplesWithLabIDString = """
SELECT Lab_ID, Client_Sample_ID, Date_Out
FROM samples
WHERE Lab_ID = '%s';
"""



print(anaLabDB)
con = sqlite3.connect(anaLabDB)


con.close()

class App:
	def __init__(self,parent):
		# define the variables
		self.mVerbose = IntVar()
		# variables changed from year-to-year
		# nOffset = 5100 for 2017  for MIDB, 
		# The toy data set uses an offset 1000
		self.mOffset = 1000
		# If one deletes a record from the database, things get
		# messed up. Increment this by one. Zero when you redo the
		# database each year...
		self.mFudge = 0
		self.mStart = 'qm-0'
		self.manaLabDBKey = StringVar()
		self.mLabID = StringVar()
		self.mAnalyst_ID = StringVar()
		self.mSubmitter_ID = StringVar()
		self.mProject_ID = StringVar()
		self.mJob_ID = StringVar()
		self.mClient_Sample_ID = StringVar()
		self.mSample_Info = StringVar()
		self.mDate_In = StringVar()
		self.mDate_Out = StringVar()
		self.mMessage = StringVar()
		self.mHours = StringVar()
		
		# initialize variables
		self.manaLabDBKey.set("1")
		self.mHours.set("4")
		self.mMessage.set("Message")
		
		f = Frame(parent)
		f.pack(padx=15,pady=15)
		#we then create an entry widget,pack it and then 
		#create two more button widgets as children to the frame.
		self.lab0 = Label(f, text='anaLabDB Key')
		self.lab0.pack(side = TOP, pady=1)
		self.anaLabDBKeyBox = Entry(f,textvariable=self.manaLabDBKey,
			width=12)
		self.anaLabDBKeyBox.pack(side= TOP,padx=10,pady=2)
		self.lab1 = Label(f, text='Lab ID')
		self.lab1.pack(side = TOP, pady=1)
		self.LabIdBox = Entry(f,textvariable=self.mLabID, width=12)
		self.LabIdBox.pack(side= TOP,padx=10,pady=2)
			
		self.lab2 = Label(f, text='Analyst ID')
		self.lab2.pack(side = TOP, pady=1)
		self.AnalystIdBox = Entry(f,textvariable=self.mAnalyst_ID,
			width=12)
		self.AnalystIdBox.pack(side= TOP,padx=10,pady=2)
			
		self.lab3 = Label(f, text='Project ID')
		self.lab3.pack(side = TOP, pady=1)
		self.ProjectIdBox = Entry(f,textvariable=self.mProject_ID,
			width=12)
		self.ProjectIdBox.pack(side= TOP,padx=10,pady=2)
			
		self.lab4 = Label(f, text='Job ID')
		self.lab4.pack(side = TOP, pady=1)
		self.JobIdBox = Entry(f,textvariable=self.mJob_ID, width=12)
		self.JobIdBox.pack(side= TOP,padx=10,pady=2)

		self.lab5 = Label(f, text='Client ID')
		self.lab5.pack(side = TOP, pady=1)
		self.ClientIdBox = Entry(f,textvariable=self.mSubmitter_ID,
			width=12)
		self.ClientIdBox.pack(side= TOP,padx=10,pady=2)
			
		self.lab6 = Label(f, text='Client Sample ID')
		self.lab6.pack(side = TOP, pady=1)
		self.ClientSampleIdBox = Entry(f,
			textvariable=self.mClient_Sample_ID,width=50)
		self.ClientSampleIdBox.pack(side= TOP,padx=10,pady=2)
			
		self.lab7 = Label(f, text='Sample Description')
		self.lab7.pack(side = TOP, pady=1)
		self.ClientSampleInfoBox = Entry(f,
			textvariable=self.mSample_Info, width=50)
		self.ClientSampleInfoBox.pack(side= TOP,padx=10,pady=2)
			
		self.lab8 = Label(f, text='Date In')
		self.lab8.pack(side = TOP, pady=1)
		self.DateInBox = Entry(f,textvariable=self.mDate_In, width=12)
		self.DateInBox.pack(side= TOP,padx=10,pady=2)
			
		self.lab9 = Label(f, text='Date Out')
		self.lab9.pack(side = TOP, pady=1)
		self.DateOutBox = Entry(f,textvariable=self.mDate_Out, width=12)
		self.DateOutBox.pack(side= TOP,padx=10,pady=2)

		self.lab10 = Label(f, text='Hours')
		self.lab10.pack(side = TOP, pady=1)
		self.HoursBox = Entry(f,textvariable=self.mHours, width=12)
		self.HoursBox.pack(side= TOP,padx=10,pady=2)
		
		self.cb = Checkbutton(f, text="Debug Info", variable=self.mVerbose)
		self.cb.pack(side = TOP, pady=1)
		
		# message box
		self.lab11 = Label(f, text='')
		self.lab11.pack(side = TOP, pady=1)
		self.lab12 = Label(f, text='Messages')
		self.lab12.pack(side = TOP, pady=2)
		self.MessageBox = Entry(f,textvariable=self.mMessage, width=50)
		self.MessageBox.pack(side= TOP,padx=10,pady=2)
		
		# this time, we pass a number of options to the
		# constructor, as keyword arguments. The first button
		# is labeled "exit"and the second is labeled "Hello". 
		# Both buttons also take a command option. This option 
		# specifies a function, or (as in this
		# case) a bound method, which will be called when the button is clicked.
			
		self.button = Button(f, text="LogIn",command=self.log_in)
		self.button.pack(side=LEFT,padx=2,pady=10)
			
		self.button = Button(f, text="LogOut",command=self.log_out)
		self.button.pack(side=LEFT,padx=2,pady=10)
			
		self.button = Button(f, text="Query DB",command=self.query_db)
		self.button.pack(side=LEFT,padx=2,pady=10)
			
		self.button = Button(f, text="write file",command=self.write_file)
		self.button.pack(side=LEFT,padx=2,pady=10)
			
		self.button = Button(f, text="read file",command=self.read_file)
		self.button.pack(side=LEFT,padx=2,pady=10)
			
		self.button = Button(f, text="update sample",command=self.update_sample)
		self.button.pack(side=LEFT,padx=2,pady=10)

		self.exit = Button(f, text="exit", command=f.quit)
		self.exit.pack(side=LEFT,padx=2,pady=10)
		
		# pull in last data
		self.ReadLast()

	def isDebugChecked(self):
		val = self.mVerbose.get()
		if val > 0:
			return(True)
		else:
			return(False)


	def log_in(self):

		bDebug = self.isDebugChecked()
		# see
		# http://dev.mysql.com/doc/connector-python/en/myconnpy_tutorial_CursorBuffered_GiveRaise.html
		cnx = sqlite3.connect(anaLabDB)
		curQ = cnx.cursor()
		curQ.execute(getNumSamplesQueryString)
		while (1):
			x = curQ.fetchone()
			if x == None: break
			nCount = int(x[0])

			if(bDebug):
				print(nCount)

			strLabID = self.mStart + str(self.mOffset + nCount + 1)
			self.mLabID.set(strLabID)

			query = insertSampleQueryString % ( self.mLabID.get(),
						self.mClient_Sample_ID.get(),
						self.mSample_Info.get(),
						self.mDate_In.get(),
						self.mDate_Out.get(),
						self.mProject_ID.get(),
						self.mJob_ID.get(),
						self.mSubmitter_ID.get(),
						self.mAnalyst_ID.get(),
					 	self.mHours.get()
					)
			if(bDebug):
				print(query)
			cursor = cnx.cursor()
			cursor.execute(query)
			cursor.execute("commit;")

			if(bDebug):
				print(query)
			cursor.close()
			cursor = cnx.cursor()
			strCheck = "SELECT * FROM samples WHERE LAB_ID = '"
			strCheck = strCheck + self.mLabID.get()
			strCheck = strCheck + "'"
			cursor.execute(strCheck)
			while (1):
				row = cursor.fetchone ()
				if row == None: break
				self.manaLabDBKey.set(str(row[0]))
				self.mLabID.set(str(row[1]))
				self.write_last()
				strMsg = str("Logged in Lab ID " + self.mLabID.get())
				self.mMessage.set(strMsg)
		curQ.close()
		cursor.close()
		cnx.close()
		self.write_last()
		if(bDebug):
			print(strCheck)

	def log_out(self):
		bDebug = self.isDebugChecked()
		# strCheck = "SELECT * FROM samples WHERE LAB_ID = '%s'"
		# self.mLabID.get()
		query = queryAllSamplesLabIDString % (self.mLabID.get())
		if(bDebug):
			print("Logout: Query All samples with Log ID")
			print(query)

		cnx = sqlite3.connect(anaLabDB)
		cursor = cnx.cursor()
		# cursor.execute(strCheck, self.mLabID.get())
		cursor.execute(query)
		for x in cursor:
		# Iterate through all samples with the same LAB_ID 
			if(bDebug):
				print(x[1])
			query = logOutSampleWithLabIDString % (self.mDate_Out.get(),
												   self.mLabID.get())
			if(bDebug):
				print("logOutSampleWithLab Query")
				print(query)
			cur = cnx.cursor()
			cur.execute(query)

			query = loggedOutSamplesWithLabIDString % (self.mLabID.get())
			if(bDebug):
				print("loggedOutSamplesWithLabID")
				print(query)
			cur.execute(query)
			for y in cur:
				strMsg = str("Logged out Lab ID " + y[0])
				self.mMessage.set(strMsg)
			cursor.execute("commit;")
			cur.close()
		cursor.close()
		cnx.close()

	def update_sample(self):
		bDebug = self.isDebugChecked()
		query = updateSampleQueryString % (
			self.mClient_Sample_ID.get(),
			self.mSample_Info.get(),
			self.mDate_In.get(),
            self.mDate_Out.get(),
			self.mProject_ID.get(),
			self.mJob_ID.get(),
			self.mSubmitter_ID.get(),
			self.mAnalyst_ID.get(),
			self.mHours.get(),
			self.mLabID.get()
			)
		print("Update Sample Query")
		print(query)
		cnx = sqlite3.connect(anaLabDB)
		cursor = cnx.cursor()
		cursor.execute(query)
		cursor.execute("commit;")
		cursor.close()
		cnx.close()
		strMsg = str("Updated Lab ID " + self.mLabID.get())
		self.mMessage.set(strMsg)
		self.write_last()


	def query_db(self):

		bDebug = self.isDebugChecked()

		cnx = sqlite3.connect(anaLabDB)
		cursor = cnx.cursor()

		query = queryAllSamplesLabIDString % (self.mLabID.get())
		if(bDebug):
			print("Logout: Query All samples with Log ID")
			print(query)
		
		cursor.execute(query)


		iVal = 0
		if(bDebug):
			for x in cursor:
				print(x[0])
				print(x[1])
				print(x[2])
				print(x[3])
				print(x[4])
				print(x[5])
				print(x[6])
				print(x[7])
				print(x[8])
				print(x[9])
				print(x[10])
			
		for x in cursor:
			iVal += 1
			self.manaLabDBKey.set(x[0])
			self.mLabID.set(x[1])
			self.mClient_Sample_ID.set(x[2])
			self.mSample_Info.set(x[3])
			self.mDate_In.set(x[4])
			self.mDate_Out.set(x[5])
			self.mProject_ID.set(x[6])
			self.mJob_ID.set(x[7])
			self.mSubmitter_ID.set(x[8])
			self.mAnalyst_ID.set(x[9])
			self.mHours.set(x[10])
			strMsg = "Queried sample %s" % (self.mLabID.get())
			self.mMessage.set(strMsg)
		if (iVal < 1):
			self.mMessage.set("No results returned...")
		cursor.close()
		cnx.close()



	def write_file(self):
		strOutFile = fd.asksaveasfilename(initialdir=iniDir,
										  filetypes= [("ini files",
													   "*.ini")])
		if strOutFile == "": return
		config = configparser.ConfigParser()
		config.add_section('LAST')
		config['LAST']['manaLabDBKey'] = self.manaLabDBKey.get()
		config['LAST']['mLabID'] = self.mLabID.get()
		config['LAST']['mClient_Sample_ID'] = self.mClient_Sample_ID.get()
		config['LAST']['mSample_Info'] = self.mSample_Info.get()
		config['LAST']['mDate_In'] = self.mDate_In.get()
		config['LAST']['mDate_Out'] = self.mDate_Out.get()
		config['LAST']['mProject_ID'] = self.mProject_ID.get()
		config['LAST']['mJob_ID'] = self.mJob_ID.get()
		config['LAST']['mSubmitter_ID'] = self.mSubmitter_ID.get()
		config['LAST']['mAnalyst_ID'] = self.mAnalyst_ID.get()
		with open(strOutFile, 'w') as configfile:		# save
			config.write(configfile)

	def write_last(self):
		strFile = '/data/anaLabDB/last_sample.ini'
		config = configparser.ConfigParser()
		config.add_section('LAST')
		config['LAST']['manaLabDBKey'] = self.manaLabDBKey.get()
		config['LAST']['mLabID'] = self.mLabID.get()
		config['LAST']['mClient_Sample_ID'] = self.mClient_Sample_ID.get()
		config['LAST']['mSample_Info'] = self.mSample_Info.get()
		config['LAST']['mDate_In'] = self.mDate_In.get()
		config['LAST']['mDate_Out'] = self.mDate_Out.get()
		config['LAST']['mProject_ID'] = self.mProject_ID.get()
		config['LAST']['mJob_ID'] = self.mJob_ID.get()
		config['LAST']['mSubmitter_ID'] = self.mSubmitter_ID.get()
		config['LAST']['mAnalyst_ID'] = self.mAnalyst_ID.get()
		with open(strFile, 'w') as configfile:		# save
			config.write(configfile)

	def read_file(self):
		self.mMessage.set("")
		strInFile = fd.askopenfilename(initialdir=iniDir,
									   filetypes= [("ini files",
													"*.ini")])
		if strInFile == "": return
		config = configparser.ConfigParser()
		config.read(strInFile)
		self.manaLabDBKey.set(config['LAST']['manaLabDBKey'])
		self.mLabID.set(config['LAST']['mLabID'])
		self.mClient_Sample_ID.set(config['LAST']['mClient_Sample_ID'])
		self.mSample_Info.set(config['LAST']['mSample_Info'])
		self.mDate_In.set(config['LAST']['mDate_In'])
		self.mDate_Out.set(config['LAST']['mDate_Out'])
		self.mProject_ID.set(config['LAST']['mProject_ID'])
		self.mJob_ID.set(config['LAST']['mJob_ID'])
		self.mSubmitter_ID.set(config['LAST']['mSubmitter_ID'])
		self.mAnalyst_ID.set(config['LAST']['mAnalyst_ID'])

	def ReadLast(self):
		self.mMessage.set("")
		strFile = iniDir + '/last_sample.ini'
		config = configparser.ConfigParser()
		config.read(strFile)
		self.manaLabDBKey.set(config['LAST']['manaLabDBKey'])
		self.mLabID.set(config['LAST']['mLabID'])
		self.mClient_Sample_ID.set(config['LAST']['mClient_Sample_ID'])
		self.mSample_Info.set(config['LAST']['mSample_Info'])
		self.mDate_In.set(config['LAST']['mDate_In'])
		self.mDate_Out.set(config['LAST']['mDate_Out'])
		self.mProject_ID.set(config['LAST']['mProject_ID'])
		self.mJob_ID.set(config['LAST']['mJob_ID'])
		self.mSubmitter_ID.set(config['LAST']['mSubmitter_ID'])
		self.mAnalyst_ID.set(config['LAST']['mAnalyst_ID'])
		
		
	
root = Tk()
root.title('anaLabDB Sqlite3 Sample Manager v. 0.2.0')
app = App(root)

root.mainloop()



