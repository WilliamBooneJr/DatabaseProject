#!/usr/bin/python3

from flask import Flask, render_template, request
import mysql.connector, os


app = Flask(__name__)


@app.route('/', methods=['GET'])
def showTable():
    """This is vulnerable to the following SQL injection:
    http://localhost:8000/?id=1' or 1=1 --%20"""
    connection = mysql.connector.connect(
        host=os.environ['SQL_HOST'],
        user=os.environ['SQL_USER'],
        password=os.environ['SQL_PWD'],
        db=os.environ['SQL_DB']
    )
    mycursor = connection.cursor()

    id = request.args.get('id') 
    if not id.isdigit():
        return "Invalid input", 400 #sanitize the input to make sure it is digit
        

    # Fetch the value from the table with a matching ID
    #sqlstring = "Select * from speaker where id='{}'".format(id)
    sqlstring = "Select * from speaker where id = %s" #parameterize the query with a placeholder
    print(sqlstring)
    mycursor.execute(sqlstring, (id,)) #pass the the value
    myresult = mycursor.fetchall()
    mycursor.close()
    connection.close()
    output = "<br />\n".join([str(row) for row in myresult])
    return output


if __name__ == '__main__':
    app.run(port=8000, debug=True, host="0.0.0.0")