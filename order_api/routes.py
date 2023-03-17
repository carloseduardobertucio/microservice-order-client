from flask import jsonify, request
from config import app, db
from models import Product, Order, OrderItem


@app.route('/products', methods=['GET'])
def get_all_products():

    products = Product.query.all()
    return jsonify({'products': [product.to_dict() for product in products]}), 200

@app.route('/product', methods=['GET'])
def get_product_by_id():

    product = Product.query.get(request.args.get('id'))
    if product is None:
        return jsonify({'error': 'Product not found'}), 404
    return jsonify(product.to_dict()), 200

@app.route('/create-product', methods=['POST'])
def create_product():

    data = request.get_json()
    new_product = Product(**data)
    db.session.add(new_product)
    db.session.commit()
    return jsonify({'message': 'Product created successfully'}), 201

@app.route('/update-product', methods=['PUT'])
def update_product():

    data = request.get_json()
    product = Product.query.get(data.get('id'))
    if product is None:
        return jsonify({'error': 'Product not found'}), 404
    for key, value in data.items():
        setattr(product, key, value)
    db.session.commit()
    return jsonify(product.to_dict()), 200

@app.route('/delete-product', methods=['DELETE'])
def delete_product():

    product = Product.query.get(request.args.get('id'))
    if product is None:
        return jsonify({'error': 'Product not found'}), 404
    db.session.delete(product)
    db.session.commit()
    return {"message": "product deleted successfully"}, 200

@app.route('/create-order', methods=['POST'])
def create_order():

    data = request.get_json()
    products_ids = data.get('products_ids')
    register_id = data.get('register_id')

    new_order = Order(register_id=register_id)
    db.session.add(new_order)

    for product_id in products_ids:

        product = Product.query.get(product_id)
        if product is None:
            db.session.rollback()
            return jsonify({'error': 'Product not found'}), 404
        
        orders = Order.query.order_by(Order.id.desc()).all()
        orders = list(filter(lambda order: order.to_dict()['register_id'] == register_id, orders))
        current_order = orders[0]

        new_order_items = OrderItem(
            order_id=getattr(current_order, "id"),
            product_id=getattr(product, "id"),
        )

        db.session.add(new_order_items)
    
    db.session.commit()
    return {"message": "order created successfully"}, 201

@app.route('/get-order', methods=['GET'])
def get_order():

    register_id = request.args.get('register_id')
    
    orders = Order.query.order_by(Order.id.desc()).all()
    orders = list(filter(lambda order: order.to_dict()['register_id'] == register_id, orders))

    if orders is None:
        return jsonify({'error': 'Orders not found'}), 404
    
    order_id = getattr(orders[0], "id")
    order_items = OrderItem.query.filter_by(order_id=order_id).all()

    products_list = []

    for order_item in order_items:
        product_id = getattr(order_item, "product_id")
        product = Product.query.get(product_id)
        products_list.append(product.to_dict())

    response = {
        "order_id": order_id,
        "products": products_list
    }

    return response, 200




















if __name__ == '__main__':
    app.run(debug=True)
