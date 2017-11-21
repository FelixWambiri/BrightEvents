import unittest

from app.models.user import User
from app.models.user_acounts import UserAccounts


class TestUserAccounts(unittest.TestCase):
    """
        This class will test:
            If the methods are working User class are working correctly
            If not, whether that is captured
        """

    def setUp(self):
        """
        Instantiating reusable variables
        """
        self.user_accounts = UserAccounts()
        self.user1 = User("Johny", "johny@bravo.com", "johnybravobravo")
        self.user2 = User("Fellow1", "fellow1@andela.com", "bootcampertofellow")
        self.user3 = User("Ricky", "ricky@morty.com", "rickandmorty")

    # Test if user accounts has been created successfully
    def test_successful_creation_of_user_accounts(self):
        self.assertEqual(isinstance(self.user_accounts, UserAccounts), True)

    # Test that on initialisation the user accounts has no user
    def test_that_on_initialization_user_accounts_is_empty(self):
        self.assertEqual(0, len(self.user_accounts.users))

    # Test that user can register successfully
    def test_successful_registration_of_user(self):
        self.user_accounts.create_user(self.user1)
        self.assertEqual(1, len(self.user_accounts.users))

    # Test multiple user registration
    def test_that_multiple_users_can_register(self):
        # First User
        self.user_accounts.create_user(self.user1)
        self.assertEqual(1, len(self.user_accounts.users))

        # Second User
        self.user_accounts.create_user(self.user2)
        self.assertEqual(2, len(self.user_accounts.users))

        # Third User
        self.user_accounts.create_user(self.user3)
        self.assertEqual(3, len(self.user_accounts.users))

    # Test exception is raised on registration of two users with same username/id
    def test_exception_raised_on_registration_of_two_users_using_the_same_id(self):
        self.user4 = User("Johny", "johny@bravo.com", "johnybravobravo")
        self.user_accounts.create_user(self.user1)
        self.assertRaises(KeyError, self.user_accounts.create_user, self.user4)

    # Test that users can be deleted
    def test_user_can_be_derigestered(self):
        self.user_accounts.create_user(self.user1)
        self.user_accounts.create_user(self.user2)
        self.user_accounts.create_user(self.user3)
        self.assertEqual(3, len(self.user_accounts.users))

        # deregister user1
        self.user_accounts.delete_user("Johny")
        self.assertEqual(2, len(self.user_accounts.users))

        # Derigester user2 and user3
        self.user_accounts.delete_user("Fellow1")
        self.user_accounts.delete_user("Ricky")
        self.assertEqual(0, len(self.user_accounts.users))

    # Test that an attempt to deregister a user not in existence raises an exception
    def test_deregistration_of_a_non_existent_user_raises_exception(self):
        self.user4 = User("Johny", "johny@bravo.com", "johnybravobravo")
        self.assertRaises(KeyError, self.user_accounts.delete_user, "Johny")

    # Test that the method get_specific_user returns that specified user
    def test_that_get_specific_user_returns_correct_output(self):
        self.user_accounts.create_user(self.user1)
        self.assertIs(self.user1, self.user_accounts.get_specific_user("Johny"))


if __name__ == '__main__':
    unittest.main()