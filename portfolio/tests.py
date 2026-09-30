from django.test import TestCase, Client
from .models import Message
class PortfolioTests(TestCase):
    def test_home_and_contact(self):
        self.assertContains(self.client.get('/'), 'Abhishek Kumar')
        response=self.client.post('/', {'name':'Visitor','email':'hello@example.com','message':'Hello'})
        self.assertEqual(response.status_code,302)
        self.assertEqual(Message.objects.count(),1)
        self.client.post('/', {'name':'Visitor','email':'bad','message':'Hi'})
        self.assertEqual(Message.objects.count(),1)
    def test_shared_pulse_and_validation(self):
        response=self.client.post('/api/pulses/',data={'x':0.2,'y':0.4},content_type='application/json')
        self.assertEqual(response.status_code,200)
        other=Client()
        self.assertEqual(len(other.get('/api/pulses/').json()['pulses']),1)
        self.assertEqual(other.post('/api/pulses/',data={'x':2,'y':0},content_type='application/json').status_code,400)
    def test_csrf(self):
        c=Client(enforce_csrf_checks=True)
        self.assertEqual(c.post('/api/pulses/',data={'x':0.2,'y':0.4},content_type='application/json').status_code,403)
