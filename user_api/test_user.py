from flask import json
from models import app, db
import unittest
from models import User

class UserTestCase(unittest.TestCase):

    def setUp(self):
        app.config['TESTING'] = True
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
        self.app = app.test_client()
        db.drop_all()
        db.create_all()

    def tearDown(self):
        db.session.remove()
        db.drop_all()

    def test_create_user(self):
       #Testando a criação de um usuário
        user_data = {
            'name': 'Thiago Abilio',
            'email': 'thiagoabilio@gmail.com'
        }
        response = self.app.post('/create-user', json=user_data)
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.data.decode(), 'user created successfully.')

        #Teste para recuperar usuário criado
        response = self.app.get('/userid=1')
        self.assertEqual(response.status_code, 200)
        expected_data = {
            'id': 1,
            'name': 'Thiago Abilio',
            'email': 'thiagoabilio@gmail.com'
        }
        self.assertDictEqual(json.loads(response.data.decode()), expected_data)

    def test_get_users(self):
        #Teste recuperando todos os usuários
        user1 = User(name='Thiago Abilio', email='thiagoabilio@gmail.com')
        user2 = User(name='Carlos Eduardo', email='carlosedu@gmail.com')
        db.session.add(user1)
        db.session.add(user2)
        db.session.commit()

        response = self.app.get('/users')
        self.assertEqual(response.status_code, 200)
        expected_data = {
            'users': [
                {
                    'id': user1.id,
                    'name': user1.name,
                    'email': user1.email
                },
                {
                    'id': user2.id,
                    'name': user2.name,
                    'email': user2.email
                }
            ]
        }
        self.assertDictEqual(json.loads(response.data.decode()), expected_data)

    def test_update_user(self):
        # Teste atualizando usuários 
        user = User(name='Carlos Eduardo', email='carlosedu@gmail.com')
        db.session.add(user)
        db.session.commit()

        update_data = {
            'id': user.id,
            'name': 'Nikholas Martins',
            'email': 'nikholasmartins@gmail.com'
        }
        response = self.app.put('/update-user', json=update_data)
        self.assertEqual(response.status_code, 200)

        #Testa a recuperação do usuário atualizado
        response = self.app.get('/userid=1')
        self.assertEqual(response.status_code, 200)
        expected_data = {
            'id': user.id,
            'name': 'Nikholas Martins',
            'email': 'nikholasmartins@gmail.com'
        }
        self.assertDictEqual(json.loads(response.data.decode()), expected_data)

    def test_delete_user(self):
        #Teste para deletar usuário existente
        user = User(name='Thiago Abilio', email='thiagoabilio@gmail.com')
        db.session.add(user)
        db.session.commit()

        response = self.app.delete('/delete-userid=1')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(json.loads(response.data.decode()), {'message': 'user deleted successfully'})

        #Testa a recuperação de usuário deletado
        response = self.app.get('/userid=1')
        self.assertEqual(response.status_code, 404)
        expected_data = {'error': 'User not found'}
        self.assertDictEqual(json.loads)

print("Todos os testes foram aprovados.")