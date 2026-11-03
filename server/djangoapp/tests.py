import json
from django.test import TestCase
from django.contrib.auth.models import User
from .models import CarMake, CarModel


class AccountInventoryTests(TestCase):
    def test_registration_login_logout(self):
        payload = {'userName': 'driver', 'firstName': 'Test', 'lastName': 'Driver',
                   'email': 'driver@example.com', 'password': 'ReviewCar2026'}
        response = self.client.post('/djangoapp/registration', json.dumps(payload),
                                    content_type='application/json')
        self.assertEqual(response.status_code, 201)
        self.assertTrue(User.objects.get(username='driver').check_password(payload['password']))
        response = self.client.get('/djangoapp/logout')
        self.assertEqual(response.json()['status'], 'Logged out')
        response = self.client.post('/djangoapp/login', json.dumps(payload),
                                    content_type='application/json')
        self.assertEqual(response.json()['status'], 'Authenticated')
        self.assertEqual(response.json()['firstName'], 'Test')

    def test_bad_login_and_anonymous_review_rejected(self):
        response = self.client.post('/djangoapp/login',
                                    json.dumps({'userName': 'missing', 'password': 'bad'}),
                                    content_type='application/json')
        self.assertEqual(response.status_code, 401)
        response = self.client.post('/djangoapp/add_review', '{}', content_type='application/json')
        self.assertEqual(response.status_code, 401)

    def test_inventory_returns_related_make_and_model(self):
        make = CarMake.objects.create(name='Toyota', description='Toyota vehicles')
        CarModel.objects.create(car_make=make, name='Camry', type='Sedan', year=2023)
        response = self.client.get('/djangoapp/get_cars')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()['CarModels'][0]['CarMake'], 'Toyota')
        self.assertEqual(response.json()['CarModels'][0]['CarModel'], 'Camry')
