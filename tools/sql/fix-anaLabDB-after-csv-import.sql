-- fix-anaLabDB-after-csv-import.sql
--
-- 2017-11-02  J. R. Minter
-- 2017-11-04  Change to simpler column names
-- 2017-11-19  Use some ideas from SQLiteStudio manual setup...
--
-- Run from the command line with:
-- sqlite3 anaLabDB.db < fix-anaLabDB-after-csv-import.sql
--

PRAGMA foreign_keys = 0;

CREATE TABLE sqlitestudio_temp_table AS SELECT *
                                          FROM samples;

DROP TABLE samples;

CREATE TABLE samples (
    ID              [INT AUTO_INCREMENT] PRIMARY KEY
                     UNIQUE ON CONFLICT IGNORE,
    Lab_ID           TEXT,
    Client_Sample_ID TEXT,
    Sample_Info      TEXT,
    Date_In          TEXT,
    Date_Out         TEXT,
    Project_ID       TEXT,
    Job_ID           TEXT,
    Submitter_ID     TEXT,
    Analyst_ID       TEXT,
    Hours            TEXT
);

INSERT INTO samples (
                        ID,
                        Lab_ID,
                        Client_Sample_ID,
                        Sample_Info,
                        Date_In,
                        Date_Out,
                        Project_ID,
                        Job_ID,
                        Submitter_ID,
                        Analyst_ID,
                        Hours
                    )
                    SELECT ID,
                           Lab_ID,
                           Client_Sample_ID,
                           Sample_Info,
                           Date_In,
                           Date_Out,
                           Project_ID,
                           Job_ID,
                           Submitter_ID,
                           Analyst_ID,
                           Hours
                      FROM sqlitestudio_temp_table;

DROP TABLE sqlitestudio_temp_table;

PRAGMA foreign_keys = 1;



PRAGMA foreign_keys = 0;

CREATE TABLE sqlitestudio_temp_table AS SELECT *
                                          FROM projects;

DROP TABLE projects;

CREATE TABLE projects (
    ID       [INT AUTO_INCREMENT] PRIMARY KEY
              UNIQUE ON CONFLICT IGNORE,
    Code      TEXT,
    Name      TEXT,
    Charge_No         TEXT,
    Manager_ID  TEXT,
    Objective TEXT
);

INSERT INTO projects (
                         ID,
                         Code,
                         Name,
                         Charge_No,
                         Manager_ID,
                         Objective
                     )
                     SELECT ID,
                            Code,
                            Name,
                            Charge_No,
                            Manager_ID,
                            Objective
                       FROM sqlitestudio_temp_table;

DROP TABLE sqlitestudio_temp_table;

PRAGMA foreign_keys = 1;

PRAGMA foreign_keys = 0;

CREATE TABLE sqlitestudio_temp_table AS SELECT *
                                          FROM people;

DROP TABLE people;

CREATE TABLE people (
    ID        [INT AUTO_INCREMENT] PRIMARY KEY
              UNIQUE ON CONFLICT IGNORE,
    Name      TEXT,
    Local_ID  TEXT,
    Address   TEXT,
    Phone     TEXT
);

INSERT INTO people (
                           ID,
                           Name,
                           Local_ID,
                           Address,
                           Phone
                       )
                       SELECT ID,
                              Name,
                              Local_ID,
                              Address,
                              Phone
                         FROM sqlitestudio_temp_table;

DROP TABLE sqlitestudio_temp_table;

PRAGMA foreign_keys = 1;
