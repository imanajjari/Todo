from rest_framework.test import APIClient
from django.urls import reverse
import pytest
from datetime import datetime
from accounts.models import User, Profile


@pytest.fixture
def api_client():
    client = APIClient()
    return client


@pytest.fixture
def common_user():
    user = User.objects.create_user(
        email="test@test.com", password="a/@1234567"
    )
    return user


@pytest.mark.django_db
class TestPostApi:
    def test_get_post_response_200_status(self, api_client):
        url = reverse("todo:api-v1:post-list")
        response = api_client.get(url)
        assert response.status_code == 200

    def test_create_post_response_403_status(self, api_client):
        url = reverse("todo:api-v1:post-list")
        data = {
            "title": "test",
            "content": "description",
            "status": True,
            "published_date": datetime.now(),
        }
        response = api_client.post(url, data)
        assert response.status_code == 403

    def test_create_post_response_201_status(self, api_client, common_user):
        url = reverse("todo:api-v1:post-list")
        data = {
            "title": "test",
            "content": "description",
            "status": True,
            "published_date": datetime.now(),
        }
        user = common_user
        api_client.force_authenticate(user=user)
        response = api_client.post(url, data)
        assert response.status_code == 201

    def test_create_post_invalid_data_response_400_status(
        self, api_client, common_user
    ):
        url = reverse("todo:api-v1:post-list")
        data = {"name": common_user , "content": True}
        user = common_user

        api_client.force_authenticate(user=user)
        response = api_client.post(url, data)
        assert response.status_code == 400

@pytest.mark.django_db
class TestCategoryApi:
    def test_get_post_response_200_status(self, api_client):
        url = reverse("todo:api-v1:category-list")
        response = api_client.get(url)
        assert response.status_code == 200

    def test_create_post_response_201_status(self, api_client, common_user):
        url = reverse("todo:api-v1:category-list")
        data = {
            "name":"test"
        }
        user = common_user
        api_client.force_authenticate(user=user)
        response = api_client.post(url, data)
        assert response.status_code == 201
