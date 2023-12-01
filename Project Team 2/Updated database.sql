--Create New Table
CREATE TABLE schedule (
    ID INT IDENTITY(1,1) PRIMARY KEY, -- Assuming an auto-incrementing primary key
    Airline NVARCHAR(100),
    FlightNumber NVARCHAR(20),
    Status NVARCHAR(50),
    OperatedBy NVARCHAR(100),
    DepartureDate DATE,
    DepartureTime TIME,
    ArrivalDate DATE,
    ArrivalTime TIME
);




-- Create a new table
CREATE TABLE Historical (
    Date DATE,
    DepTime TIME,
    ArrTime TIME,
    FlightNum VARCHAR(50),
    AirlineName VARCHAR(100)
);

-- Insert data from the SELECT query into the new table
INSERT INTO Historical(Date, DepTime, ArrTime, FlightNum, AirlineName)
SELECT 
    HD.Date, 
    CONVERT(TIME, HD.DepTime),
    CONVERT(TIME, HD.ArrTime), 
    HD.FlightNum, 
    A.AirlineName
FROM 
    HistoricalData HD
JOIN 
    Airlines A ON HD.UniqueCarrier = A.AirlineCode;
