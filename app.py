from random import randint, choice

from flask import Flask, render_template, request, redirect, url_for

from models import db, Products, Inventory, Locations

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:pass@localhost:3306/mysql_bd'
db.init_app(app)

locations = ['Ашан', 'Лента', 'Метро']


@app.cli.command('init-db')
def init_db():
    db.create_all()
    print("Database created")


@app.cli.command('drop-db')
def drop_db():
    db.drop_all()


@app.cli.command('load-data')
def load_data():
    for i in range(1,3):
        location = Locations(
            name=f"Location {i}")
        db.session.add(location)
    for i in range(1,15):
        product = Products(
            name=f'Товар {i}',
            description=f'Описание{i}',
            price=randint(1, 100)
        )
        db.session.add(product)
    for i in range(1,15):
        inventory = Inventory(
            product_id=i,
            location_id= randint(1, len(locations)),
            quantity=i + 2
        )
        db.session.add(inventory)
        db.session.commit()


@app.route('/', methods=['POST', 'GET'])
def index():
    inventory = Inventory.query.order_by(Inventory.product_id).all()
    locs = Locations.query.all()
    if request.method == 'POST':
        add_ = request.form.getlist('add')
        del_ = request.form.getlist('del')
        id_ = request.form.getlist('_id')
        add_ = (''.join(add_))
        del_ = (''.join(del_))
        id_ = (''.join(id_))
        print(id_)
        if add_ > del_:
            name = add_
        else:
            name = del_
        print(name)
        product = Inventory.query.filter_by(product_id=id_).first()
        if name == 'Добавить':
            product.quantity += 1
        elif name == 'Удалить':
            if product.quantity > 0:
                product.quantity -= 1
        db.session.commit()
        return redirect(url_for('index'))
    else:
        return render_template('table.html', inventory=inventory, locations=locs)


@app.post('/add-product/')
def add_product():
    send = request.form.getlist('send')
    print(send)
    location = Locations(
        name=request.form.get('loc_name')
    )
    db.session.add(location)
    product = Products(
        name=request.form.get('product_name'),
        description=request.form.get('description'),
        price=request.form.get('price'),
    )
    db.session.add(product)
    inventory = Inventory(
        quantity=request.form.get('quantity'),
        product_id=product.id,
        location_id = request.form.get('loc.id')
    )
    db.session.add(inventory)
    db.session.commit()
    # return render_template('table.html', inventory=Inventory.query.all())


if __name__ == '__main__':
    app.run(debug=True)
