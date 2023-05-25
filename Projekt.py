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

def insert_into_customer(session, Name, SocialSecurityNR):
    insert_sql = "INSERT INTO customer ( Name, SocialSecurityNR) VALUES ('{}', '{}') ".format(Name, SocialSecurityNR);
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
        purchase_id = get_next_purchase_id(session)
        while True:
            print("Please enter the prodID to select a product.\nIf you would like to view your shopingcart enter 'Cart'.")
            print("If you would like to view all our products enter 'Products'")
            print("If you wuold lite to remove an item from the shoping cart enter 'Remove'")
            print("Enter the product ID (or 'No' to finish): ")
            product_id = input()

            if product_id.lower() == 'no':
                break
            else:
                if product_id.lower() == 'cart':
                    print_purchase()
                elif product_id.lower() == "products":
                    print_productsList()
                elif product_id.lower() == "remove":
                    remove_done = False
                    print("Please enter the product ID of the item you would like to remove.")
                    print("When you are done, enter 'End'.")
                    while not remove_done:
                        remove_prod = input("Your choice: ")
                        if remove_prod.isdigit():
                            if int(remove_prod) < 41 and int(remove_prod) > 0:  # Adjust the range as needed
                                remove_product_from_purchase(session, remove_prod, purchase_id)
                            else:
                                print("Invalid input! Please try again!")
                        else:
                            if remove_prod.lower() == "end":
                                remove_done = True
                            else:
                                print("Invalid input! Please try again!")

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

def get_next_purchase_id(session):
    try:
        query = "SELECT MAX(PurchaseID) FROM Purchase;"
        result = session.sql(query).execute()

        # Fetch the maximum purchase ID
        max_purchase_id = result.fetch_one()[0]

        # Determine the next purchase ID
        if max_purchase_id is None:
            next_purchase_id = 1
        else:
            next_purchase_id = max_purchase_id + 1

        return next_purchase_id
    except DatabaseError as de:
        print(de.msg)

def remove_product_from_purchase(session, product_id, purchase_id):
    try:
        delete_sql = """
        DELETE FROM Purchase
        WHERE PurchaseID = {} AND ProdID = {};
        """.format(purchase_id, product_id)

        session.sql(delete_sql).execute()
        print("Product removed from the purchase.")
    except DatabaseError as de:
        print(de.msg)

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

print("\n")

#Skriver ut alla produkter som kostar mer än 50kr
# Price = 50
# query2 = "SELECT ProdID, ProdName, Price FROM ProductsList WHERE Price > {} GROUP BY ProdID".format(Price)
# result = session.sql(query2).execute()
#print("| {:<15} | {:<15} | {}".format("ProdID", "ProdName", "Price"))
#print("-"*68)
#for (ProdID, ProdName, Price) in result.fetch_all():
    #print("| {:<15} | {:<15} | {}".format(ProdID, ProdName, Price))

print("\n\n")
def print_purchase():
    query = """SELECT p.PurchaseID, p.PurchaseDate, p.TotalPrice, p.Quantity, pl.ProdName FROM Purchase p
                JOIN ProductsList pl ON p.ProdID = pl.ProdID"""
    result = session.sql(query).execute()
    print("| {:<12} | {:<12} | {:<10} | {:<8} | {:<8} |".format("PurchaseID", "PurchaseDate", "TotalPrice", "Quantity", "ProdName"))
    print("-" * 66)
    for (PurchaseID, PurchaseDate, TotalPrice, Quantity, ProdName) in result.fetch_all():
        formatted_date = PurchaseDate.strftime("%Y-%m-%d")
        print("| {:<12} | {:<12} | {:<10} | {:<8} | {:<8} |".format(PurchaseID, formatted_date, TotalPrice, Quantity, ProdName))

def print_productsList():
    query = "SELECT ProdID, ProdName, Price FROM Productslist"
    result = session.sql(query).execute()
    print("| {:<15} | {:<15} | {}".format("ProdID", "ProdName", "Price"))
    print("-"*68)
    for (ProdID, ProdName, Price) in result.fetch_all():
        print("| {:<15} | {:<15} | {}".format(ProdID, ProdName, Price))

    print("\n\n")

def check_customer_existence(session, ssn):
    select_sql = "SELECT * FROM Customer WHERE SocialSecurityNR = '{}'".format(ssn)

    try:
        result = session.sql(select_sql).execute()
        if len(result.fetch_all()) > 0:
            print("Customer exists in the database.")
            return 1
            # Further code for existing customer
        else:
            print("Customer does not exist in the database.")
            return 0
            # Further code for non-existing customer
    except DatabaseError as de:
        print("Failed to check customer existence, error: {}".format(de))

if __name__ == '__main__':
    ok_input = False
    print("Welcome to our Food Store!\n")
    print("We're delighted to offer you a curated selection of mouthwatering food items.")
    print("Explore our collection of fresh ingredients and culinary delights.")
    print("Savor the flavors and elevate your culinary adventures. Enjoy your shopping experience with us!")
    
    while ok_input == False:
        account_yes_no = input("Do you have an account with us? (Please enter 'yes' or 'no'):\n")
        if account_yes_no == "yes":
            social_security = input("Please enter your socialsecurity number (YYMMDDXXXX):\n")
            find_customer = 0
            while find_customer == 0:
                find_customer =  check_customer_existence(session, social_security) #Funkar inte just nu 
                if find_customer == 1:
                    print("Here is a list of all our products:\n")
                    print_productsList()
                    clear_purchase_table(session)
                    make_purchase(session) 
                    print_purchase()
                else:
                    customer_name = input("Please enter your name:\n")
                    social_security = input("Please enter your socialsecurity number (YYMMDDXXXX):\n")
            ok_input = True
        elif account_yes_no == "no":
            customer_name = input("Please enter your name:\n")
            social_security = input("Please enter your socialsecurity number (YYMMDDXXXX):\n")
            insert_into_customer(session,customer_name,social_security)
            clear_purchase_table(session)
            make_purchase(session) 
            print_purchase()
            ok_input = True
        else:
            print("Invalid input! please try again!")
    
    # Det Totala priset för just det köpet
    result = session.sql("SELECT SUM(TotalPrice) AS TotalCost FROM Purchase;").execute()
    row = result.fetch_one()
    total_cost = row[0]
    print("Total Cost: {}".format(total_cost))