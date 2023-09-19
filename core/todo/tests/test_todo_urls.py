from django.test import TestCase, SimpleTestCase
from django.urls import resolve, reverse
from ..views import IndexView, ItemDetailView, PostCreateView, PostEditView, PostDeleteView

# Create your tests here.

class TestUrl(TestCase):

    def test_todo_index_url_resolve(self):
        url = reverse("todo:index")
        self.assertEquals(resolve(url).func.view_class,IndexView)

    def test_todo_detail_url_resolve(self):
        url = reverse("todo:item-detail", kwargs={'pk':5})
        self.assertEquals(resolve(url).func.view_class,ItemDetailView)

    def test_todo_create_url_resolve(self):
        url = reverse("todo:item-create")
        self.assertEquals(resolve(url).func.view_class,PostCreateView)

    def test_todo_edit_url_resolve(self):
        url = reverse("todo:item-edit", kwargs={'pk':5})
        self.assertEquals(resolve(url).func.view_class,PostEditView)

    def test_todo_delete_url_resolve(self):
        url = reverse("todo:item-delete", kwargs={'pk':5})
        self.assertEquals(resolve(url).func.view_class,PostDeleteView)
