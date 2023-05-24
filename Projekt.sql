CREATE TABLE Customer (
	CustID int,
    Name varchar(255),
    SocialSecurityNR varchar(255),
    PRIMARY KEY (CustID)
);

CREATE TABLE ProductsList (
	ProdID int,
    ProdName varchar(255),
    Price int,
    PRIMARY KEY (ProdID)
);

CREATE TABLE Purchase (
	PurchaseID int,
    PurchaseDate date,
    TotalPrice int,
	Quantity int,
    CustID int,
    ProdID int,
    PRIMARY KEY (PurchaseID),
	FOREIGN KEY (CustID) REFERENCES Customer(CustID),
    FOREIGN KEY (ProdID) REFERENCES ProductsList(ProdID)
);


