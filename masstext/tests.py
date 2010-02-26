from django.test import TestCase, Client
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse

from masstext.models import PhoneNumber

class TextingTestCase(TestCase):
    def setUp(self):
        u1 = User(username='user1')
        u2 = User(username='user2')
        u1.save()
        u2.save()

        pn1 = PhoneNumber(owner=u1, number='9195555555')
        pn2 = PhoneNumber(owner=u2, number='9195555556')
        pn1.save()
        pn2.save()

    def test_mass_text_get(self):
        #tests that gets return nothing
        url = reverse('masstext')
        c = Client()
        r = c.get(url)
        self.assertEqual(r.content, "You don't get how this works, do you?")

    def test_mass_text_post(self):
        #tests that posts work
        url = reverse('masstext')
        c = Client()
        data = dict(
            From='9195555555',
            Body='This is a message.'
        )
        expected = ''.join('<?xmlversion="1.0"encoding="UTF-8"?><Response><Sms to="9195555556">user1 says: This is a message.</Sms></Response>'.split())
        r = c.post(url, data)
        received = ''.join(r.content.split())
        self.assertEqual(received, expected)

class PhoneNumberManagerTestCase(TestCase):
    def setUp(self):
        u1 = User(username='user1')
        u2 = User(username='user2')
        u1.save()
        u2.save()

        pn1 = PhoneNumber(owner=u1, number='9195555555')
        pn2 = PhoneNumber(owner=u2, number='9195555556')
        pn1.save()
        pn2.save()

    def test_get_reply_numbers_with_valid_number(self):
        #tests that a valid reply set is returned for a valid number
        numbers = PhoneNumber.objects.all().values()
        sender = numbers[0]['number']
        receiver = numbers[1]['number']
        reply_set = PhoneNumber.objects.get_reply_numbers(sender)
        self.assertEqual([receiver], reply_set)

    def test_get_reply_numbers_with_invalid_number(self):
        #tests that an invalid number gets no reply set
        invalid_number = '9198888888'
        expected_reply = [] 
        reply_set = PhoneNumber.objects.get_reply_numbers(invalid_number)
        self.assertEqual(reply_set, expected_reply)
