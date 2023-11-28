CREATE TABLE MasterSchema (
    ReportingYear DATE,
    MeasureUniqueIdentifier VARCHAR(255), -- assuming VARCHAR but adjust as needed
    MeasureName VARCHAR(255), 
    FieldId INT, 
    FieldName VARCHAR(255),
    FieldType VARCHAR(255),
    ResultType VARCHAR(255),
	CodeTypeID INT,
	CodeID INT,
    Code VARCHAR(255),
    CodeDescription VARCHAR(255),
    DomainName VARCHAR(255),
    DomainDescription VARCHAR(255),
    CustomerID INT,
    InsurnaceName VARCHAR(255),
    City VARCHAR(255),
    State VARCHAR(50),  -- adjust size based on standards
    ZipCode VARCHAR(10),  -- assuming US zip, adjust if needed
    Country VARCHAR(50), 
    LOBID INT,
    Star INT  -- assuming integer ratings, adjust if needed
);
