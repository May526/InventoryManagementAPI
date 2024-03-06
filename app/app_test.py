from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DB_URI'] = 'mysql+pymysql://username:password@localhost/mydatabase'
db = SQLAlchemy(app)

class Item(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String(50), nullable = False)
    amount = db.Column(db.Integer, nullable = False)
    price = db.Column(db.Integer, nullable = False)


@app.route('/v1/stocks', methods = ['POST'])
def create_item():
    data = request.get_json()
    name = data.get('name')
    amount = data.get('amounta')

    item = Item.query.filter_by(name = name).first()
    if item:
        item.amount += amount
    else:
        item = Item(name=name, amount=amount)
        db.session.add(item)
    pass

    db.session.commit()

    response = {
        'name' : name,
        'amount' : amount
    }

    return jsonify(response), 201, {'Location': f'http://54.250.158.52:80/v1/stocks/{name}'}

@app.route('/v1/stocks(/:name)', methods = ['GET'])
def get_item():

    pass

@app.route('/v1/sales', methods = ['POST'])
def sell_item():

    pass

@app.route('/v1/sales', methods = ['GET'])
def sell_check_item():

    pass

@app.route('/v1/stocks', methods = ['DELETE'])
def delete_item():

    pass



