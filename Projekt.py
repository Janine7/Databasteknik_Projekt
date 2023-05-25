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

def insert_into_customer(session):
    insert_sql = """
    INSERT INTO customer (CustID, Name, SocialSecurityNR)
    VALUES (1, 'John Doe', '19981226-1257');
    """
    try:
        print("Inserting into customer table: ")
        session.sql(insert_sql).execute()
    except DatabaseError as de:
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
                 "  `TotalPrice` varchar(255) NOT NULL," \
                 "  `Quantity` int NOT NULL," \
                 "  `CustID` int NOT NULL," \
                 "  `ProdID` int NOT NULL," \
                 "  `Price` varchar(255) NOT NULL," \
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
    insert_sql = ["""INSERT INTO ProductsList (ProdID, ProdName, Price) VALUES
                  ('1', 'Cucumber', '15'),
                  ('2', 'Tomato', '4'),
                  ('3', 'Onion', '2'),
                  ('4', 'Salad', '20'),
                  ('5', 'Parsley', '19'),
                  ('6', 'Basil', '22'),
                  ('7', 'Lemon', '10'),
                  ('8', 'Apple', '5'),
                  ('9', 'Pear', '9'),
                  ('10', 'Banana', '4'),
                  ('11', 'Melon', '28'),
                  ('12', 'Grapes', '35'),
                  ('13', 'Bread', '30'),
                  ('14', 'Knäckebröd', '22'),
                  ('15', 'Skorpa', '20'),
                  ('16', 'Riskaka', '15'),
                  ('17', 'Cookie', '20'),
                  ('18', 'Ham', '30'),
                  ('19', 'Meatballs', '23'),
                  ('20', 'Sausage', '36'),
                  ('21', 'Minced meat', '89'),
                  ('22', 'Chicken', '105'),
                  ('23', 'Salmon', '109'),
                  ('24', 'Cod', '70'),
                  ('25', 'Liver paste', '15'),
                  ('26', 'Milk', '12'),
                  ('27', 'Yoghurt', '25'),
                  ('28', 'Butter', '60'),
                  ('29', 'Cheese', '99'),
                  ('30', 'Cream', '29'),
                  ('31', 'Cream Fraiche', '16'),
                  ('32', 'Beans', '10'),
                  ('33', 'Taco seasoning', '10'),
                  ('34', 'Tortilla', '15'),
                  ('35', 'Chips', '29'),
                  ('36', 'Candy', '125'),
                  ('37', 'Chocolate', '22'),
                  ('38', 'Ice cream', '30'),
                  ('39', 'Soda', '19'),
                  ('40', 'Juice', '18');"""
                  ]

    for query in insert_sql:
        try:
            print("SQL query {}: ".format(query), end='')
            session.sql(query).execute()
        except DatabaseError.Error as err:
            print(err.msg)
        else:
            print("OK")

# Define a trigger function
def trigger_on_insert(session):
    trigger_sql = """
    CREATE TRIGGER update_total_price BEFORE INSERT ON purchase FOR EACH ROW
    BEGIN
        SET NEW.TotalPrice = (
            SELECT Price * NEW.Quantity FROM ProductsList
            WHERE ProdID = NEW.ProdID
        );
    END;
    """
    try:
        print("Creating trigger: ")
        session.sql(trigger_sql).execute()
    except DatabaseError as de:
        if de.errno == 1304:
            print("already exists.")
        else:
            print(de.msg)
    else:
        print("OK")

def clear_purchase_table(session):
    try:
        # Execute the TRUNCATE TABLE statement
        session.sql("TRUNCATE TABLE Purchase;").execute()
        print("Purchase table cleared successfully.")
    except DatabaseError as de:
        print("Error clearing Purchase table: {}".format(de.msg))

def make_purchase(session):
    try:
        total_price = 0

        while True:
            print("Enter the product ID (or 'No' to finish): ")
            product_id = input()

            if product_id.lower() == 'no':
                break

            print("Enter the quantity: ")
            quantity = int(input())

            # Retrieve the price of the selected product from the ProductsList table
            price_sql = "SELECT Price FROM ProductsList WHERE ProdID = {};".format(product_id)
            result = session.sql(price_sql).execute()

            # Fetch all the rows returned by the query
            rows = result.fetch_all()
            if len(rows) == 0:
                print("Invalid product ID. Please enter a valid product ID.")
                continue

            # Extract the price from the first row
            price = rows[0][0]

            # Calculate the total price for the current product
            product_total_price = int(price) * int(quantity)
            total_price += product_total_price

            # Insert the purchase into the Purchase table
            insert_sql = """
            INSERT INTO Purchase (PurchaseID, PurchaseDate, TotalPrice, Quantity, CustID, ProdID, Price)
            VALUES (NULL, CURDATE(), {}, {}, 1, {}, {});
            """.format(product_total_price, quantity, product_id, price)

            print("Inserting into Purchase table: ")
            session.sql(insert_sql).execute()
            print("Purchase completed successfully.")

        # print("Total price: {}".format(total_price))
    except DatabaseError as de:
        print(de.msg)
    except ValueError:
        print("Invalid input. Please enter a valid product ID and quantity.")

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
        insert_into_customer(session)
        insert_into_productslist(session)
        trigger_on_insert(session)
        
    else:
        print("Error executing SQL command: {}".format(de))
        raise

#Skriver ut alla produkter
query = "SELECT ProdID, ProdName, Price FROM Productslist"
result = session.sql(query).execute()
for (ProdID, ProdName, Price) in result.fetch_all():
    print("ProdID: {:<15} Product: {:<15} Price: {}".format(ProdID, ProdName, Price))

print("\n")
clear_purchase_table(session)
make_purchase(session)

#Skriver ut alla produkter som kostar mer än 50kr
# Price = 50
# query2 = "SELECT ProdID, ProdName, Price FROM ProductsList WHERE Price > {} GROUP BY ProdID".format(Price)
# result = session.sql(query2).execute()
#print("| {:<15} | {:<15} | {}".format("ProdID", "ProdName", "Price"))
#print("-"*68)
#for (ProdID, ProdName, Price) in result.fetch_all():
    #print("| {:<15} | {:<15} | {}".format(ProdID, ProdName, Price))

# print("\n\n")
# query3 = "SELECT PurchaseID, PurchaseDate, TotalPrice, Quantity, CustID, ProdID FROM Purchase"
# result = session.sql(query3).execute()
# print("| {:<12} | {:<12} | {:<10} | {:<8} | {:<8} | {:<8} |".format("PurchaseID", "PurchaseDate", "TotalPrice", "Quantity", "CustID", "ProdID"))
# print("-" * 77)

# for (PurchaseID, PurchaseDate, TotalPrice, Quantity, CustID, ProdID) in result.fetch_all():
#     formatted_date = PurchaseDate.strftime("%Y-%m-%d")
#     print("| {:<12} | {:<12} | {:<10} | {:<8} | {:<8} | {:<8} |".format(PurchaseID, formatted_date, TotalPrice, Quantity, CustID, ProdID))

print("\n\n")

query4 = """SELECT p.PurchaseID, p.PurchaseDate, p.TotalPrice, p.Quantity, pl.ProdName FROM Purchase p
            JOIN ProductsList pl ON p.ProdID = pl.ProdID"""
result = session.sql(query4).execute()
print("| {:<12} | {:<12} | {:<10} | {:<8} | {:<8} |".format("PurchaseID", "PurchaseDate", "TotalPrice", "Quantity", "ProdName"))
print("-" * 66)
for (PurchaseID, PurchaseDate, TotalPrice, Quantity, ProdName) in result.fetch_all():
    formatted_date = PurchaseDate.strftime("%Y-%m-%d")
    print("| {:<12} | {:<12} | {:<10} | {:<8} | {:<8} |".format(PurchaseID, formatted_date, TotalPrice, Quantity, ProdName))

# Det Totala priset för just det köpet
result = session.sql("SELECT SUM(TotalPrice) AS TotalCost FROM Purchase;").execute()
row = result.fetch_one()
total_cost = row[0]
print("Total Cost: {}".format(total_cost))

def print_productsList():
    query = "SELECT ProdID, ProdName, Price FROM Productslist"
    result = session.sql(query).execute()
    print("| {:<15} | {:<15} | {}".format("ProdID", "ProdName", "Price"))
    print("-"*68)
    for (ProdID, ProdName, Price) in result.fetch_all():
        print("| {:<15} | {:<15} | {}".format(ProdID, ProdName, Price))

    print("\n\n")

if __name__ == '__main__':
    print("\n\n")
    print("Welcome to our Food Store!\n")
    print("We're delighted to offer you a curated selection of mouthwatering food items.")
    print("Explore our collection of fresh ingredients and culinary delights.")
    print("Savor the flavors and elevate your culinary adventures. Enjoy your shopping experience with us!")
    #print_productsList()