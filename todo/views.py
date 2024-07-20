from rest_framework import viewsets, mixins
from rest_framework.decorators import action
from rest_framework.permissions import AllowAny, IsAuthenticated
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.db import IntegrityError
from django.utils import timezone
from django.contrib.auth.models import User
from .models import Todo
from api.serializers import TodoSerializer
from .forms import TodoForm


class TodoViewSet(
    mixins.ListModelMixin,
    mixins.CreateModelMixin,
    mixins.RetrieveModelMixin,
    mixins.UpdateModelMixin,
    mixins.DestroyModelMixin,
    viewsets.GenericViewSet
):
    serializer_class = TodoSerializer
    queryset = Todo.objects.all()

    def get_permissions(self):
        if self.action in ['home', 'signup_user', 'login_user']:
            permission_classes = [AllowAny]
        else:
            permission_classes = [IsAuthenticated]
        return [permission() for permission in permission_classes]

    @action(detail=False, permission_classes=[AllowAny])
    def home(self, request):
        return render(request, 'todo/home.html')

    @action(detail=False, methods=['get', 'post'],
            permission_classes=[AllowAny])
    def signup_user(self, request):
        if request.method == 'GET':
            return render(request, 'todo/signupuser.html',
                          {'form': UserCreationForm()})
        else:
            if request.POST['password1'] == request.POST['password2']:
                try:
                    user = User.objects.create_user(request.POST['username'],
                                                    password=request.POST['password1'])
                    user.save()
                    login(request, user)
                    return redirect('currenttodos')
                except IntegrityError:
                    return render(request, 'todo/signupuser.html',
                                  {'form': UserCreationForm(),
                                   'error': 'That username has already been taken.'
                                            'Please choose a new username'})
            else:
                return render(request, 'todo/signupuser.html',
                              {'form': UserCreationForm(),
                               'error': 'Passwords did not match'})

    @action(detail=False, methods=['get', 'post'], permission_classes=[AllowAny])
    def login_user(self, request):
        if request.method == 'GET':
            return render(request,
                          'todo/loginuser.html',
                          {'form': AuthenticationForm()})
        else:
            user = authenticate(request,
                                username=request.POST['username'],
                                password=request.POST['password'])
            if user is None:
                return render(request, 'todo/loginuser.html',
                              {'form': AuthenticationForm(),
                               'error': 'Username and password did not match'})
            else:
                login(request, user)
                return redirect('currenttodos')

    @action(detail=False, methods=['post'], permission_classes=[IsAuthenticated])
    def logout_user(self, request):
        if request.method == 'POST':
            logout(request)
            return redirect('home')

    @action(detail=False, methods=['get', 'post'])
    def create_todo(self, request):
        if request.method == 'GET':
            return render(request,
                          'todo/createtodo.html',
                          {'form': TodoForm()})
        else:
            try:
                form = TodoForm(request.POST)
                new_todo = form.save(commit=False)
                new_todo.user = request.user
                new_todo.save()
                return redirect('currenttodos')
            except ValueError:
                return render(request, 'todo/createtodo.html',
                              {'form': TodoForm(),
                               'error': 'Bad data passed in. Try again.'})

    @action(detail=False)
    def current_todos(self, request):
        todos = Todo.objects.filter(user=request.user, date_completed__isnull=True)
        return render(request, 'todo/currenttodos.html',
                      {'todos': todos})

    @action(detail=False)
    def completed_todos(self, request):
        todos = Todo.objects.filter(user=request.user,
                                    date_completed__isnull=False).order_by('-date_completed')
        return render(request, 'todo/completedtodos.html',
                      {'todos': todos})

    @action(detail=True, methods=['get', 'post'])
    def view_todo(self, request, pk=None):
        todo = get_object_or_404(Todo, pk=pk, user=request.user)
        if request.method == 'GET':
            form = TodoForm(instance=todo)
            return render(request, 'todo/viewtodo.html',
                          {'todo': todo, 'form': form})
        else:
            try:
                form = TodoForm(request.POST, instance=todo)
                form.save()
                return redirect('currenttodos')
            except ValueError:
                return render(request, 'todo/viewtodo.html',
                              {'todo': todo, 'form': form, 'error': 'Bad info'})

    @action(detail=True, methods=['post'])
    def complete_todo(self, request, pk=None):
        todo = get_object_or_404(Todo, pk=pk, user=request.user)
        if request.method == 'POST':
            todo.date_completed = timezone.now()
            todo.save()
            return redirect('currenttodos')

    @action(detail=True, methods=['post'])
    def delete_todo(self, request, pk=None):
        todo = get_object_or_404(Todo, pk=pk, user=request.user)
        if request.method == 'POST':
            todo.delete()
            return redirect('currenttodos')
