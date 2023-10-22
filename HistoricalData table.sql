CREATE TABLE HistoricalData (
    Date DATE,
    DepTime TIME,
    ArrTime TIME,
    UniqueCarrier VARCHAR(255),
    FlightNum VARCHAR(10)
);

INSERT INTO YourTableName (Date, DepTime, ArrTime, UniqueCarrier, FlightNum) VALUES (?, ?, ?, ?, ?)

