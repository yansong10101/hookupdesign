from django.shortcuts import render, redirect, get_object_or_404
from django.core.urlresolvers import reverse
from django.contrib.auth import *
from django.contrib.auth.forms import UserCreationForm


# Create your views here.
def index(request):
    return render(request, 'index.html')


def home(request):
    reverse('design:login', current_app=request.resolver_match.namespace)
    return render(request, 'home.html')


def signup(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            username = request.POST['username']
            password = request.POST['password1']
            user = authenticate(username=username, password=password)
            login(request, user)
            return redirect(reverse(index))     # need redirect to successful page, or to home page and show msg
        else:
            return render(request, 'signup.html', {'form': form})
    else:
        form = UserCreationForm()
        return render(request, 'signup.html', {'form': form})


def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect(reverse('design:index'))
        else:
            return render(request, 'login.html')
    else:
        return render(request, 'login.html')


def logout_view(request):
    logout(request)
    return redirect(reverse('design:index'))


# ==============================================
from django.contrib.auth.models import User, Group
from rest_framework import viewsets
from designweb.serializer import UserSerializer, GroupSerializer


class UserViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    queryset = User.objects.all()
    serializer_class = UserSerializer


class GroupViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows groups to be viewed or edited.
    """
    queryset = Group.objects.all()
    serializer_class = GroupSerializer