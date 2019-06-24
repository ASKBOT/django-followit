"""
Test cases for the follower module
"""
from django.test import TestCase
from followit.compat import get_user_model
import followit

class FollowerTests(TestCase):
    def setUp(self):
        User = get_user_model()
        self.u1 = User.objects.create_user('user1', 'user1@example.com')
        self.u2 = User.objects.create_user('user2', 'user2@example.com')
        self.u3 = User.objects.create_user('user3', 'user3@example.com')
        followit.register(User)

    def test_multiple_follow(self):
        
        self.u1.follow_user(self.u2)
        self.u1.follow_user(self.u3)
        self.u2.follow_user(self.u1)

        self.assertEqual(
            set(self.u1.get_followers()),
            set([self.u2])
        )

        self.assertEqual(
            set(self.u2.get_followers()),
            set([self.u1])
        )

        self.assertEqual(
            set(self.u1.get_followed_users()),
            set([self.u2, self.u3])
        )

    def test_unfollow(self):
        self.u1.follow_user(self.u2)
        self.u1.unfollow_user(self.u2)
        self.assertEqual(self.u1.get_followed_users().count(), 0)

    def test_is_following(self):
        self.u2.follow_user(self.u1)
        self.assertTrue(self.u2.is_following(self.u1))
        self.assertFalse(self.u1.is_following(self.u2))
