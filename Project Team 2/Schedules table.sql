CREATE TABLE Schedules(
    Airline VARCHAR(255),
    FlightNumber VARCHAR(10),
    Status VARCHAR(50),
    OperatedBy VARCHAR(255),
    DepartureTime DATETIME,
    ArrivalTime DATETIME
);

INSERT INTO YourTableName (Airline, FlightNumber, Status, OperatedBy, DepartureTime, ArrivalTime)
VALUES (?, ?, ?, ?, ?, ?);
