-- fix-anaLabDB-after-csv-import.sql
--
-- 2017-11-02  J. R. Minter
--
-- Run from the command line with:
-- sqlite3 anaLabDB.db < fix-anaLabDB-after-csv-import.sql
--

PRAGMA foreign_keys = 0;

CREATE TABLE sqlitestudio_temp_table AS SELECT *
                                          FROM samples;

DROP TABLE samples;

CREATE TABLE samples (
    Sample_ID        INTEGER PRIMARY KEY AUTOINCREMENT,
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
                        Sample_ID,
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
                    SELECT Sample_ID,
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
    Proj_ID           INTEGER PRIMARY KEY AUTOINCREMENT,
    Project_Code      TEXT,
    Project_Name      TEXT,
    Charge_No         TEXT,
    Principal_Sci_ID  TEXT,
    Project_Objective TEXT
);

INSERT INTO projects (
                         Proj_ID,
                         Project_Code,
                         Project_Name,
                         Charge_No,
                         Principal_Sci_ID,
                         Project_Objective
                     )
                     SELECT Proj_ID,
                            Project_Code,
                            Project_Name,
                            Charge_No,
                            Principal_Sci_ID,
                            Project_Objective
                       FROM sqlitestudio_temp_table;

DROP TABLE sqlitestudio_temp_table;

PRAGMA foreign_keys = 1;

PRAGMA foreign_keys = 0;

CREATE TABLE sqlitestudio_temp_table AS SELECT *
                                          FROM scientists;

DROP TABLE scientists;

CREATE TABLE scientists (
    Scientist_ID   INTEGER PRIMARY KEY,
    Scientist_Name TEXT,
    Local_ID       TEXT,
    Local_Address  TEXT,
    Local_Phone    TEXT
);

INSERT INTO scientists (
                           Scientist_ID,
                           Scientist_Name,
                           Local_ID,
                           Local_Address,
                           Local_Phone
                       )
                       SELECT Scientist_ID,
                              Scientist_Name,
                              Local_ID,
                              Local_Address,
                              Local_Phone
                         FROM sqlitestudio_temp_table;

DROP TABLE sqlitestudio_temp_table;

PRAGMA foreign_keys = 1;
