from django.urls import path, include
from rest_framework.routers import DefaultRouter
from todo.views import TodoViewSet

router = DefaultRouter()
router.register(r'todos', TodoViewSet, basename='todos')

urlpatterns = [
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    ]
