from django.contrib.auth import logout, get_user_model
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse


User = get_user_model()


def login_required(function):
    def wrapper(request, *args, **kw):
        user = request.user
        if user.is_authenticated:
            return function(request, *args, **kw)

    return wrapper


def super_admin_required(function):
    def wrapper(request, *args, **kw):
        user = request.user
        if user.is_superuser:
            return function(request, *args, **kw)

    return wrapper


def pharmacy_required(function):
    def wrapper(request, *args, **kw):
        pass

    return wrapper


def admin_required(function):
    def wrapper(request, *args, **kw):
        pass

    return wrapper


def first_login(function):
    def wrapper(request, *args, **kwargs):
        user = request.user
        pass

    return wrapper
