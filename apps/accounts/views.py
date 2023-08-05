from django.shortcuts import render, redirect
from django.contrib import messages
from django.views import View
from .forms import RegisterForm, LoginForm
from .models import User
from django.contrib.auth import authenticate, login, logout


class RegisterView(View):
    template_name = 'accounts/register.html'
    form_class = RegisterForm

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            messages.warning(request, 'برای ساخت حساب جدید ابتدا از حساب خود خارج شوید', 'warning')
            return redirect('dashboard:dashboard')
        return super().dispatch(request, request, *args, **kwargs)

    def get(self, request, *args, **kwargs):
        return render(request, self.template_name, {'form': self.form_class})

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        # if user data were correct
        if form.is_valid():
            cleaned_data = form.cleaned_data
            # create user instance
            User.objects.create_user(
                first_name=cleaned_data['first_name'],
                last_name=cleaned_data['last_name'],
                phone_number=cleaned_data['phone_number'],
                password=cleaned_data['password']
            )
            messages.success(request, 'حساب شما با موفقیت ساخته شد', 'success')
            # return redirect('accounts:login')
        messages.error(request, 'مشکلی در ساخت حساب شما به وجود آمد، لطفا دوباره تلاش کنید', 'danger')
        return render(request, self.template_name, {'form': form})


class LoginView(View):
    template_name = 'accounts/login.html'
    form_class = LoginForm

    def setup(self, request, *args, **kwargs):
        self.next = request.GET.get('next')
        return super().setup(request, *args, **kwargs)

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            messages.warning(request, 'قبلا وارد حساب خود شده اید', 'warning')
            return redirect('dashboard:dashboard')
        return super().dispatch(request, request, *args, **kwargs)

    def get(self, request, *args, **kwargs):
        return render(request, self.template_name, {'form': self.form_class})

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        if form.is_valid():
            cleaned_data = form.cleaned_data
            user = authenticate(phone_number=cleaned_data['phone_number'],password=cleaned_data['password'])
            if user:
                login(request, user)
                messages.success(request, 'با موفقیت وارد حسابتان شدید', 'success')
                if self.next:
                    return redirect(self.next)
                return redirect('dashboard:dashboard')
            messages.error(request, 'اطلاعات کاربری صحیح نیست', 'danger')
            return render(request, self.template_name, {'form': form})
        messages.error(request, 'اطلاعات ورود را به درستی وارد کنید', 'danger')
        return render(request, self.template_name, {'form': form})


class LogoutView(View):
    def get(self, request):
        logout(request)
        messages.info(request, 'از حساب خود خارج شدید', 'info')
        return redirect('accounts:login')