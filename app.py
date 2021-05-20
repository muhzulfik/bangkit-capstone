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

def dict_factory(cursor, row):
    d = {}
    for idx, col in enumerate(cursor.description):
        d[col[0]] = row[idx]
    return d


@app.route('/', methods=['GET'])
def home():
    return '''<h1>Distant Reading Archive</h1>
<p>A prototype API for distant reading of science fiction novels.</p>'''


@app.route('/api/v1/resources/books/all', methods=['GET'])
def api_all():
    conn = mysql.connect()
    cur = conn.cursor(pymysql.cursors.DictCursor)
    cur.execute('SELECT * FROM makanan WHERE id_size=1;')

    rv = cur.fetchall()

    for index in range(len(rv)):
        cur.execute('SELECT * FROM nutrisi WHERE id_makanan={};'.format(rv[index]["id_size"]))
        ukuran = cur.fetchall()
        rv[index]['ukuran'] = ukuran
        # print(rv[index])

    return jsonify(rv)

    # thisdict =	{
    #     "id": 1,
    #     "nama": "ayam goreng",
    #     }

    # thisdict["ukuran"] =  [{
    #         "id": 1,
    #         "value": "1 buah",
    #         "energi": 391,
    #         "lemak": 21.82,
    #         "protein": 32.9,
    #         "karbohidrat": 16.15
    #     },
    #     {
    #         "id": 2,
    #         "value": "1 porsi",
    #         "energi": "781 kkal",
    #         "lemak": "43.64 g",
    #         "protein": "65.8 g",
    #         "karbohidrat": "32.29 g"
    #     },
    #     {
    #         "id": 3,
    #         "value": "100 gram",
    #         "energi": "260 kkal",
    #         "lemak": "14.45 g",
    #         "protein": "21.93 g",
    #         "karbohidrat": "10.76 g"
    #     }]

    # return jsonify(thisdict)