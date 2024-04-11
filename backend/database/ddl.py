""" SQL DDL Functions
"""

def create_db_if_not_exists( connection, database):
    try:
        if connection.is_connected():
            cursor = connection.cursor()
            create_db_query = f"CREATE DATABASE IF NOT EXISTS {database};"
            cursor.execute(create_db_query)
            cursor.close()
            connection.database = database
            create_tables_if_not_exist( connection )
            insert_products(connection)
            print("Database Initialized.")

    except Exception as e:
        print("Error Creating Database:", e)

def create_tables_if_not_exist(connection):
    create_queries = """
        CREATE TABLE IF NOT EXISTS Customer(
           Customer_ID VARCHAR(5),
           Name VARCHAR(20) NOT NULL,
           Email TEXT NOT NULL,
           Password_client TEXT,
           PRIMARY KEY(Customer_ID)
        );

        CREATE TABLE IF NOT EXISTS Customer_Order(
           Customer_ID VARCHAR(5),
           Product_ID VARCHAR(5),
           Total_Payment DECIMAL(10, 2),
           Order_Timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
           Status ENUM("In Progress", "Shipped", "Complete"),
           PRIMARY KEY(Customer_ID, Order_Timestamp)
        );

        -- CREATE TABLE Product
        CREATE TABLE IF NOT EXISTS Product(
           Product_ID VARCHAR(5),
           Product_Name TEXT,
           Product_Description TEXT,
           Price INT,
           PRIMARY KEY (Product_ID)
        );

        CREATE TABLE IF NOT EXISTS Customer_Order(
           Customer_ID VARCHAR(5),
           Product_ID VARCHAR(5),
           Total_Payment DECIMAL(10, 2),
           Order_Timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
           Status ENUM("In Progress", "Shipped", "Complete"),
           PRIMARY KEY(Customer_ID, Order_Timestamp),
           FOREIGN KEY(Customer_ID) REFERENCES Customer(Customer_ID)
           ON DELETE CASCADE ON UPDATE CASCADE,
           FOREIGN KEY(Product_ID) REFERENCES Product(Product_ID)
           ON DELETE CASCADE ON UPDATE CASCADE
        );

        -- CREATE TABLE STORAGE
        CREATE TABLE IF NOT EXISTS STORAGE(
           Product_ID VARCHAR(5),
           Quantity INT,
           Threshold INT,
           Restock_Time INT,
           PRIMARY KEY(Product_ID),
           FOREIGN KEY(Product_ID)
           REFERENCES Product(Product_ID) ON DELETE CASCADE ON UPDATE CASCADE
        );

        -- CREATE TABLE Admin
        CREATE TABLE IF NOT EXISTS Admin (
            Admin_ID VARCHAR(5) PRIMARY KEY,
            password VARCHAR(100)
        );

        CREATE TABLE IF NOT EXISTS RESTOCK_REQUESTS(
           Product_ID VARCHAR(5),
           Date_Time TIMESTAMP,
           Status ENUM("In Progress","Shipped",
           "Complete", "Cancelled"),
           Quantity INT,
           PRIMARY KEY (Product_ID, Date_Time),
           FOREIGN KEY(Product_ID) REFERENCES Product(Product_ID)
           ON DELETE CASCADE ON UPDATE CASCADE
        );
    """

    try:
        if connection.is_connected():
            sql_commands_list = [command.strip() for command in create_queries.split(";") if command.strip()]

            cursor = connection.cursor()
            for query in sql_commands_list:
                cursor.execute( query, multi=True)
            connection.commit()
            cursor.close()
            print("Tables created successfully.")
    except Exception as e:
        print("Error Creating Tables:", e)


def insert_products( connection ):
    insert_query = """INSERT INTO Product (Product_ID, Product_Name, Product_Description, Price)
                        VALUES
                        ('P0001', 'Toyota Camry', 'The Toyota Camry, a renowned car model, is the perfect blend of style and performance. This car offers a comfortable and efficient driving experience for those seeking both luxury and reliability.', 1825000),
                        ('P0002', 'Ford F-150', 'The Ford F-150, is built to handle tough tasks with ease. Its robust build and powerful performance make it the ideal choice for work and adventure enthusiasts who require a dependable and rugged vehicle.', 2555000),
                        ('P0003', 'Honda Civic', 'The Honda Civic, a classic car model, is synonymous with reliability and efficiency.Known for its fuel economy and sleek design, this car is a top pick for those who value practicality and style on the road.', 1460000),
                        ('P0004', 'Chevrolet Silverado', 'The Chevrolet Silverado, a versatile truck model, is designed to tackle heavy-duty jobs with finesse.With its strong performance and spacious interior, this truck is perfect for individuals who demand power and comfort.', 2190000),
                        ('P0005', 'BMW S1000RR', 'The BMW S1000RR is a high-performance sportbike that combines cutting-edge technology with thrilling speed. With its aerodynamic design and powerful engine, its the ultimate choice for motorcycle enthusiasts.', 1500000),
                        ('P0006', 'Tesla Model 3', 'The Tesla Model 3 is an electric car that redefines sustainability and style. With its sleek design and advanced autopilot features, it offers a futuristic driving experience for eco-conscious individuals.', 4500000),
                        ('P0007', 'Yamaha YZF R6', 'The Yamaha YZF R6 is a sporty and agile motorcycle designed for adrenaline junkies. Its compact size and powerful engine make it perfect for both city commuting and track racing.', 900000),
                        ('P0008', 'Honda Accord', 'The Honda Accord is a reliable and stylish sedan known for its fuel efficiency and comfortable ride. With advanced safety features and modern design, its a top choice for those seeking a dependable daily driver.', 2600000),
                        ('P0009', 'Ducati Multistrada V4', 'The Ducati Multistrada V4 is an adventure motorcycle built for versatility and performance. With its powerful engine and rugged design, its the perfect option for riders who enjoy both on and off-road journeys.', 2200000),
                        ('P0010', 'Toyota Prius', 'The Toyota Prius is a hybrid car that sets the standard for fuel efficiency. With its eco-friendly features and practical design, its a great choice for environmentally conscious drivers.', 2500000);
                    """
    try:
        if connection.is_connected():
            cursor = connection.cursor()
            cursor.execute("SELECT COUNT(*) FROM Product")
            count = cursor.fetchone()[0]
            if count == 0:  # If Product table is empty, insert data
                cursor.execute(insert_query)
                connection.commit()
                print("Products inserted successfully.")
            cursor.close()
    except Exception as e:
        print("Error Inserting Products:", e)