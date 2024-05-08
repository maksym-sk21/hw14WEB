import unittest
from unittest.mock import MagicMock

from rest_api.src.database.models import User
from rest_api.src.schemas import UserModel
from rest_api.src.repository.users import (get_user_by_email, create_user, update_token, confirmed_email)


class TestUserFunctions(unittest.TestCase):
    def setUp(self):
        self.session = MagicMock()

    async def test_get_user_by_email(self):
        email = "test@example.com"
        user = User(id=1, email=email)
        self.session.query().filter().first.return_value = user

        result = await get_user_by_email(email, self.session)

        self.assertEqual(result, user)

    async def test_create_user(self):
        body = UserModel(email="test@example.com")
        self.session.commit.return_value = None

        result = await create_user(body, self.session)

        self.assertIsInstance(result, User)
        self.assertEqual(result.email, body.email)
        self.assertIsNotNone(result.avatar)

    async def test_update_token(self):
        user = User(id=1, email="test@example.com")
        token = "some_token"

        await update_token(user, token, self.session)

        self.assertEqual(user.refresh_token, token)
        self.session.commit.assert_called_once()

    async def test_confirmed_email(self):
        email = "test@example.com"
        user = User(id=1, email=email, confirmed=False)
        self.session.query().filter().first.return_value = user
        self.session.commit.return_value = None

        await confirmed_email(email, self.session)

        self.assertTrue(user.confirmed)
        self.session.commit.assert_called_once()


if __name__ == "__main__":
    unittest.main()
