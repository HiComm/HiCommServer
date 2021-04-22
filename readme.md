# HiComm on django

pythonでバックエンド(とフロント)を書けるライブラリ「django」でHiCommのサーバーサイドを楽に構築する試みです。

htmlが動的に生成できたり便利（なはず）


# 構築のインストラクション
## requirements
python3系が入っている前提
```shell
$pip3 install django
$pip3 install python3-django

#↓↓MySQLのpythonバインディングパッケージ↓↓

$sudo apt install libmysqlclient-dev
$pip3 insatll mysqlclient

```
## mysqlにdjango用ユーザー作成＋各種設定
```SQL
#ユーザー作成＋権限設定
create user "[user name]"@"%" identified by "[password]"
grant CREATE, ALTER, INDEX, SELECT, UPDATE, INSERT, DELETE, REFERENCES on *.* to django_usr;

#アプリの接続先データベース作成
create database "[database name]" character set utf8mb4
```
* 作成ユーザーは@"%"（ワイルドカード）にしておき、リモートからアクセスできるようにする。接続元が決まっていたらそこのIPでもOK
* データベースの文字コードは絵文字とか入れられるようにutf-8 mb4にしているけど、utf-8でないとダメかもしれない

mysqlサーバーの/etc/mysql/mysql.conf.d/mysql.cnfを編集
```sh
#bind-address = 127.0.0.1 #ローカルのループバックのみ
bind-address = 0.0.0.0 #どこからでもアクセス可能
```
mysqlを再起動
```sh
$sudo systemctl restart mysql.service
```

## プロジェクトのディレクトリの初期化
```sh
$cd tekitou_dir #適当なところ
$django-admin startproject [projectname] .
```

## データベースの情報を変更
設定ファイル（.[projectname]/settings.py）を編集
```python
DATABASES = {（ひとりでBASE_DIR, 'db.sqlite3'),
    }
}
```
を以下のように編集[^1]
```python
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': '[database name]',
        'USER': '[user name]',
        'PASSWORD':'[password]'
        'HOST': '172.19.115.160',
        'PORT': '3306',
    }
}
```
[^1]: パスワードは平文で保存すると危ない（githubとかに上げるとき）けれど、今回はローカルなのでヨシ

### ついでに日本語環境にする
```python
# Internationalization
# https://docs.djangoproject.com/en/2.2/topics/i18n/

#LANGUAGE_CODE = 'en-us'
LANGUAGE_CODE = 'ja-JP'

#TIME_ZONE = 'UTC'
TIME_ZONE = 'Asia/Tokyo'
```

## ユーザーアカウントの仕様を作る

### 認証用のアプリを初期化する
```sh
$python3 manage.py startapp account_manager
$cd account_manager
```
### 認証のデータベース定義をアプリディレクトリ内のmodels.pyで設定

AbstractBaseUserを継承するので、ほぼAbstractUserのコードに似た感じで書く。じゃあAbstractUserでよかったじゃんと思うけれどなんとなく

```python
#models.py
from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.contrib.auth.validators import UnicodeUsernameValidator
from django.utils import timezone
from django.utils.translation import gettext_lazy as _
from django.core.mail import send_mail
from django.contrib.auth.base_user import BaseUserManager
# Create your models here.

class UserManager(BaseUserManager):
    use_in_migrations = True
        
    def _create_user(self, company_id, email, password, **extra_fields):
        """
        Create and save a user with the given company_id, and password.
        """
        if not company_id:
            raise ValueError('The given username must be set')
        email = self.normalize_email(email)
        user = self.model(company_id=company_id, email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, company_id, email=None, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('is_superuser', False)
        return self._create_user(company_id, email, password, **extra_fields)

    def create_superuser(self, company_id, email=None, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self._create_user(company_id, email, password, **extra_fields)

class CustomUser(AbstractBaseUser, PermissionsMixin):
    username = models.CharField(
        _("username"),
        max_length = 128,
        unique = True,
    )

    first_name = models.CharField(_("first name"), max_length=64, blank=True)
    last_name = models.CharField(_("last name"), max_length=64, blank=True)
    company_id = models.IntegerField(null=True)
    email = models.EmailField(_("email address"), blank=True)
    is_staff = models.BooleanField(
        _("staff status"),
        default=False,
    )

    is_active = models.BooleanField(
        _("active status"),
        default=True,
    )
    data_joined = models.DateField(_("date joined"), default=timezone.now)




    objects = UserManager()
    
    EMAIL_FIELD = 'email'
    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['company_id']

    def sendmail(self, subject, message, from_email=None, **kwargs):
        """Send an email to this user."""
        send_mail(subject, message, from_email, [self.email], **kwargs)
```

admin.pyで設定？項目を書く
このへんdjangoの仕様がよくわかっていない

```python
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser

# Register your models here.


class CustomUserAdmin(UserAdmin):
    model = CustomUser
    fieldsets = ((None, {"fields" : ("company_id",)}),)
    list_display = ["username", "email", "company_id"]
admin.site.register(CustomUser, CustomUserAdmin)
```
次にプロジェクトルートディレクトリのsettings.pyでアプリの情報を加える

```python
#settings.py
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    "account_manager",
]
#中略

#custom user
AUTH_USER_MODEL = "account_manager.CustomUser"
```
アプリのmake migrateをする
```sh
$python3 manage.py makemigrations account_manager
```

migrateする
```sh
$python3 manage.py migrate
```

管理画面用のスーパーユーザーを作成する
```sh
$python3 manage.py createsuperuser
```

# アプリ部分
## アプリ構成

|機能|名称|
|---|---|
|ユーザー認証|account_manager|
|Q&A投稿・編集・削除|q_and_a|
|ナレッジ投稿・編集・削除|knowledge|

## ユーザー認証
UserをCustomUserクラスに置き換える。（前節migration前に行った）

## Q&A関連
あ