from flask import Blueprint, redirect, url_for, render_template, request, Flask
from .models import categoria, product, user
import sqlite3, datetime, os
from werkzeug.utils import secure_filename
from . import db_manager as db

app = Flask(__name__)
UPLOAD_FOLDER = './upload'
DATABASE = 'database.db'
ALLOWED_EXTENSIONS = {'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'}
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

main_bp = Blueprint(
    "main_bp", __name__, template_folder="templates", static_folder="static"
)

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def get_db():
    # sqlite3_database_path = DATABASE
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row
    return conn

@main_bp.route("/")
def hello_world():
    return render_template('hello.html')

@main_bp.route("/products/list")
def list():
    items = db.session.query(product).all()
    return render_template("products/list.html",items = items)

@main_bp.route("/products/create", methods = ['GET','POST'])
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

        return redirect(url_for('main_bp.list'))
    else:
        return render_template('products/create.html')
    
@main_bp.route("/products/read/<int:id>")
def read(id):
    # app.logger.debug("INT" if (type(id) is int) else "OTHER")
    items = db.session.query(product).where(product.id == id)
    return render_template("products/list.html",items = items)


@main_bp.route("/products/update/<int:id>", methods = ['GET', 'POST'])
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
        return redirect(url_for('main_bp.list'))

@main_bp.route("/products/delete/<int:id>", methods = ['GET', 'POST'])  
def delete(id):
    item = db.session.query(product).filter(product.id == id).one()

    db.session.delete(item)
    db.session.commit()

    return redirect(url_for('main_bp.list'))