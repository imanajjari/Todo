from django.test import TestCase
from datetime import datetime
from django.contrib.auth import get_user_model
from accounts.models import User, Profile
from .. models import Post, Category

class TestModel(TestCase):

    def setUp(self):
        self.user = User.objects.create_user(
            email="test1@gmail.com",
            password="Iph@ne1394"
        )
        self.profile = Profile.objects.create(
            user=self.user,
            first_name= "test_first_name",
            last_name= "test_last_name",
            description= "test_description"
        )

    def test_create_post_with_valid_data(self):
        
        post = Post.objects.create(
            author = self.profile,
            title = "test",
            content = "this a test",
            status = True,
            category = None,
            published_date = datetime.now() 
        )
        self.assertTrue(Post.objects.filter(id=post.id).exists())
        self.assertEquals(post.title, "test")
