from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import LoginView
from django.contrib import auth, messages
from django.db.models import Prefetch
from django.http import HttpResponseRedirect
from django.shortcuts import redirect, render
from django.urls import reverse, reverse_lazy

from carts.models import Cart
from orders.models import Order, OrderItem
from users.forms import ProfileForm, UserLoginForm, UserRegistrationForm


class UserLoginViews(LoginView):
    template_name = "login.html"
    form_class = UserLoginForm
    # success_url = reverse_lazy ("main:index")

    def get_success_url(self) -> str:
        redirect_page = self.request.POST.get("next", None)
        if redirect_page and redirect_page != reverse_lazy("user:login"):
            return redirect_page
        return reverse_lazy("main:index")

    def form_valid(self, form):
        session_key = self.request.session.session_key
        user = form.get_user()

        if user:
            auth.login(self.request, user)
            if session_key:
                forgot_carts = Cart.objects.filter(user=user)
                if forgot_carts.exists():  # если старая корзина не пуста
                    forgot_carts.delete()  # то удаляем ее
                Cart.objects.filter(session_key=session_key).update(user=user)
                messages.success(self.request, f"{user.username}, вы вошли в аккаунт")

                return HttpResponseRedirect(self.get_success_url())

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "Авторизация"
        return context


def registration(request):
    if request.method == "POST":
        form = UserRegistrationForm(data=request.POST)
        if form.is_valid():
            form.save()

            session_key = request.session.session_key

            user = form.instance
            auth.login(request, user)

            if session_key:
                Cart.objects.filter(session_key=session_key).update(user=user)

            messages.success(request, f"{user.username}, вы успешно зарегистрировались")
            return HttpResponseRedirect(reverse("main:index"))
    else:
        form = UserRegistrationForm()

    context = {
        "title": "Home - Регистрация",
        "form": form,
    }
    return render(request, "registration.html", context)


@login_required
def profile(request):
    if request.method == "POST":
        form = ProfileForm(
            data=request.POST, instance=request.user, files=request.FILES
        )
        if form.is_valid():
            form.save()
            messages.success(request, "Профайл успешно обновлен")
            return HttpResponseRedirect(reverse("user:profile"))
    else:
        form = ProfileForm(instance=request.user)

    orders = (
        Order.objects.filter(user=request.user)
        .prefetch_related(
            Prefetch(
                "orderitem_set",
                queryset=OrderItem.objects.select_related("product"),
            )
        )
        .order_by("-id")
    )

    context = {"title": "Home - Кабинет", "form": form, "orders": orders}
    return render(request, "profile.html", context)


def users_cart(request):
    return render(request, "users_cart.html")


@login_required
def logout(request):
    messages.success(request, f"{request.user.username}, вы вышли из аккаунта")
    auth.logout(request)
    return redirect(reverse("main:index"))


# def login(request):
#     if request.method == "POST":
#         form = UserLoginForm(data=request.POST)
#         if form.is_valid():
#             username = request.POST["username"]
#             password = request.POST["password"]
#             user = auth.authenticate(username=username, password=password)

#             session_key = request.session.session_key

#             if user:
#                 auth.login(request, user)
#                 messages.success(request, f"{username}, вы вошли в аккаунт")

#                 if session_key:
#                     Cart.objects.filter(session_key=session_key).update(user=user)

#                 redirect_page = request.POST.get("next", None)
#                 if redirect_page and redirect_page != reverse("user:login"):
#                     return HttpResponseRedirect(request.POST.get("next"))
#                 return HttpResponseRedirect(reverse("main:index"))
#     else:
#         form = UserLoginForm()

#     context = {
#         "title": "Home - Авторизация",
#         "form": form,
#     }
#     return render(request, "login.html", context)
