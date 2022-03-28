from flask import Flask, render_template, request, redirect, url_for
import fdb

app = Flask(__name__)
con = fdb.connect(dsn='D:/Narine/Firebird/DATA.FDB', user='sysdba', password='masterkey', charset='UTF8')
cur = con.cursor()


@app.route('/warning')
def login_err():
    return render_template('login_err.html')


@app.route('/')
def index():
    return render_template('index.html')

@app.route('/table')
def nameerr():
    return render_template('table.html')


@app.route('/', methods=['POST'])
def login_info():
    login = request.form.get('login').strip()
    password = request.form.get('password').strip()
    cur.execute("""SELECT UUID FROM USER3 WHERE  LOGIN=? and PASSWORD=?""", (login, password))
    result = cur.fetchall()

    if result:
        cur.execute("""SELECT REQUEST_NUMBER, REQUEST_DESCRIPTION, START_DATE FROM REQUEST 
                       WHERE  EMPLOYEE_UUID=? AND END_DATE IS NULL""", result[0])
        res = cur.fetchall()
        for i in res:
            req_num = i[0]
            req_description = i[1]
            start_date = i[2]

            @app.route('/table')
            def table():
                return render_template("table.html", value1=req_num, value2=req_description, value3=start_date)
    else:
        return login_err()

if __name__ == "__main__":
    app.run(debug=True, port=80)