import unittest
import json
from config import app, db
from models import Product


class TestRoutes(unittest.TestCase):

    def setUp(self):
        self.app = app.test_client()
        self.app.testing = True

    def test_get_all_products(self):
        response = self.app.get('/products')
        data = json.loads(response.get_data(as_text=True))
        self.assertEqual(response.status_code, 200)
        self.assertIsInstance(data, dict)
        self.assertIn('products', data)
        self.assertIsInstance(data['products'], list)

    def test_get_product_by_id(self):
        
        product = Product(name='Test Product', price=10.0)
        db.session.add(product)
        db.session.commit()

       
        response = self.app.get('/product?id={}'.format(product.id))
        data = json.loads(response.get_data(as_text=True))
        self.assertEqual(response.status_code, 200)
        self.assertIsInstance(data, dict)
        self.assertIn('id', data)
        self.assertIn('name', data)
        self.assertIn('price', data)
        self.assertEqual(data['id'], product.id)
        self.assertEqual(data['name'], product.name)
        self.assertEqual(data['price'], float(product.price))

    def test_get_product_by_id_not_found(self):
        response = self.app.get('/product?id=99999')
        data = json.loads(response.get_data(as_text=True))
        self.assertEqual(response.status_code, 404)
        self.assertIsInstance(data, dict)
        self.assertIn('error', data)
        self.assertEqual(data['error'], 'Product not found')

    def test_create_product(self):
        data = {'name': 'Test Product', 'price': 10.0}
        response = self.app.post('/create-product', json=data)
        data = json.loads(response.get_data(as_text=True))
        self.assertEqual(response.status_code, 201)
        self.assertIsInstance(data, dict)
        self.assertIn('message', data)
        self.assertEqual(data['message'], 'Product created successfully')

    def test_update_product(self):
    
        product = Product(name='Test Product', price=10.0)
        db.session.add(product)
        db.session.commit()

   
        data = {'id': product.id, 'name': 'Updated Product', 'price': 20.0}
        response = self.app.put('/update-product', json=data)
        data = json.loads(response.get_data(as_text=True))
        self.assertEqual(response.status_code, 200)
        self.assertIsInstance(data, dict)
        self.assertIn('id', data)
        self.assertIn('name', data)
        self.assertIn('price', data)
        self.assertEqual(data['id'], product.id)
        self.assertEqual(data['name'], 'Updated Product')
        self.assertEqual(data['price'], 20.0)

    def test_update_product_not_found(self):
        data = {'id': 99999, 'name': 'Updated Product', 'price': 20.0}
        response = self.app.put('/update-product', json=data)
        data = json.loads(response.get_data(as_text=True))
        self.assertEqual(response.status_code, 404)
        self.assertIsInstance(data, dict)
        self.assertIn('error', data)
        self.assertEqual(data['error'], 'Product not found')

    def test_delete_product(self):
        product = Product(name='Test Product', price=10.0)
        db.session.add(product)
        db.session.commit()
        response = self.client.delete(f'/delete-product?id={product.id}')
        data = response.get_json()
        self.assertEqual(response.status_code, 200) 
        self.assertEqual(data.get('message'), 'product deleted successfully')
        deleted_product = Product.query.get(product.id)
        self.assertIsNone(deleted_product)