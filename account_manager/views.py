from django.shortcuts import render, redirect

# Create your views here.

from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import (
    LoginView, LogoutView,
)
from django.views import generic
from .forms import LoginForm, UserCreateForm
from django.contrib.sites.shortcuts import get_current_site
from django.core.signing import BadSignature, SignatureExpired, loads, dumps
from django.http import Http404, HttpResponseBadRequest
from django.shortcuts import redirect
from django.template.loader import render_to_string
from django.conf import settings

from .models import CustomUser
from .auth_backend import EmailAuthBackend as ea
from django.contrib.auth import login, authenticate

#landing page
def Top(request):
    return redirect("../../hicomm/")#マジックナンバーみ

'''
class Top(generic.TemplateView):
    redirect("q_and_a/index.html")
    #template_name = 'top.html'
'''

class Login(LoginView):
    """ログインページ"""
    form_class = LoginForm
    template_name = 'login.html'
    
    def post(self, request, *args, **kwargs):
        form = self.form_class(data=request.POST, files=request.FILES)
        if form.is_valid():
            email = request.POST['email']
            password = request.POST['password']
            username = CustomUser.objects.get(email=email.lower()).username
            print(username)
            user = authenticate(email=email, password=password)
            print(user)
            login(request, user)
            return redirect("q_and_a:index")
        
        return render(request, "./login.html", {"form" : form,})
    
class Logout(LogoutView):
    """ログアウトページ"""
    template_name = 'top.html'


#新規登録
class UserCreate(generic.CreateView):
    """ユーザー仮登録"""
    template_name = 'register.html'
    form_class = UserCreateForm

    def form_valid(self, form):
        """仮登録と本登録用メールの発行."""
        # 仮登録：is_valid = False
        user = form.save(commit=False)
        user.is_active = False
        user.save()

        # アクティベーションURLの送付
        current_site = get_current_site(self.request)
        domain = current_site.domain
        context = {
            'protocol': self.request.scheme,
            'domain': domain,
            'token': dumps(user.pk),
            'user': user,
        }

        subject = render_to_string('mail/register/subject.txt', context)
        message = render_to_string('mail/register/body.txt', context)
        user.sendmail(subject, message)

        return redirect('account_manager:registerInProcess')


class UserCreateInProcess(generic.TemplateView):
    """ユーザー仮登録したよ"""
    template_name = 'registerInProcess.html'
    
class UserCreateComplete(generic.TemplateView):
    """メール内URLアクセス後のユーザー本登録"""
    template_name = 'registerDone.html'
    timeout_seconds = getattr(settings, 'ACTIVATION_TIMEOUT_SECONDS', 60*60*24)  # デフォルトでは1日以内

    def get(self, request, **kwargs):
        """tokenが正しければ本登録."""
        token = kwargs.get('token')
        try:
            user_pk = loads(token, max_age=self.timeout_seconds)

        # 期限切れ
        except SignatureExpired:
            return HttpResponseBadRequest()

        # tokenが間違っている
        except BadSignature:
            return HttpResponseBadRequest()

        # tokenは問題なし
        else:
            try:
                user = CustomUser.objects.get(pk=user_pk)
            except CustomUser.DoesNotExist:
                return HttpResponseBadRequest()
            else:
                if not user.is_active:
                    # 問題なければ本登録とする
                    user.is_active = True
                    user.save()
                    return super().get(request, **kwargs)
            
                else:
                    return redirect('q_and_a:index')

        return HttpResponseBadRequest()