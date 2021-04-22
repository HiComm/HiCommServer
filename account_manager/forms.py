from django.contrib.auth.forms import (
    AuthenticationForm,
    UserCreationForm
)
from django import forms
from .models import CustomUser
from django.contrib.auth import authenticate

class LoginForm(AuthenticationForm):
    """ログインフォーム"""
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields.pop("username")#使わないので

    email = forms.EmailField(widget=forms.EmailInput(
        attrs={
            'class':'input is-rounded is-medium',
            "placeholder" : "Email"
        }
    ))
    '''
    username = forms.CharField(widget=forms.TextInput(
        attrs={
        'class':'input is-rounded is-medium',
        'placeholder':'Username'
        }
    ))
    '''


    password = forms.CharField(widget=forms.PasswordInput(
        attrs={
        'class':'input is-rounded is-medium',
        'placeholder':'Password'
        }
    ))


    field_order = ['email', 'password']

    def clean(self, *args, **kwargs):
        email = self.cleaned_data.get("email")
        password = self.cleaned_data.get("password")
        if email and password:
            user = authenticate(email=email, password=password)
            if not user:
                raise forms.ValidationError("User does not exist.")
            if not user.is_active:
                raise forms.ValidationError("User is no longer active.")
        return super(LoginForm, self).clean(*args, **kwargs)


class UserCreateForm(UserCreationForm):
    """ユーザー登録用フォーム"""

    class Meta:
        model = CustomUser
        fields = ('username','email',)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs['class'] = 'input is-rounded'

    def clean_email(self):
        email = self.cleaned_data['email']
        CustomUser.objects.filter(email=email, is_active=False).delete()
        return email