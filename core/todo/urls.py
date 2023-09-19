from django.urls import path, include
from . import views
app_name = 'todo'

urlpatterns = [
    path('items/',views.IndexView.as_view(), name="index"),
    path('items/api/',views.IndexApiView.as_view(), name="index-api"),
    path('items/<int:pk>',views.ItemDetailView.as_view(), name="item-detail"),
    path('items/create',views.PostCreateView.as_view(), name="item-create"),
    path('items/<int:pk>/edit/',views.PostEditView.as_view(), name="item-edit"),
    path('items/<int:pk>/delete/',views.PostDeleteView.as_view(), name="item-delete"),
    path("items/create/", views.TaskCreate.as_view(), name="create_task"),
    path("items/complete/<int:pk>/", views.TaskComplete.as_view(), name="complete_task"),
    path("items/start/<int:pk>/", views.TaskStart.as_view(), name="start_task"),
    path('api/v1/', include('todo.api.v1.urls') ),

]
