from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
import os
print("Hiiii")
app = Flask(__name__)

# Configure the PostgreSQL database
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://myuser:mypassword@postgres:5432/mydatabase'
#os.environ.get('DATABASE_URL')
db = SQLAlchemy(app)

# Define a model for your data
class Item(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)

@app.route('/populate', methods=['POST'])
def populate_data():
    # Sample data to insert
    sample_data = [
        {'name': 'Item 1'},
        {'name': 'Item 2'},
        {'name': 'Item 3'}
    ]

    for data in sample_data:
        new_item = Item(name=data['name'])
        db.session.add(new_item)

    db.session.commit()
    return jsonify({'message': 'Example data inserted successfully'}), 201

@app.route('/items', methods=['GET'])
def get_items():
    items = Item.query.all()
    return jsonify([item.name for item in items])

@app.route('/items/<int:item_id>', methods=['GET'])
def get_item(item_id):
    item = Item.query.get(item_id)
    if item:
        return jsonify({'name': item.name})
    else:
        return jsonify({'message': 'Item not found'}), 404

@app.route('/items', methods=['POST'])
def create_item():
    data = request.get_json()
    name = data.get('name')
    if name:
        new_item = Item(name=name)
        db.session.add(new_item)
        db.session.commit()
        return jsonify({'message': 'Item created successfully'}), 201
    else:
        return jsonify({'message': 'Invalid input data'}), 400

@app.route('/items/<int:item_id>', methods=['PUT'])
def update_item(item_id):
    item = Item.query.get(item_id)
    if item:
        data = request.get_json()
        new_name = data.get('name')
        if new_name:
            item.name = new_name
            db.session.commit()
            return jsonify({'message': 'Item updated successfully'})
        else:
            return jsonify({'message': 'Invalid input data'}), 400
    else:
        return jsonify({'message': 'Item not found'}), 404

@app.route('/items/<int:item_id>', methods=['DELETE'])
def delete_item(item_id):
    item = Item.query.get(item_id)
    if item:
        db.session.delete(item)
        db.session.commit()
        return jsonify({'message': 'Item deleted successfully'})
    else:
        return jsonify({'message': 'Item not found'}), 404

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
