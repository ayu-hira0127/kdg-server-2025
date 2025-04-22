from django.shortcuts import render

# Create your views here.
from django.views import View



from django.shortcuts import render, redirect
from django.views import View
from django.contrib.auth import login, logout
from django.contrib.auth.forms import AuthenticationForm
from .forms import SignUpForm

class SignupView(View):
    def get(self, request):
        form = SignUpForm()
        return render(request, 'signup.html', {'form': form})

    def post(self, request):
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('search_app:search_view')
        return render(request, 'signup.html', {'form': form})

class CustomLoginView(View):
    def get(self, request):
        form = AuthenticationForm()
        return render(request, 'login.html', {'form': form})

    def post(self, request):
        form = AuthenticationForm(request, request.POST)
        if form.is_valid():
            login(request, form.get_user())
            return redirect('search_app:search_view')
        return render(request, 'login.html', {'form': form})

class CustomLogoutView(View):
    def get(self, request):
        logout(request)
        return redirect('search_app:search_view')
    
class MyPageView(View):
    def get(self, request):
        # ユーザー情報をコンテキストに渡す
        context = {'user': request.user}
        return render(request, 'mypage.html', context)

mypage = MyPageView.as_view()

signup = SignupView.as_view()
user_login = CustomLoginView.as_view()
user_logout = CustomLogoutView.as_view()
user_mypage = MyPageView.as_view()
