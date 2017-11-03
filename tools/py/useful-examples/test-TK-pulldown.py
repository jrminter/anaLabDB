"""
test-TK-pulldown.py

A test of a pulldown menu adapted from
https://pythonspot.com/en/tk-dropdown-example/

"""

from tkinter import *
import sqlite3
import sys
import string
import os

# instance = "anaLabDBprod"
instance = "anaLabDBtest"

dbRoot = os.getenv("ANA_DB_DIR")
wrkDir = dbRoot + '/' + instance
anaLabDB = wrkDir + '/anaLabDB.db'

queryProjectsString = "SELECT Project_Name FROM projects;"
queryClientString = "SELECT Scientist_Name FROM scientists;"

# initialize the project set
projChoices = set()
con = sqlite3.connect(anaLabDB)
cur = con.cursor()
cur.execute(queryProjectsString)
while (1):
	x = cur.fetchone()
	if x == None: break
	projChoices.add(x)
cur.close()
con.close()

# initialize the people set
clientChoices = set()
con = sqlite3.connect(anaLabDB)
cur = con.cursor()
cur.execute(queryClientString)
while (1):
	x = cur.fetchone()
	if x == None: break
	clientChoices.add(x)
cur.close()
con.close()
 
root = Tk()
root.title("Tk dropdown example")
 
# Add a grid
mainframe = Frame(root)
mainframe.grid(column=0,row=0, sticky=(N,W,E,S) )
mainframe.columnconfigure(0, weight = 1)
mainframe.rowconfigure(0, weight = 1)
mainframe.pack(pady = 100, padx = 100)
 
# Create a Tkinter variable
tkStrProj = StringVar(root)
tkStrClient = StringVar(root)
 
# Dictionary with options
tkStrProj.set('Pick One') # set the default option
tkStrClient.set('Pick One') # set the default option
 
popupMenuProj = OptionMenu(mainframe, tkStrProj, *projChoices)
Label(mainframe, text="Choose a project").grid(row = 1, column = 1)
popupMenuProj.grid(row = 2, column =1)
popupMenuClient = OptionMenu(mainframe, tkStrClient, *clientChoices)
Label(mainframe, text="Choose a Client").grid(row = 3, column = 1)
popupMenuClient.grid(row = 24, column =1)
 
# on change dropdown value
def change_proj_dropdown(*args):
	res = tkStrProj.get()
	res = res.replace('(', "")
	res = res.replace(')', "")
	res = res.replace(',', "")
	print(res)
 
# link function to change dropdown
tkStrProj.trace('w', change_proj_dropdown)



# on change dropdown value
def change_client_dropdown(*args):
	res = tkStrClient.get()
	res = res.replace('(', "")
	res = res.replace(')', "")
	res = res.replace(',', "")
	print(res)

# link function to change dropdown
tkStrClient.trace('w', change_client_dropdown)
 
root.mainloop()