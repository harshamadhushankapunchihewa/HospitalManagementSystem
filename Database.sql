CREATE DATABASE DATABASE8;
GO

USE DATABASE8;
GO

CREATE TABLE RFIDTag (
    RID VARCHAR(10) PRIMARY KEY
);


CREATE TABLE RFIDScanner (
    RFIDS VARCHAR(20) PRIMARY KEY
);

CREATE TABLE Room (
    RoomID INT PRIMARY KEY
);

CREATE TABLE RoomRFID (
    RoomID INT,
    RFIDS VARCHAR(20),
	NextRoom INT,
    FOREIGN KEY (RoomID) REFERENCES Room (RoomID),
    FOREIGN KEY (RFIDS) REFERENCES RFIDScanner (RFIDS)
);

CREATE TABLE SecurityTbl (
    SecID INT PRIMARY KEY,
    SecName VARCHAR(50),
    RID VARCHAR(10),
    FOREIGN KEY (RID) REFERENCES RFIDTag (RID)
);

CREATE TABLE AdminTbl (
    AdmID INT PRIMARY KEY,
    AdmName VARCHAR(50),
    RID VARCHAR(10),
    FOREIGN KEY (RID) REFERENCES RFIDTag (RID)
);

CREATE TABLE Doctor (
    DID INT PRIMARY KEY,
    DName VARCHAR(50),
    Speciality VARCHAR(50),
    RID VARCHAR(10),
    FOREIGN KEY (RID) REFERENCES RFIDTag (RID)
);

CREATE TABLE Patient (
    PID INT PRIMARY KEY,
    PName VARCHAR(50),
    Condition VARCHAR(50),
	gender VARCHAR(5),
	age INT,
    RoomID INT,
    RID VARCHAR(10),
    FOREIGN KEY (RoomID) REFERENCES Room (RoomID),
    FOREIGN KEY (RID) REFERENCES RFIDTag (RID)
);

CREATE TABLE Visitor (
    VID INT PRIMARY KEY,
    VName VARCHAR(50),
    VAddress VARCHAR(50),
    RID VARCHAR(10),
    PID INT,
    RoomID INT,
    FOREIGN KEY (RID) REFERENCES RFIDTag (RID),
    FOREIGN KEY (PID) REFERENCES Patient (PID),
    FOREIGN KEY (RoomID) REFERENCES Room (RoomID)
);

CREATE TABLE DoctorRoom (
    DID INT,
    RoomID INT,
    FOREIGN KEY (RoomID) REFERENCES Room (RoomID),
    FOREIGN KEY (DID) REFERENCES Doctor (DID)
);

CREATE TABLE PatientDoctor (
    PID INT,
    DID INT,
    FOREIGN KEY (PID) REFERENCES Patient (PID),
    FOREIGN KEY (DID) REFERENCES Doctor (DID)
);

CREATE Table TimestampTbl (
    TID INT NOT NULL IDENTITY(1,1) PRIMARY KEY,
    TimeIn DATETIME,
    CurrentRoom INT,
	TIMESTAMP,
    RID VARCHAR(10),
    FOREIGN KEY (RID) REFERENCES RFIDTag (RID)
);

CREATE TABLE AllowedRoom (
	RID VARCHAR(10),
	AllowedRooms INT
);

-- Insert values into RFIDTag table
INSERT INTO RFIDTag (RID) VALUES
('RFID1'),
('RFID2'),
('RFID3'),
('RFID4'),
('RFID5');

-- Insert values into RFIDScanner table
INSERT INTO RFIDScanner (RFIDS) VALUES
('192.168.1.4'),
('192.168.1.5');

-- Insert values into Room table
INSERT INTO Room (RoomID) VALUES
(101),
(102);

-- Insert values into RoomRFID table
INSERT INTO RoomRFID (RoomID, RFIDS, NextRoom) VALUES
(101, '192.168.1.4', 102),
(102, '192.168.1.4', 101),
(102, '192.168.1.5', 103);


-- Insert values into SecurityTbl table
INSERT INTO SecurityTbl (SecID, SecName, RID) VALUES
(1, 'Harsha', 'RFID1');


-- Insert values into AdminTbl table
INSERT INTO AdminTbl (AdmID, AdmName, RID) VALUES
(1, 'Kisara', 'RFID2');


-- Insert values into Doctor table
INSERT INTO Doctor (DID, DName, Speciality, RID) VALUES
(1, 'Angelo', 'General', 'RFID3');


-- Insert values into Patient table
INSERT INTO Patient (PID, PName, Condition, gender, age, RoomID, RID) VALUES
(1, 'Tharindu', 'flu', 'Male', 24, 101, 'RFID4');


-- Insert values into Visitor table
INSERT INTO Visitor (VID, VName, VAddress, RID, PID, RoomID) VALUES
(1, 'Venuja', 'No.9,Colombo', 'RFID5', 1, 101);

-- Insert values into DoctorRoom table
INSERT INTO DoctorRoom (DID, RoomID) VALUES
(1, 101);

-- Insert values into PatientDoctor table
INSERT INTO PatientDoctor (PID, DID) VALUES
(1, 1);


-- Insert values into TimestampTbl table
INSERT INTO TimestampTbl (TimeIn, CurrentRoom, RID) VALUES
('2023-10-06 08:00:00', 101, 'RFID1'),
('2023-10-06 09:30:00', 102, 'RFID2');

-- Insert values into AllowedRoom table
INSERT INTO AllowedRoom (RID, AllowedRooms) VALUES
('RFID1', 101),
('RFID1', 102),
('RFID2', 101),
('RFID3', 102);