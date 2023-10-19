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
        description = datos.get('descripcio')
        price       = int(datos.get('preu'))
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

@app.route("/products/delete/<int:product_id>", methods=['GET', 'POST'])
def delete(product_id):
    with get_db() as conn:
        if request.method == 'POST':
            sql = "DELETE FROM products WHERE id = ?"
            conn.execute(sql, (product_id,))
            return redirect(url_for('item_list'))
        else:
            sql = "SELECT * FROM products WHERE id = ?"
            res = conn.execute(sql, (product_id,))
            product = res.fetchone()
            if product:
                return render_template('products/delete.html', product=product)
            else:
                return "Producto no encontrado", 404
            
@app.route("/products/update/<int:product_id>", methods=['GET', 'POST'])
def update(product_id):
    with get_db() as conn:
        if request.method == 'POST':
            datos       = request.form
            title       = datos.get('nom')
            description = datos.get('descripcio')
            price       = int(datos.get('preu'))
            foto        = 'hola' # O modifica esto según la lógica de tu aplicación
            updated     = datetime.datetime.now()

            sql = """
            UPDATE products 
            SET title = ?, description = ?, photo = ?, price = ?, updated = ? 
            WHERE id = ?
            """
            conn.execute(sql, (title, description, foto, price, updated, product_id))
            return redirect(url_for('item_list'))

        else:
            sql = "SELECT * FROM products WHERE id = ?"
            res = conn.execute(sql, (product_id,))
            product = res.fetchone()
            if product:
                return render_template('products/update.html', product=product)
            else:
                return "Producto no encontrado", 404