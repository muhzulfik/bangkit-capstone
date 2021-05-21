import flask
from flask import request, jsonify
import pymysql
from flaskext.mysql import MySQL

mysql = MySQL()

app = flask.Flask(__name__)
app.config["DEBUG"] = True
app.config['MYSQL_DATABASE_USER'] = 'root'
app.config['MYSQL_DATABASE_PASSWORD'] = ''
app.config['MYSQL_DATABASE_DB'] = 'task'
app.config['MYSQL_DATABASE_HOST'] = 'localhost'
mysql.init_app(app)

@app.route('/api/task', methods=['GET'])
def api_all():
    conn = mysql.connect()
    cur = conn.cursor(pymysql.cursors.DictCursor)
    cur.execute('''SELECT * FROM makanan;''')

    rv = cur.fetchall()

    for index in range(len(rv)):
        cur.execute('SELECT * FROM nutrisi WHERE id_makanan={};'.format(rv[index]["id_makanan"]))
        ukuran = cur.fetchall()
        rv[index]['ukuran'] = ukuran
        # print(rv[index])

    return jsonify(rv)

app.run()