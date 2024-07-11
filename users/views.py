from django.shortcuts import render


def login(request):
    context = {"title": "Home - Авторизация"}
    return render(request, "login.html", context)


def registration(request):
    context = {"title": "Home - Регистрация"}
    return render(request, "registration.html", context)


def profile(request):
    context = {"title": "Home - Кабинет"}
    return render(request, "profile.html", context)


def logout(
    request,
): ...
