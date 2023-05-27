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
    try:
        # Insert the new customer into the customer table
        insert_sql = "INSERT INTO customer (Name, SocialSecurityNR) VALUES ('{}', '{}')".format(Name, SocialSecurityNR)
        print("Inserting into customer table:")
        session.sql(insert_sql).execute()
        print("OK")
        return True
    except DatabaseError as de:
        print(de.msg)
        return False

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

# Creating stored Procedure
def create_stored_procedure(session):
    procedure_sql = """
    CREATE PROCEDURE calculate_total_cost()
    BEGIN
        -- Calculate the total cost of the purchase
        SELECT SUM(TotalPrice) AS TotalCost FROM Purchase;
    END;
    """
    try:
        print("Creating stored procedure: ")
        session.sql(procedure_sql).execute()
        print("OK")
    except DatabaseError as de:
        if de.errno == 1304:
            print("Stored procedure already exists.")
        else:
            print(de.msg)

def execute_stored_procedure(session):
    try:
        # Call the stored procedure
        call_sql = "CALL calculate_total_cost();"
        result = session.sql(call_sql).execute()

        # Fetch the result of the stored procedure
        row = result.fetch_one()
        total_cost = row[0]
        print("Total Cost: {}".format(total_cost))

    except DatabaseError as de:
        print("Error executing stored procedure: {}".format(de.msg))

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
        purchase_complete = False

        while not purchase_complete:
            print("If you would like to view your shopping cart, enter 'Cart'.")
            print("If you would like to view all our products, enter 'Products'.")
            print("If you would like to remove an item from the shopping cart, enter 'Remove'.")
            print("Enter the product ID (or 'No' to finish): ")
            product_id = input()

            if product_id.lower() == 'no':
                break
            elif product_id.lower() == 'cart':
                print_purchase()
                make_purchase(session)
                return
            elif product_id.lower() == "products":
                print_productsList()
                make_purchase(session)
                return
            elif product_id.lower() == "remove":
                while True:
                    print("Enter the product ID to remove or 'end' to cancel: ")
                    product_id_remove = input()
                    if product_id_remove.lower() == "end":
                        print("Removal cancelled.")
                        make_purchase(session)
                        return
                    elif product_id_remove.isdigit():
                        if check_product_in_purchase(session, product_id_remove):
                            remove_product_from_purchase(session, product_id_remove)
                            make_purchase(session)
                            return
                        else:
                            print("Product ID does not exist in the purchase. Try again or enter 'end' to cancel the removal.")
                    else:
                        print("Invalid input. Please enter a valid product ID or 'end' to cancel.")
                        
            elif product_id.isdigit():
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

                # Calculate the discounted price
                discounted_price = calculate_discount(session, product_id)
                print("Discounted Price:", discounted_price)  # Add this line

                # Check if the product already exists in the Purchase table
                check_sql = "SELECT COUNT(*) FROM Purchase WHERE ProdID = {};".format(product_id)
                result = session.sql(check_sql).execute()
                count = result.fetch_one()[0]

                if count > 0:
                    # Update the quantity of the existing row
                    update_sql = "UPDATE Purchase SET Quantity = Quantity + {} WHERE ProdID = {};".format(quantity, product_id)
                    session.sql(update_sql).execute()
                else:
                    # Insert the purchase into the Purchase table
                    total_price = quantity * discounted_price  # Calculate the total price
                    insert_sql = """
                    INSERT INTO Purchase (PurchaseID, PurchaseDate, TotalPrice, Quantity, CustID, ProdID, Price)
                    VALUES (NULL, CURDATE(), {}, {}, 1, {}, {});""".format(total_price, quantity, product_id, price)
                    session.sql(insert_sql).execute()

                print("Product added to the purchase.")
            else:
                print("invalid input, try again")
                make_purchase(session)

    except DatabaseError as de:
        print(de.msg)
    except ValueError:
        print("Invalid input. Please enter a valid product ID and quantity.")

def check_product_in_purchase(session, product_id):
    try:
        query = "SELECT * FROM Purchase WHERE ProdID = {};".format(product_id)
        result = session.sql(query).execute()
        rows = result.fetch_all()
        return len(rows) > 0
    except DatabaseError as de:
        print(de.msg)
        return False

def remove_product_from_purchase(session, product_id):
    try:
        remove_sql = "DELETE FROM Purchase WHERE ProdID = {} AND CustID = 1;".format(product_id)
        session.sql(remove_sql).execute()
        print("Product removed from the purchase.")
    except DatabaseError as de:
        print(de.msg)

def calculate_discount(session, product_id):
    try:
        # Execute the discount calculation function for the specified product ID
        discount_sql = "SELECT calculate_discounted_price({}) AS discounted_price".format(product_id)
        result = session.sql(discount_sql).execute()

        row = result.fetch_one()
        discounted_price = row[0]  # Access the discounted price directly
        #print("result in calculate_discount:", discounted_price)
        return discounted_price

    except DatabaseError as de:
        print(de.msg)

def create_discounted_price_function(session):
    function_sql = """
        CREATE FUNCTION calculate_discounted_price(prod_id INT)
        RETURNS DECIMAL(10,2)
        DETERMINISTIC
        BEGIN
            DECLARE original_price DECIMAL(10,2);
            DECLARE discounted_price DECIMAL(10,2);
            
            -- Retrieve the original price of the product
            SELECT Price INTO original_price FROM ProductsList WHERE ProdID = prod_id;
            
            -- Apply discount based on product ID
            IF prod_id = 12 THEN
                SET discounted_price = original_price - (original_price * 10 / 100); -- 10% discount
            ELSEIF prod_id = 34 THEN
                SET discounted_price = original_price - (original_price * 15 / 100); -- 15% discount
            ELSEIF prod_id = 40 THEN
                SET discounted_price = original_price - (original_price * 20 / 100); -- 20% discount
            ELSE
                SET discounted_price = original_price; -- No discount
            END IF;
            
            RETURN discounted_price;
        END
    """
    try:
        print("Creating Function: ")
        session.sql(function_sql).execute()
        print("OK")
    except DatabaseError as de:
        if de.errno == 1304:
            print("Function already exists.")
        else:
            print(de.msg)

def print_purchase():
    query = """SELECT p.PurchaseID, p.PurchaseDate, p.TotalPrice, p.Quantity, pl.ProdName FROM Purchase p
                JOIN ProductsList pl ON p.ProdID = pl.ProdID"""
    result = session.sql(query).execute()
    print("| {:<12} | {:<12} | {:<10} | {:<8} | {:<12} |".format("PurchaseID", "PurchaseDate", "TotalPrice", "Quantity", "ProdName"))
    print("-" * 70)
    for (PurchaseID, PurchaseDate, TotalPrice, Quantity, ProdName) in result.fetch_all():
        formatted_date = PurchaseDate.strftime("%Y-%m-%d")
        print("| {:<12} | {:<12} | {:<10} | {:<8} | {:<12} |".format(PurchaseID, formatted_date, TotalPrice, Quantity, ProdName))

def print_productsList():
    query = "SELECT * FROM Productslist"
    result = session.sql(query).execute()
    print("| {:<15} | {:<15} | {}".format("ProdID", "ProdName", "Price"))
    print("-"*68)
    for (ProdID, ProdName, Price) in result.fetch_all():
        print("| {:<15} | {:<15} | {}".format(ProdID, ProdName, Price))

def check_customer_existence(session, ssn):
    query = "SELECT * FROM Customer WHERE SocialSecurityNR = '{}'".format(ssn)
    try:
        result = session.sql(query).execute()
        if len(result.fetch_all()) > 0:
            print("Customer exists in the database.")
            return 1
            # Further code for existing customer
        else:
            print("Customer does not exist in the database.")
            return 0
    except DatabaseError as de:
        print("Failed to check customer existence, error: {}".format(de))

def find_cheapest_product(session):
    query = """
        SELECT pl.ProdName, p.Quantity * pl.Price AS TotalPrice
        FROM Purchase p
        JOIN ProductsList pl ON p.ProdID = pl.ProdID
        ORDER BY TotalPrice ASC
        LIMIT 1
    """
    result = session.sql(query).execute()
    row = result.fetch_one()
    
    if row:
        prod_name = row[0]
        print("The cheapest product in the purchase table is: {}".format(prod_name))
    else:
        print("No data found in the purchase table.")

def find_expensive_product(session):
    query = """
        SELECT pl.ProdName, p.Quantity * pl.Price AS TotalPrice
        FROM Purchase p
        JOIN ProductsList pl ON p.ProdID = pl.ProdID
        ORDER BY TotalPrice DESC
        LIMIT 1
    """
    result = session.sql(query).execute()
    row = result.fetch_one()
    
    if row:
        prod_name = row[0]
        print("The most expensive product in the purchase table is: {}".format(prod_name))
    else:
        print("No data found in the purchase table.")

def generate_order_number(session):
    # Generate a random order number using alphanumeric characters in MySQL
    query = "SELECT CONCAT(UPPER(SUBSTRING(MD5(RAND()) FROM 1 FOR 5)), LPAD(FLOOR(RAND() * 99999.99), 5, '0')) AS order_number"
    result = session.sql(query).execute()
    result = result.fetch_one()[0]
    return result

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
        create_stored_procedure(session)
        create_discounted_price_function(session)
    else:
        print("Error executing SQL command: {}".format(de))
        raise

def call_functions(session):
    print("Here is a list of all our products:\n")
    print_productsList()
    clear_purchase_table(session)
    make_purchase(session)
    print_purchase()
    execute_stored_procedure(session)
    order_number = generate_order_number(session)
    print("Order Number: {}".format(order_number))
    find_expensive_product(session)
    find_cheapest_product(session)
    return

if __name__ == '__main__':
    print("Welcome to our Food Store!\n")
    print("We're delighted to offer you a curated selection of mouthwatering food items.")
    print("Explore our collection of fresh ingredients and culinary delights.")
    print("Savor the flavors and elevate your culinary adventures. Enjoy your shopping experience with us!")

    ok_input = False
    while ok_input == False:
        account_yes_no = input("Do you have an account with us? (Please enter 'yes' or 'no'):\n")
        if account_yes_no == "yes":
            ok_input = True
            social_security_input = False
            while social_security_input == False:
                social_security = input("Please enter your social security number (YYMMDDXXXX):\n")
                if len(social_security) == 10:
                    social_security_input = True
                    find_customer = check_customer_existence(session, social_security)
                    if find_customer == 1:
                        call_functions(session)
                    else:
                        input_ok = False
                        while input_ok == False:
                            create_account = input("You don't have an account. Do you want to create one? (Please enter 'yes' or 'no'):\n")
                            if create_account == "yes":
                                input_ok = True
                                customer_name = input("Please enter your name:\n")
                                insert_into_customer(session, customer_name, social_security)
                                call_functions(session)
                            elif create_account == "no":
                                input_ok = True
                                print("Thank you. Goodbye!")
                            else:
                                print("Invalid input, try again")
                   
                else:
                        print("Invalid social security input, try again!")

        elif account_yes_no == "no":
            ok_input = True
            customer_name = input("Please enter your name:\n")
            social_security_input = False
            while social_security_input == False:
                social_security = input("Please enter your social security number (YYMMDDXXXX):\n")
                if len(social_security) == 10:
                    social_security_input = True
                    find_customer = check_customer_existence(session, social_security)
                    if find_customer == 1:
                        input = False
                        while input == False:
                            continue_purchase = input("You already have an account. Do you want to continue with the purchase? (Please enter 'yes' or 'no'):\n")
                            if continue_purchase == "yes":
                                input = True
                                print("Here is a list of all our products:\n")
                                call_functions(session)
                            elif continue_purchase == "no":
                                input = True
                                print("Thank you. Goodbye!")
                            else:
                                print("Invalid input, try again!")
                    else:
                        insert_into_customer(session, customer_name, social_security)
                        call_functions(session)
                else:
                    print("Invalid social security number, try again")
        else:
            print("Invalid input! Please try again!")


  #  main()