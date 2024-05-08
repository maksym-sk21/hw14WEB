import unittest
from unittest.mock import MagicMock

from sqlalchemy.orm import Session

from faker import Faker

from rest_api.src.database.models import Contact, User
from rest_api.src.schemas import ContactCreate, ContactUpdate, Contact
from rest_api.src.repository.contacts import (create_contact, get_contact, get_contacts, delete_contact, update_contact)


fake = Faker()


class TestContacts(unittest.IsolatedAsyncioTestCase):

    def setUp(self):
        self.session = MagicMock(spec=Session)
        self.user = User(id=1)

    async def test_get_contacts(self):
        contacts = [Contact(first_name=fake.first_name(),
                            last_name=fake.last_name(),
                            email=fake.email(),
                            phone_number=fake.phone_number(),
                            birthday=fake.date_of_birth(),
                            id=1),
                    Contact(first_name=fake.first_name(),
                            last_name=fake.last_name(),
                            email=fake.email(),
                            phone_number=fake.phone_number(),
                            birthday=fake.date_of_birth(),
                            id=1),
                    Contact(first_name=fake.first_name(),
                            last_name=fake.last_name(),
                            email=fake.email(),
                            phone_number=fake.phone_number(),
                            birthday=fake.date_of_birth(),
                            id=1)]
        self.session.query().filter().offset().limit().all.return_value = contacts
        result = get_contacts(skip=0, limit=10, user=self.user, db=self.session)
        self.assertEqual(result, contacts)

    async def test_get_contact_found(self):
        contact = Contact(first_name=fake.first_name(),
                          last_name=fake.last_name(),
                          email=fake.email(),
                          phone_number=fake.phone_number(),
                          birthday=fake.date_of_birth(),
                          id=1)
        self.session.query().filter().first.return_value = contact
        result = get_contact(contact_id=1, user=self.user, db=self.session)
        self.assertEqual(result, contact)

    async def test_get_contact_not_found(self):
        self.session.query().filter().first.return_value = None
        result = get_contact(contact_id=1, user=self.user, db=self.session)
        self.assertIsNone(result)

    async def test_create_contact(self):
        body = ContactCreate(first_name=fake.first_name(),
                             last_name=fake.last_name(),
                             email=fake.email(),
                             phone_number=fake.phone_number(),
                             birthday=fake.date_of_birth())
        contacts = [Contact(id=1,
                            user_id=1,
                            first_name=fake.first_name(),
                            last_name=fake.last_name(),
                            email=fake.email(),
                            phone_number=fake.phone_number(),
                            birthday=fake.date_of_birth()),
                    Contact(id=2,
                            user_id=1,
                            first_name=fake.first_name(),
                            last_name=fake.last_name(),
                            email=fake.email(),
                            phone_number=fake.phone_number(),
                            birthday=fake.date_of_birth())]
        self.session.query().filter().all.return_value = contacts
        result = create_contact(contact=body, current_user=self.user, db=self.session)
        self.assertEqual(result.first_name, body.first_name)
        self.assertTrue(hasattr(result, "id"))

    async def test_remove_contact_found(self):
        contact = Contact(first_name=fake.first_name(),
                          last_name=fake.last_name(),
                          email=fake.email(),
                          phone_number=fake.phone_number(),
                          birthday=fake.date_of_birth(),
                          id=1)
        self.session.query().filter().first.return_value = contact
        self.session.commit.return_value = None
        result = delete_contact(contact_id=1, user=self.user, db=self.session)
        self.assertEqual(result, True)

    async def test_remove_contact_not_found(self):
        result = delete_contact(contact_id=1, user=self.user, db=self.session)
        self.session.query().filter().first.return_value = result
        self.assertEqual(result, True)

    async def test_update_contact_found(self):
        body = Contact(first_name=fake.first_name(),
                       last_name=fake.last_name(),
                       email=fake.email(),
                       phone_number=fake.phone_number(),
                       birthday=fake.date_of_birth(),
                       id=1)
        contact = Contact(id=1,
                          first_name=fake.first_name(),
                          last_name=fake.last_name(),
                          email=fake.email(),
                          phone_number=fake.phone_number(),
                          birthday=fake.date_of_birth(),
                          )
        self.session.query().filter().first.return_value = contact
        self.session.commit.return_value = None
        result = update_contact(contact_id=1, contact=body, user=self.user, db=self.session)
        self.assertEqual(result.first_name, body.first_name)
        self.assertEqual(result.last_name, body.last_name)
        self.assertEqual(result.email, body.email)
        self.assertEqual(result.phone_number, body.phone_number)
        self.assertEqual(result.birthday, body.birthday)

    async def test_update_contact_not_found(self):
        body = ContactUpdate(first_name=fake.first_name(),
                             last_name=fake.last_name(),
                             email=fake.email(),
                             phone_number=fake.phone_number(),
                             birthday=fake.date_of_birth())
        self.session.query().filter().first.return_value = None
        self.session.commit.return_value = None
        result = update_contact(contact_id=1, contact=body, user=self.user, db=self.session)
        self.assertIsNone(result)


if __name__ == '__main__':
    unittest.main()
