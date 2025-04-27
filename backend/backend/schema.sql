
CREATE TABLE Doctors (
    id SERIAL PRIMARY KEY,
    name VARCHAR(255),
    photo_url TEXT,
    gender VARCHAR(20),
    DOB DATE,
    primary_mobile_no VARCHAR(20),
    secondry_mobile_no VARCHAR(20),
    email VARCHAR(255),
    address TEXT
);


CREATE TABLE Patient (
    id SERIAL PRIMARY KEY,
    name VARCHAR(255),
    photo_url TEXT,
    gender VARCHAR(20),
    DOB DATE,
    primary_mobile_no VARCHAR(20),
    secondry_mobile_no VARCHAR(20),
    email VARCHAR(255),
    address TEXT,
    referred_by INTEGER REFERENCES Doctors(id) ON DELETE SET NULL,
    blood_type VARCHAR(5)
);


CREATE TABLE Appointment (
    id SERIAL PRIMARY KEY,
    patient_id INTEGER REFERENCES Patient(id) ON DELETE CASCADE,
    doctor_id INTEGER REFERENCES Doctors(id) ON DELETE CASCADE,
    timestamp TIMESTAMP
);


CREATE TABLE Inquiry_or_Request (
    id SERIAL PRIMARY KEY,
    patient_id INTEGER REFERENCES Patient(id) ON DELETE CASCADE,
    doctor_of_interest_id INTEGER REFERENCES Doctors(id) ON DELETE CASCADE,
    body TEXT,
    timestamp TIMESTAMP,
    type VARCHAR(100)
);


CREATE TABLE Medical_History (
    id SERIAL PRIMARY KEY,
    patient_id INTEGER REFERENCES Patient(id) ON DELETE CASCADE,
    history_entry TEXT
);


CREATE TABLE Family_Relatives (
    id SERIAL PRIMARY KEY,
    patient_id INTEGER REFERENCES Patient(id) ON DELETE CASCADE,
    relative_id INTEGER REFERENCES Patient(id) ON DELETE CASCADE,
    relation VARCHAR(100)
);

-- Create Group table
CREATE TABLE GroupTable ( -- "group" is a reserved word in SQL, so changed table name
    id SERIAL PRIMARY KEY,
    patient_id INTEGER REFERENCES Patient(id) ON DELETE CASCADE,
    group_name VARCHAR(255)
);


CREATE TABLE Scan (
    id SERIAL PRIMARY KEY,
    patient_id INTEGER REFERENCES Patient(id) ON DELETE CASCADE,
    scan_file_url TEXT,
    scan_date DATE,
    scan_type VARCHAR(100)
);

GRANT ALL PRIVILEGES ON SCHEMA public TO information_system_owner;

