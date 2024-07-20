import pytest
from django.urls import reverse
from django.contrib.auth.models import User
from rest_framework.test import APIClient
from todo.models import Todo
from django.utils import timezone


@pytest.fixture
def api_client():
    return APIClient()


@pytest.fixture
def create_user(db):
    def make_user(**kwargs):
        user = User.objects.create_user(**kwargs)
        return user

    return make_user


@pytest.fixture
def authenticate(api_client, create_user):
    def make_authenticated(user=None):
        if not user:
            user = create_user(username='testuser', password='testpassword')
        api_client.login(username=user.username, password='testpassword')
        return user

    return make_authenticated


@pytest.mark.django_db
def test_home_view(api_client):
    response = api_client.get(reverse('home'))
    assert response.status_code == 200


@pytest.mark.django_db
def test_signup_user(api_client):
    response = api_client.post(reverse('signupuser'), {
        'username': 'newuser',
        'password1': 'newpassword',
        'password2': 'newpassword'
    })
    assert response.status_code == 302


@pytest.mark.django_db
def test_login_user(api_client, create_user):
    user = create_user(username='testuser', password='testpassword')
    response = api_client.post(reverse('loginuser'), {
        'username': 'testuser',
        'password': 'testpassword'
    })
    assert response.status_code == 302


@pytest.mark.django_db
def test_logout_user(api_client, authenticate):
    user = authenticate()
    response = api_client.post(reverse('logoutuser'))
    assert response.status_code == 302


@pytest.mark.django_db
def test_create_todo_get(api_client, authenticate):
    user = authenticate()
    response = api_client.get(reverse('createtodo'))
    assert response.status_code == 200


@pytest.mark.django_db
def test_create_todo_post(api_client, authenticate):
    user = authenticate()
    response = api_client.post(reverse('createtodo'), {'title': 'Test Todo', 'memo': 'Test Memo'})
    assert response.status_code == 302
    assert Todo.objects.count() == 1


@pytest.mark.django_db
def test_current_todos(api_client, authenticate):
    user = authenticate()
    Todo.objects.create(title='Test Todo', user=user)
    response = api_client.get(reverse('currenttodos'))
    assert response.status_code == 200
    assert 'Test Todo' in response.content.decode()


@pytest.mark.django_db
def test_completed_todos(api_client, authenticate):
    user = authenticate()
    todo = Todo.objects.create(title='Test Todo', user=user, date_completed=timezone.now())
    response = api_client.get(reverse('completedtodos'))
    assert response.status_code == 200
    assert 'Test Todo' in response.content.decode()


@pytest.mark.django_db
def test_view_todo_get(api_client, authenticate):
    user = authenticate()
    todo = Todo.objects.create(title='Test Todo', user=user)
    response = api_client.get(reverse('viewtodo', args=[todo.pk]))
    assert response.status_code == 200


@pytest.mark.django_db
def test_view_todo_post(api_client, authenticate):
    user = authenticate()
    todo = Todo.objects.create(title='Test Todo', user=user)
    response = api_client.post(reverse('viewtodo', args=[todo.pk]), {'title': 'Updated Title'})
    assert response.status_code == 302
    todo.refresh_from_db()
    assert todo.title == 'Updated Title'


@pytest.mark.django_db
def test_complete_todo(api_client, authenticate):
    user = authenticate()
    todo = Todo.objects.create(title='Test Todo', user=user)
    response = api_client.post(reverse('completetodo', args=[todo.pk]))
    assert response.status_code == 302
    todo.refresh_from_db()
    assert todo.date_completed is not None


@pytest.mark.django_db
def test_delete_todo(api_client, authenticate):
    user = authenticate()
    todo = Todo.objects.create(title='Test Todo', user=user)
    response = api_client.post(reverse('deletetodo', args=[todo.pk]))
    assert response.status_code == 302
    assert not Todo.objects.filter(pk=todo.pk).exists()
