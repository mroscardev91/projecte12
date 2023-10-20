from flask import Flask ,render_template ,g ,request, redirect, url_for
import sqlite3, datetime, os
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import UniqueConstraint
from werkzeug.utils import secure_filename

UPLOAD_FOLDER = './upload'
ALLOWED_EXTENSIONS = {'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'}

app = Flask(__name__)
DATABASE = 'database.db'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# ruta absoluta d'aquesta carpeta
basedir = os.path.abspath(os.path.dirname(__file__)) 

# paràmetre que farà servir SQLAlchemy per a connectar-se
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///" + basedir + "/database.db"
# mostre als logs les ordres SQL que s'executen
app.config["SQLALCHEMY_ECHO"] = True

db = SQLAlchemy()
db.init_app(app)
now = datetime.datetime.utcnow

class categoria(db.Model):
    __tablename__ = "categories"
    id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    name = db.Column(db.Text, nullable=False)
    slug = db.Column(db.Text, nullable=False)

class product(db.Model):
    __tablename__ = "products"
    id              = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title           = db.Column(db.Text, nullable=False)
    description     = db.Column(db.Text, nullable=False)
    photo           = db.Column(db.Text, nullable=False)
    price           = db.Column(db.Numeric(10,2), nullable=False)
    category_id     = db.Column(db.Integer, db.ForeignKey("categories.id"), nullable=False)
    seller_id       = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    created         = db.Column(db.DateTime, default=now)
    updated         = db.Column(db.DateTime, default=now)


# taula users

class user(db.Model):
    __tablename__   = "users"
    id              = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name            = db.Column(db.Text, nullable=False, unique=True)
    email           = db.Column(db.Text, nullable=False, unique=True)
    password        = db.Column(db.Text, nullable=False)
    created         = db.Column(db.DateTime, default=now)
    update          = db.Column(db.DateTime, default=now)

# class Order(db.Model):
#     __tablename__ = "orders"
#     id = db.Column(db.Integer, autoincrement=True, primary_key=True)
#     product_id = db.Column(db.Integer, nullable=False)
#     buyer_id = db.Column(db.Integer, nullable=False)
#     created = db.Column(db.DateTime, default=now)
#     UniqueConstraint("product_id", "buyer_id", name="uc_product_buyer")
#     category_id = db.Column(db.ForeignKey("categories.id"), nullable=False)
#     seller_id = db.Column(db.ForeignKey("users.id"), nullable=False)

# class ConfirmedOrder(db.Model):
#     __tablename__ = "confirmed_orders"
#     order_id = db.Column(db.Integer, primary_key=True)
#     created = db.Column(db.DateTime, default=now)
#     order_id = db.Column(db.ForeignKey("orders.id"), nullable=False)


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def get_db():
    # sqlite3_database_path = DATABASE
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row
    return conn

@app.route("/")
def hello_world():
    return render_template('hello.html')

@app.route("/products/list")
def list():
    items = db.session.query(product).all()
    return render_template("products/list.html",items = items)

@app.route("/products/create", methods = ['GET','POST'])
def create():
    if request.method == 'POST':
        datos           = request.form
        title           = datos.get('title')
        description     = datos.get('description')
        price           = int(datos.get('price'))
        fotoBD          = request.files['photo'].filename
        archivo         = request.files['photo']
        created         = datetime.datetime.now()
        updated         = datetime.datetime.now()         
        filename        = secure_filename(archivo.filename)
        archivo.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        

        nou_item = product()
        nou_item.title  = title
        nou_item.description  = description
        nou_item.price = price
        nou_item.photo  = fotoBD
        nou_item.created  = created
        nou_item.updated = updated

        db.session.add(nou_item)
        db.session.commit()

        return redirect(url_for('list'))
    else:
        return render_template('products/create.html')
    
@app.route("/products/read/<int:id>")
def read(id):
    # app.logger.debug("INT" if (type(id) is int) else "OTHER")
    items = db.session.query(product).where(product.id == id)
    return render_template("products/list.html",items = items)


@app.route("/products/update/<int:id>", methods = ['GET', 'POST'])
def update(id):
    item = db.session.query(product).filter(product.id == id).one()
    if request.method == 'GET':
        # with get_db() as conn:
        #     results = conn.execute("SELECT * FROM products WHERE id = " + str(id))
        #     items = results.fetchall()

        return render_template('products/update.html', item = item)
    
    elif request.method == 'POST':
        # with get_db() as conn:
        datos           = request.form
        description     = datos.get('description')
        title           = datos.get('title')
        price           = float(datos.get('price'))
        foto            = request.files['photo'].filename
        updated         = datetime.datetime.now()
            # conn.execute("UPDATE products SET title = ?, description = ?, photo = ?, price = ?, updated = ? WHERE id = ?", 
            #     (title, description, foto, price, updated, id))
        item.title          = title
        item.description    = description
        item.price          = price
        item.photo          = foto
        item.updated        = updated

        # update!
        db.session.add(item)
        db.session.commit()
        return redirect(url_for('list'))

@app.route("/products/delete/<int:id>", methods = ['GET', 'POST'])  
def delete(id):
    item = db.session.query(product).filter(product.id == id).one()

    db.session.delete(item)
    db.session.commit()

    return redirect(url_for('list'));

