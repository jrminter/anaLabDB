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


print(anaLabDB)
con = sqlite3.connect(anaLabDB)

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
print(query)


con.close()


