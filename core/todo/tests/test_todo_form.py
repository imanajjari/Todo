from django.test import SimpleTestCase, TestCase
from datetime import datetime

from ..forms import PostForm
from ..models import Category

class testForm(TestCase):

    def test_post_form_with_data(self):
        category_obj = Category.objects.create(name='test')
        form = PostForm(data={
            "title": "test",
            "content": "this a test",
            "status": True,
            "category": category_obj,
            "published_date": datetime.now() 
        })
        self.assertTrue(form.is_valid())