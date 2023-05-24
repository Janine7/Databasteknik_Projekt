import mysqlx
from mysqlx.errors import DatabaseError
# Connect to server on localhost
session = mysqlx.get_session({
    "host": "localhost",
    "port": 33060,
    "user": "root",
    "password": "1234"
})

DB_NAME = 'Projekt'

def create_database(session, DB_NAME):
    try:
        print("Creating database {}".format(DB_NAME))
        session.sql("CREATE DATABASE {} DEFAULT CHARACTER SET 'utf8'".format(DB_NAME)).execute()
    except DatabaseError as de:
        print("Faild to create database, error: {}".format(de))
        exit(1)

def create_table_customer(session):
    creat_customer = "CREATE TABLE `Customer` (" \
                 "  `CustID` int NOT NULL AUTO_INCREMENT," \
                 "  `Name` varchar(255) NOT NULL," \
                 "  `SocialSecurityNR` varchar(255) NOT NULL," \
                 "  PRIMARY KEY (`CustID`)" \
                 ") ENGINE=InnoDB"

    try:
        print("Creating table customer: ")
        session.sql(creat_customer).execute()
    except DatabaseError as de:
        if de.errno == 1050:
            print("already exists.")
        else:
            print(de.msg)
    else:
        print("OK")

def create_table_productslist(session):
    creat_productslist = "CREATE TABLE `ProductsList` (" \
                 "  `ProdID` int NOT NULL AUTO_INCREMENT," \
                 "  `ProdName` varchar(255) NOT NULL," \
                 "  `Price` varchar(255) NOT NULL," \
                 "  PRIMARY KEY (`ProdID`)" \
                 ") ENGINE=InnoDB"

    try:
        print("Creating table productslist: ")
        session.sql(creat_productslist).execute()
    except DatabaseError as de:
        if de.errno == 1050:
            print("already exists.")
        else:
            print(de.msg)
    else:
        print("OK")

def create_table_purchase(session):
    creat_purchase = "CREATE TABLE `Purchase` (" \
                 "  `PurchaseID` int NOT NULL AUTO_INCREMENT," \
                 "  `PurchaseDate` date," \
                 "  `TotalPrice` int NOT NULL," \
                 "  `Quantity` int NOT NULL," \
                 "  `CustID` int NOT NULL," \
                 "  `ProdID` int NOT NULL," \
                 "  PRIMARY KEY (`PurchaseID`)," \
                 "  FOREIGN KEY (`CustID`)  REFERENCES Customer(`CustID`)," \
                 "  FOREIGN KEY (`ProdID`)  REFERENCES ProductsList(`ProdID`)" \
                 ") ENGINE=InnoDB"

    try:
        print("Creating table purchase: ")
        session.sql(creat_purchase).execute()
    except DatabaseError as de:
        if de.errno == 1050:
            print("already exists.")
        else:
            print(de.msg)
    else:
        print("OK")

def insert_into_productslist(session):
    insert_sql = ["INSERT INTO ProductsList (ProdID, ProdName, Price)"
                  "VALUES ('1', 'Cucumber', '15');",
                  "INSERT INTO ProductsList (ProdID, ProdName, Price)"
                  "VALUES ('2', 'Tomato', '4');",
                  "INSERT INTO ProductsList (ProdID, ProdName, Price)"
                  "VALUES ('3', 'Onion', '2');",
                  "INSERT INTO ProductsList (ProdID, ProdName, Price)"
                  "VALUES ('4', 'Salad', '20');",
                  "INSERT INTO ProductsList (ProdID, ProdName, Price)"
                  "VALUES ('5', 'Parsley', '19');",
                  "INSERT INTO ProductsList (ProdID, ProdName, Price)"
                  "VALUES ('6', 'Basil', '22');",
                  "INSERT INTO ProductsList (ProdID, ProdName, Price)"
                  "VALUES ('7', 'Lemon', '10');",
                  "INSERT INTO ProductsList (ProdID, ProdName, Price)"
                  "VALUES ('8', 'Apple', '5');",
                  "INSERT INTO ProductsList (ProdID, ProdName, Price)"
                  "VALUES ('9', 'Pear', '9');",
                  "INSERT INTO ProductsList (ProdID, ProdName, Price)"
                  "VALUES ('10', 'Banana', '4');",
                  "INSERT INTO ProductsList (ProdID, ProdName, Price)"
                  "VALUES ('11', 'Melon', '28');",
                  "INSERT INTO ProductsList (ProdID, ProdName, Price)"
                  "VALUES ('12', 'Grapes', '35');",
                  "INSERT INTO ProductsList (ProdID, ProdName, Price)"
                  "VALUES ('13', 'Bread', '30');",
                  "INSERT INTO ProductsList (ProdID, ProdName, Price)"
                  "VALUES ('14', 'Knäckebröd', '22');",
                  "INSERT INTO ProductsList (ProdID, ProdName, Price)"
                  "VALUES ('15', 'Skorpa', '20');",
                  "INSERT INTO ProductsList (ProdID, ProdName, Price)"
                  "VALUES ('16', 'Riskaka', '15');",
                  "INSERT INTO ProductsList (ProdID, ProdName, Price)"
                  "VALUES ('17', 'Cookie', '20');",
                  "INSERT INTO ProductsList (ProdID, ProdName, Price)"
                  "VALUES ('18', 'Ham', '30');",
                  "INSERT INTO ProductsList (ProdID, ProdName, Price)"
                  "VALUES ('19', 'Meatballs', '23');",
                  "INSERT INTO ProductsList (ProdID, ProdName, Price)"
                  "VALUES ('20', 'Sausage', '36');",
                  "INSERT INTO ProductsList (ProdID, ProdName, Price)"
                  "VALUES ('21', 'Minced meat', '89');",
                  "INSERT INTO ProductsList (ProdID, ProdName, Price)"
                  "VALUES ('22', 'Chicken', '105');",
                  "INSERT INTO ProductsList (ProdID, ProdName, Price)"
                  "VALUES ('23', 'Salmon', '109');",
                  "INSERT INTO ProductsList (ProdID, ProdName, Price)"
                  "VALUES ('24', 'Cod', '70');",
                  "INSERT INTO ProductsList (ProdID, ProdName, Price)"
                  "VALUES ('25', 'Liver paste', '15');",
                  "INSERT INTO ProductsList (ProdID, ProdName, Price)"
                  "VALUES ('26', 'Milk', '12');",
                  "INSERT INTO ProductsList (ProdID, ProdName, Price)"
                  "VALUES ('27', 'Yoghurt', '25');",
                  "INSERT INTO ProductsList (ProdID, ProdName, Price)"
                  "VALUES ('28', 'Butter', '60');",
                  "INSERT INTO ProductsList (ProdID, ProdName, Price)"
                  "VALUES ('29', 'Cheese', '99');",
                  "INSERT INTO ProductsList (ProdID, ProdName, Price)"
                  "VALUES ('30', 'Cream', '29');",
                  "INSERT INTO ProductsList (ProdID, ProdName, Price)"
                  "VALUES ('31', 'Cream Fraiche', '16');",
                  "INSERT INTO ProductsList (ProdID, ProdName, Price)"
                  "VALUES ('32', 'Beans', '10');",
                  "INSERT INTO ProductsList (ProdID, ProdName, Price)"
                  "VALUES ('33', 'Taco seasoning', '10');",
                  "INSERT INTO ProductsList (ProdID, ProdName, Price)"
                  "VALUES ('34', 'Tortilla', '15');",
                  "INSERT INTO ProductsList (ProdID, ProdName, Price)"
                  "VALUES ('35', 'Chips', '29');",
                  "INSERT INTO ProductsList (ProdID, ProdName, Price)"
                  "VALUES ('36', 'Candy', '125');",
                  "INSERT INTO ProductsList (ProdID, ProdName, Price)"
                  "VALUES ('37', 'Chocolate', '22');",
                  "INSERT INTO ProductsList (ProdID, ProdName, Price)"
                  "VALUES ('38', 'Ice cream', '30');",
                  "INSERT INTO ProductsList (ProdID, ProdName, Price)"
                  "VALUES ('39', 'Soda', '19');",
                  "INSERT INTO ProductsList (ProdID, ProdName, Price)"
                  "VALUES ('40', 'Juice', '18');"
                  ]

    for query in insert_sql:
        try:
            print("SQL query {}: ".format(query), end='')
            session.sql(query).execute()
        except DatabaseError.Error as err:
            print(err.msg)
        else:
            print("OK")

try:
    session.sql("USE {}".format(DB_NAME)).execute()
except DatabaseError as de:
    if de.errno == 1049:
        print("Error: Database '{}' does not exist.".format(DB_NAME))

        create_database(session, DB_NAME)
        session.sql("USE {}".format(DB_NAME)).execute()
        create_table_customer(session)
        create_table_productslist(session)
        create_table_purchase(session)
        insert_into_productslist(session)
    else:
        print("Error executing SQL command: {}".format(de))
        raise

#Skriver ut alla produkter
query = "SELECT ProdID, ProdName, Price FROM Productslist"
result = session.sql(query).execute()
for (ProdID, ProdName, Price) in result.fetch_all():
    print("ProdID: {:<15} Product: {:<15} Price: {}".format(ProdID, ProdName, Price))

print("\n\n")

#Skriver ut alla produkter som kostar mer än 50kr
Price = 50
query2 = "SELECT ProdID, ProdName, Price FROM productslist WHERE Price>{}".format(Price)
result = session.sql(query2).execute()

print("| {:<15} | {:<15} | {}".format("ProdID", "ProdName", "Price"))
print("-"*68)
for (ProdID, ProdName, Price) in result.fetch_all():
    print("| {:<15} | {:<15} | {}".format(ProdID, ProdName, Price))

print("hej")