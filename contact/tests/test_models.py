from django.test import TestCase
from contact.models import Contact

"""Test case utilisé pour tester les Contact models."""
class ContactModelTest(TestCase):
    def setUp(self):
        Contact.objects.create(first_name="l",
                               last_name="sl",
                               email="lsl@gmail.com",
                               message="Very cool website !"
        )
    def test_fname_Contact(self):
        contact_info= Contact.objects.get(first_name="l")
        field_label = Contact._meta.get_field('first_name').verbose_name
        self.assertEquals(field_label, 'first name')

    def test_lname_Contact(self):
        contact_info= Contact.objects.get(first_name="l")
        field_label = Contact._meta.get_field('last_name').verbose_name
        self.assertEquals(field_label, 'last name')

    def test_email_Contact(self):
        contact_info= Contact.objects.get(first_name="l")
        field_label = Contact._meta.get_field('email').verbose_name
        self.assertEquals(field_label, 'email')

    def test_message_Contact(self):
        contact_info= Contact.objects.get(first_name="l")
        field_label = Contact._meta.get_field('message').verbose_name
        self.assertEquals(field_label, 'message')