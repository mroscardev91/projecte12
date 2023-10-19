from flask import Flask, render_template , g, request, url_for, abort, redirect
import sqlite3, datetime

app = Flask(__name__)
DATABASE = 'database.db'

@app.route("/")
def hello_world():
    return render_template("hello.html")

def get_db():
    con = sqlite3.connect(DATABASE)
    con.row_factory = sqlite3.Row
    return con

@app.route("/products/list")
def item_list():
      with get_db() as con:
        res = con.execute("SELECT * FROM products ORDER BY id ASC")
        items = res.fetchall()
      
      return render_template("products/list.html",items = items)



@app.route("/products/create", methods = ['GET','POST'])
def create():
    if request.method == 'POST':
        datos       = request.form
        title       = datos.get('nom')
        description = datos.get('description')
        price       = int(datos.get('price'))
        foto        = 'hola'
        created     = datetime.datetime.now()
        updated     = datetime.datetime.now()
        
        with get_db() as conn:
            sql = "INSERT INTO products (title, description, photo, price, created, updated) VALUES (?, ?, ?, ?, ?, ?)"
            # app.logger.info('SQL: %s', sql)
            conn.execute(sql, (title, description, foto, price, created, updated))
        return redirect(url_for('list'))
    else:
        return render_template('products/create.html')
    
@app.route("/products/read/<int:id>")
def read(id):
    app.logger.debug("INT" if (type(id) is int) else "OTHER")
    with get_db() as conn:
        sql = "SELECT * FROM products WHERE id = " + str(id)
        resultat = conn.execute(sql)
        items = resultat.fetchall()
    return render_template("products/list.html",items = items)

