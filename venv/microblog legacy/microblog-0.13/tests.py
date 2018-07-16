#!/usr/bin/env python
from datetime import datetime, timedelta
import unittest
from app import app, db
from app.models import User

# class ValidationError(Exception):
#     def __init__(self, message, errors):

#         # Call the base class constructor with the parameters it needs
#         super().__init__(message)

#         # Now for your custom code...
#         self.errors = errors

class UserModelCase(unittest.TestCase):
    def setUp(self):
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite://'
        db.create_all()

    def tearDown(self):
        db.session.remove()
        db.drop_all()

    def test_password_hashing(self):
        u = User(username='susan')
        u.set_password('cat')
        self.assertFalse(u.check_password('dog'))
        self.assertTrue(u.check_password('cat'))

    def test_avatar(self):
        u = User(username='john', email='john@example.com')
        self.assertEqual(u.avatar(128), ('https://www.gravatar.com/avatar/'
                                         'd4c74594d841139328695756648b6bd6'
                                         '?d=identicon&s=128'))
    def test_token_authentication(self):
        u = User(username='wololo')
        token = u.get_reset_password_token
        print('acc_pw_reset_token = ')
        print(str(token))
        result = u.verify_reset_password_token(token)
        if result == None:
            raise EnvironmentError

if __name__ == '__main__':
    unittest.main(verbosity=2)
