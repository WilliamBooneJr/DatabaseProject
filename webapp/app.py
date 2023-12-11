from flask import Flask, request, redirect, url_for, render_template
import mysql.connector, os

app = Flask(__name__)

def dbconnection():
    return mysql.connector.connect(
        host='localhost',
        user='billy',
        password='1235',
        db='coffeeshopdb'
    )
@app.route('/') # Display and add coffee shops
def home():
    return render_template('home.html')

def get_max_ID(data):
    print(data)
    maxID = 0
    for i in data:
        if maxID < i[0]:
            maxID = i[0]
    return maxID + 1


@app.route('/coffeeshops', methods=['GET','POST'])

def manage_coffeeshop():
    connection = dbconnection()
    mycursor = connection.cursor()
    mycursor.execute("SELECT * FROM COFFEESHOP")
    data = mycursor.fetchall()
    mycursor.execute("SELECT * FROM EMPLOYEE")
    managers = mycursor.fetchall()
    #Handle POST for creating coffeeshop
    if request.method == 'POST':
        shopID = get_max_ID(data)
        shopname = request.form['shopname']
        location = request.form['location']
        rating = request.form['rating']
        manager = request.form['managerID']
        mycursor.execute("INSERT INTO COFFEESHOP (ShopID, ShopName, Location, Rating, ManagerID) VALUES (%s, %s, %s, %s, %s)", 
                         (shopID, shopname, location, rating, manager))
        connection.commit()
    
    # Fetch the current values of the COFFEESHOP table

    mycursor.execute("SELECT * FROM COFFEESHOP")
    data = mycursor.fetchall()
    mycursor.close()
    connection.close()


    return render_template('coffeeshops.html', coffeeshop=data, managers=managers)

@app.route('/coffeeshops/<int:shop_id>', methods=['GET', 'POST'])  # Update a coffee shop
def update_coffeeshop(shop_id):
    connection = dbconnection()
    mycursor = connection.cursor()
    mycursor.execute("SELECT * FROM EMPLOYEE")
    managers = mycursor.fetchall()

    
    if request.method == 'POST':
        shopID = shop_id
        shopname = request.form['shopname']
        location = request.form['location']
        rating = request.form['rating']
        manager = request.form['managerID']
        sql = "UPDATE COFFEESHOP SET ShopName = '%s', Location = '%s', Rating = %s, ManagerID = %s WHERE ShopID = %s" % (shopname, location, rating, manager, shopID)
        print(sql)
        mycursor.execute(sql)
        connection.commit()
        mycursor.execute("SELECT * FROM COFFEESHOP")
        data = mycursor.fetchall()
        return render_template('coffeeshops.html', coffeeshop=data, managers=managers)
    
    # Fetch the current values of the COFFEESHOP table

    mycursor.execute("SELECT * FROM COFFEESHOP")
    data = mycursor.fetchall()

   
    #Fetch the details of the coffee shop to pre-fill the form
    sql = "SELECT * FROM COFFEESHOP WHERE ShopID = %s" % (shop_id)
    mycursor.execute(sql)
    data = mycursor.fetchone()
    mycursor.close()
    connection.close()
    print(data)
    return render_template('updatecoffeeshop.html', shop_details=data, managers=managers)


@app.route('/coffeeshops/delete/<int:shop_id>', methods=['POST'])  # Delete a coffee shop
def delete_coffeeshop(shop_id):
    connection = dbconnection()
    mycursor = connection.cursor()

    sql = "DELETE FROM COFFEESHOP WHERE ShopID = %d" % (shop_id)
    mycursor.execute(sql)
    connection.commit()
    mycursor.close()
    connection.close()
    return redirect(url_for('manage_coffeeshop'))

# Route for managing suppliers
@app.route('/suppliers', methods=['GET', 'POST'])

def manage_supplier():
    connection = dbconnection()
    mycursor = connection.cursor()
    mycursor.execute("SELECT * FROM SUPPLIER")
    data = mycursor.fetchall()

    if request.method == 'POST':
        # Handle form submissions for adding suppliers
        supplierID = get_max_ID(data)
        suppliername = request.form['suppliername']
        supplierlocation = request.form['supplierlocation']
        mycursor.execute("INSERT INTO SUPPLIER (SupplierID, SupplierName, SupplierLocation) VALUES (%s, %s, %s)", 
                         (supplierID, suppliername, supplierlocation))
        connection.commit()

    # Fetch the list of suppliers
    mycursor.execute("SELECT * FROM SUPPLIER")
    data = mycursor.fetchall()
    mycursor.close()
    connection.close()

    return render_template('suppliers.html', suppliers=data)

@app.route('/suppliers/<int:supplier_id>', methods=['GET', 'POST'])

def update_supplier(supplier_id):
    connection = dbconnection()
    mycursor = connection.cursor()

    if request.method == 'POST':
        supplierID = supplier_id
        suppliername = request.form['suppliername']
        supplierlocation = request.form['supplierlocation']
        sql = "UPDATE SUPPLIER SET SupplierName = %s, SupplierLocation = %s WHERE SupplierID = %s"
        mycursor.execute(sql, (suppliername, supplierlocation, supplierID))
        connection.commit()
        mycursor.execute("SELECT * FROM SUPPLIER")
        suppliers = mycursor.fetchall()
        return render_template('suppliers.html', suppliers=suppliers)
    
    # Fetch the current values of the SUPPLIER table

    mycursor.execute("SELECT * FROM SUPPLIER WHERE SupplierID = %s", (supplier_id,))
    supplier = mycursor.fetchone()

    mycursor.close()
    connection.close()

    return render_template('updatesupplier.html', supplier_details=supplier)


@app.route('/suppliers/delete/<int:supplier_id>', methods=['POST'])

def delete_supplier(supplier_id):
    connection = dbconnection()
    mycursor = connection.cursor()

    sql = "DELETE FROM SUPPLIER WHERE SupplierID = %s"
    mycursor.execute(sql, (supplier_id,))
    connection.commit()
    mycursor.close()
    connection.close()
    return redirect(url_for('manage_supplier'))

# Route for managing contracts
@app.route('/contracts', methods=['GET', 'POST'])

def manage_contract():
    connection = dbconnection()
    mycursor = connection.cursor()
    # Add logic for CRUD operations here
    mycursor.execute("""
        SELECT CONTRACT.ContractID, COFFEESHOP.ShopName, SUPPLIER.SupplierName
        FROM CONTRACT
        JOIN COFFEESHOP ON CONTRACT.ShopID = COFFEESHOP.ShopID
        JOIN SUPPLIER ON CONTRACT.SupplierID = SUPPLIER.SupplierID
    """)
    data = mycursor.fetchall()

    if request.method == 'POST':
        # Handle form submissions for adding contracts
        contractID = get_max_ID(data)
        supplierID = request.form['supplierID']
        shopID = request.form['shopID']
        mycursor.execute("INSERT INTO CONTRACT (ContractID, SupplierID, ShopID) VALUES (%s, %s, %s)", 
                         (contractID, supplierID, shopID))
        connection.commit()

    mycursor.execute("""
        SELECT CONTRACT.ContractID, COFFEESHOP.ShopName, SUPPLIER.SupplierName
        FROM CONTRACT
        JOIN COFFEESHOP ON CONTRACT.ShopID = COFFEESHOP.ShopID
        JOIN SUPPLIER ON CONTRACT.SupplierID = SUPPLIER.SupplierID
    """)
    data = mycursor.fetchall()

    # Fetch suppliers
    mycursor.execute("SELECT SupplierID, SupplierName FROM SUPPLIER")
    suppliers = mycursor.fetchall()

    # Fetch coffee shops
    mycursor.execute("SELECT ShopID, ShopName FROM COFFEESHOP")
    coffeeshops = mycursor.fetchall()

    mycursor.close()
    connection.close()

    return render_template('contracts.html', contracts=data, suppliers=suppliers, coffeeshops=coffeeshops)

@app.route('/contracts/<int:contract_id>', methods=['GET', 'POST'])  # Update a contract
def update_contract(contract_id):
    connection = dbconnection()
    mycursor = connection.cursor()

    # Fetch suppliers
    mycursor.execute("SELECT SupplierID, SupplierName FROM SUPPLIER")
    suppliers = mycursor.fetchall()
    print(suppliers)
  

    # Fetch coffee shops
    mycursor.execute("SELECT ShopID, ShopName FROM COFFEESHOP")
    coffeeshops = mycursor.fetchall()
    print(coffeeshops)


    #Fetch contract
    mycursor.execute("""
        SELECT CONTRACT.ContractID, COFFEESHOP.ShopName, SUPPLIER.SupplierName
        FROM CONTRACT
        JOIN COFFEESHOP ON CONTRACT.ShopID = COFFEESHOP.ShopID
        JOIN SUPPLIER ON CONTRACT.SupplierID = SUPPLIER.SupplierID
    """)
    data = mycursor.fetchall()
    print(data)

    if request.method == 'POST':
        contractID = contract_id
        supplierID = request.form['supplierID']
        shopID = request.form['shopID']
        sql = "UPDATE CONTRACT SET SupplierID = '%s', ShopID = '%s' WHERE ContractID = %s" % (supplierID, shopID, contractID)
        print(sql)
        mycursor.execute(sql)
        connection.commit()
        mycursor.execute("""
        SELECT CONTRACT.ContractID, COFFEESHOP.ShopName, SUPPLIER.SupplierName
        FROM CONTRACT
        JOIN COFFEESHOP ON CONTRACT.ShopID = COFFEESHOP.ShopID
        JOIN SUPPLIER ON CONTRACT.SupplierID = SUPPLIER.SupplierID""")
        data = mycursor.fetchall()

        return render_template('contracts.html', suppliers=suppliers, coffeeshops=coffeeshops, contracts=data)
    
    # Fetch the current values of the CONTRACT table

    mycursor.execute("""
        SELECT CONTRACT.ContractID, COFFEESHOP.ShopName, SUPPLIER.SupplierName
        FROM CONTRACT
        JOIN COFFEESHOP ON CONTRACT.ShopID = COFFEESHOP.ShopID
        JOIN SUPPLIER ON CONTRACT.SupplierID = SUPPLIER.SupplierID""")
    data = mycursor.fetchall()
   
    #Fetch the details of the contract to pre-fill the form
    sql = "SELECT * FROM CONTRACT WHERE ContractID = %s" % (contract_id)
    mycursor.execute(sql)
    data = mycursor.fetchone()
    mycursor.close()
    connection.close()
    print(data)

    return render_template('updatecontract.html', contract_details=data, suppliers=suppliers, coffeeshops=coffeeshops)


@app.route('/contract/delete/<int:contract_id>', methods=['POST'])  # Delete a contract
def delete_contract(contract_id):
    connection = dbconnection()
    mycursor = connection.cursor()

    sql = "DELETE FROM CONTRACT WHERE ContractID = %d" % (contract_id)
    mycursor.execute(sql)
    connection.commit()
    mycursor.close()
    connection.close()
    return redirect(url_for('manage_contract'))

@app.route('/employees', methods=['GET', 'POST'])
def manage_employee():
    connection = dbconnection()
    mycursor = connection.cursor()

    # Fetch all employees
    mycursor.execute("SELECT * FROM EMPLOYEE")
    employees = mycursor.fetchall()

    if request.method == 'POST':
        # Extract employee data from form
        employeeID = request.form['employeeID']
        employeeName = request.form['employeeName']
        shopID = request.form['shopID']
        managerID = request.form['managerID']
        
        # Insert new employee into the database
        mycursor.execute("INSERT INTO EMPLOYEE (EmployeeID, EmployeeName, ShopID, ManagerID) VALUES (%s, %s, %s, %s)", 
                         (employeeID, employeeName, shopID, managerID))
        connection.commit()

    mycursor.close()
    connection.close()
    return render_template('employees.html', employees=employees)

@app.route('/employees/update/<int:employee_id>', methods=['GET', 'POST'])
def update_employee(employee_id):
    connection = dbconnection()
    mycursor = connection.cursor()

    if request.method == 'POST':
        # Extract updated data from form
        employeeName = request.form['employeeName']
        shopID = request.form['shopID']
        managerID = request.form['managerID']

        # Update employee in the database
        mycursor.execute("UPDATE EMPLOYEE SET EmployeeName = %s, ShopID = %s, ManagerID = %s WHERE EmployeeID = %s", 
                         (employeeName, shopID, managerID, employee_id))
        connection.commit()
        return redirect(url_for('manage_employee'))

    # Fetch the current employee's details
    mycursor.execute("SELECT * FROM EMPLOYEE WHERE EmployeeID = %s", (employee_id,))
    employee = mycursor.fetchone()
    mycursor.close()
    connection.close()
    return render_template('updateemployee.html', employee=employee)

@app.route('/employees/delete/<int:employee_id>', methods=['POST'])
def delete_employee(employee_id):
    connection = dbconnection()
    mycursor = connection.cursor()

    # Delete employee from the database
    mycursor.execute("DELETE FROM EMPLOYEE WHERE EmployeeID = %s", (employee_id,))
    connection.commit()
    mycursor.close()
    connection.close()
    return redirect(url_for('manage_employee'))

@app.route('/menuitems', methods=['GET', 'POST'])
def manage_menuitem():
    connection = dbconnection()
    mycursor = connection.cursor()

    # Fetch all menu items
    mycursor.execute("SELECT * FROM MENU_ITEM")
    menu_items = mycursor.fetchall()

    # Fetch item categories
    mycursor.execute("SELECT ItemCategory FROM ITEM_CATEGORY")
    item_categories = mycursor.fetchall()

    if request.method == 'POST':
        # Extract menu item data from form
        itemID = request.form['itemID']
        itemPrice = request.form['itemPrice']
        itemCategory = request.form['itemCategory']
        
        # Insert new menu item into the database
        mycursor.execute("INSERT INTO MENU_ITEM (ItemID, ItemPrice, ItemCategory) VALUES (%s, %s, %s)", 
                         (itemID, itemPrice, itemCategory))
        connection.commit()

    mycursor.close()
    connection.close()
    return render_template('menuitems.html', menu_items=menu_items, item_categories=item_categories)

@app.route('/menuitems/update/<int:item_id>', methods=['GET', 'POST'])
def update_menuitem(item_id):
    connection = dbconnection()
    mycursor = connection.cursor()

    # Fetch item categories
    mycursor.execute("SELECT ItemCategory FROM ITEM_CATEGORY")
    item_categories = mycursor.fetchall()

    if request.method == 'POST':
        # Extract updated data from form
        itemPrice = request.form['itemPrice']
        itemCategory = request.form['itemCategory']

        # Update menu item in the database
        mycursor.execute("UPDATE MENU_ITEM SET ItemPrice = %s, ItemCategory = %s WHERE ItemID = %s", 
                         (itemPrice, itemCategory, item_id))
        connection.commit()
        return redirect(url_for('manage_menuitem'))

    # Fetch the current menu item's details
    mycursor.execute("SELECT * FROM MENU_ITEM WHERE ItemID = %s", (item_id,))
    menu_item = mycursor.fetchone()
    mycursor.close()
    connection.close()
    return render_template('updatemenuitem.html', menu_item=menu_item, item_categories=item_categories)

@app.route('/menuitems/delete/<int:item_id>', methods=['POST'])
def delete_menuitem(item_id):
    connection = dbconnection()
    mycursor = connection.cursor()

    # Delete menu item from the database
    mycursor.execute("DELETE FROM MENU_ITEM WHERE ItemID = %s", (item_id,))
    connection.commit()
    mycursor.close()
    connection.close()
    return redirect(url_for('manage_menuitem'))


if __name__ == '__main__':
    app.run(port=8000, debug=True, host="0.0.0.0")