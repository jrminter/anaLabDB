# -*- coding: utf-8 -*-
"""
create-anaLabDB-from-csv.py

Create the anaLabDB sqlite3 database from csv files.
We use an environment variable (ANA_DB_DIR) to specify
the base path for databases. We can have test and production
instances. This script ASSUMES these directories exist and
have the needed .csv files...

execute with:

python create-anaLabDB-from-csv.py

  Date      who   ver   Comment
----------  ---  -----  ----------------------------------------
2017-11-02  JRM  0.0.1  Initial

"""

import sqlite3
import pandas
import os

# instance = "anaLabDBprod"
instance = "anaLabDBtest"

dbRoot = os.getenv("ANA_DB_DIR")
wrkDir = dbRoot + '/' + instance
anaLabDB = wrkDir + '/anaLabDB.db'



print(anaLabDB)
con = sqlite3.connect(anaLabDB)

csvFil = wrkDir + '/csv/samples.csv'
df = pandas.read_csv(csvFil)
print(df.tail())
df.to_sql('samples', con, if_exists='replace', index=False)

csvFil = wrkDir + '/csv/projects.csv'
df = pandas.read_csv(csvFil)
print(df.tail())
df.to_sql('projects', con, if_exists='replace', index=False)

csvFil = wrkDir + '/csv/scientists.csv'
df = pandas.read_csv(csvFil)
print(df.tail())
df.to_sql('scientists', con, if_exists='replace', index=False)

con.close()
