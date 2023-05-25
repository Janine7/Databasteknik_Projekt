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

def insert_into_customer(session, name, ssn):
    insert_sql = "INSERT INTO Customer (Name, SocialSecurityNR) VALUES ('{}', '{}')".format(name, ssn)

    try:
        print("Inserting new customer: ")
        session.sql(insert_sql).execute()
        print("Customer inserted successfully.")
    except DatabaseError as de:
        print("Failed to insert customer, error: {}".format(de))

def check_customer_existence(session, ssn): #FUNKAR INTE
    '''select_sql = "SELECT * FROM Customer WHERE SocialSecurityNR = '{}'".format(ssn)

    try:
        result = session.sql(select_sql).execute()
        if result.fetch_all() > 0:
            print("Customer exists in the database.")
            return 1
            # Further code for existing customer
        else:
            print("Customer does not exist in the database.")
            return 0
            # Further code for non-existing customer
    except DatabaseError as de:
        print("Failed to check customer existence, error: {}".format(de))'''
    print("In check_cutomer_existence")
    return 1

def print_purchase():
    print("In print_purchase")

def remove_product():
    print("In remove_product")

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
def print_productsList():
    query = "SELECT ProdID, ProdName, Price FROM Productslist"
    result = session.sql(query).execute()
    print("| {:<15} | {:<15} | {}".format("ProdID", "ProdName", "Price"))
    print("-"*68)
    for (ProdID, ProdName, Price) in result.fetch_all():
        print("| {:<15} | {:<15} | {}".format(ProdID, ProdName, Price))

    print("\n\n")

#Skriver ut alla produkter som kostar mer än 50kr
Price = 50
query2 = "SELECT ProdID, ProdName, Price FROM productslist WHERE Price>{}".format(Price)
result = session.sql(query2).execute()

print("| {:<15} | {:<15} | {}".format("ProdID", "ProdName", "Price"))
print("-"*68)
for (ProdID, ProdName, Price) in result.fetch_all():
    print("| {:<15} | {:<15} | {}".format(ProdID, ProdName, Price))

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
                    cart = []
                    done = False
                    print("Here is a list of all our products:\n")
                    print_productsList()
                    while done == False:
                        print("Please enter the prodID to select a product.\nIf you would like to view your shopingcart enter 'Cart'.")
                        print("If you would like to view all our products enter 'Products'")
                        print("If you wuold lite to remove an item from the shoping cart enter 'Remove'")
                        print("If you would like to go to checkout enter 'Done'.")
                        selected_prod = input("Your choice: ")
                        if selected_prod.isdigit():
                            if int(selected_prod) < 41: #Hårdkodat?
                                cart.append(selected_prod)
                            else:
                                print("Invalid input! Please try again!\n")
                        else:
                            if selected_prod == "Done":
                                done = True
                            elif selected_prod == "Cart":
                                print_purchase() #Inte klar
                            elif selected_prod == "Products":
                                print_productsList()
                            elif selected_prod == "Remove":
                                remove_done = False
                                print("Please enter the prodID of the item you would like to remove:\nWhen you are done enter 'End'.\n")
                                while remove_done == False:
                                    remove_prod = input("Your choice: ")
                                    if remove_prod.isdigit():
                                        if int(remove_prod) < 41 and int(remove_prod) > 0 :#Hårdkodat?
                                            remove_product()#Inte klar 
                                        else:
                                            print("Invalid input! Please try again!\n")
                                    else:
                                        if remove_prod == "End":
                                            remove_done = True
                                        else:
                                            print("Invalid input! Please try again!\n")
                            else:
                                print("Invalid input! Please try again!\n")
                    print("Thank you for your purchase!\nWe appreciate your business and hope you had a great shopping experience with us.")
                    print("We look forward to serving you again in the future.\nWelcome back!\n")
                            
                else:
                    customer_name = input("Please enter your name:\n")
                    social_security = input("Please enter your socialsecurity number (YYMMDDXXXX):\n")
            ok_input = True
        elif account_yes_no == "no":
            customer_name = input("Please enter your name:\n")
            social_security = input("Please enter your socialsecurity number (YYMMDDXXXX):\n")
            insert_into_customer(session,customer_name,social_security)
            ok_input = True
        else:
            print("Invalid input! please try again!")
