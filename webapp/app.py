from flask import Flask, request, render_template

app = Flask(__name__)

@app.route('/', methods=['GET']) #display page1 data
def display_page1():
    return render_template('page1.html')

@app.route('/process_data', methods=['POST']) #process data from page 1 to page 2
def process_data():
    field1 = request.form['field1']
    field2 = request.form['field2']
    field3 = request.form['field3']
    #pass entered fields to page2
    return render_template('page2.html', field1=field1, field2=field2, field3=field3)


if __name__ == '__main__':
    app.run(port=8000, debug=True, host="0.0.0.0")