"""todowoo URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.contrib import admin
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from todo.views import TodoViewSet
from django.conf import settings
from django.conf.urls.static import static

router = DefaultRouter()
router.register(r'todos', TodoViewSet, basename='todos')

urlpatterns = [
    path('admin/', admin.site.urls),

    # Custom view actions
    path('', TodoViewSet.as_view({'get': 'home'}), name='home'),
    path('signup/', TodoViewSet.as_view({'get': 'signup_user', 'post': 'signup_user'}), name='signupuser'),
    path('login/', TodoViewSet.as_view({'get': 'login_user', 'post': 'login_user'}), name='loginuser'),
    path('logout/', TodoViewSet.as_view({'post': 'logout_user'}), name='logoutuser'),

    # Todo view actions
    path('create/', TodoViewSet.as_view({'get': 'create_todo', 'post': 'create_todo'}), name='createtodo'),
    path('current/', TodoViewSet.as_view({'get': 'current_todos'}), name='currenttodos'),
    path('completed/', TodoViewSet.as_view({'get': 'completed_todos'}), name='completedtodos'),
    path('todo/<int:pk>/', TodoViewSet.as_view({'get': 'view_todo', 'post': 'view_todo'}), name='viewtodo'),
    path('todo/<int:pk>/complete/', TodoViewSet.as_view({'post': 'complete_todo'}), name='completetodo'),
    path('todo/<int:pk>/delete/', TodoViewSet.as_view({'post': 'delete_todo'}), name='deletetodo'),

    # API routes
    path('todo/api/', include(router.urls)),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

