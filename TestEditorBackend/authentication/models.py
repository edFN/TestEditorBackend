from django.contrib.auth.base_user import BaseUserManager
from django.contrib.auth.models import AbstractUser, PermissionsMixin
from django.db import models


class UserManager(BaseUserManager):

    def create_user(self,  email, password=None):
        """ Создает и возвращает пользователя с имэйлом, паролем и именем. """
        if email is None:
            raise TypeError('Users must have an email address.')

        user = self.model(email=self.normalize_email(email))
        user.set_password(password)
        user.save()

        return user

    def create_superuser(self, email, password):
        """ Создает и возввращет пользователя с привилегиями суперадмина. """

        if email is None:
            raise TypeError("Superuser must have a email")

        if password is None:
            raise TypeError('Superusers must have a password.')

        print("CREATED ADMIN")

        user = self.create_user(email, password)
        user.is_superuser = True
        user.is_staff = True
        user.save()

        return user


class User(AbstractUser, PermissionsMixin):
    username = models.CharField(
        "uSERNAME",
        max_length=150,
        null=True,blank=True
    )
    first_name = models.CharField("Имя", max_length=150, blank=True)
    last_name = models.CharField("Фамилия", max_length=150, blank=True)
    patronymic = models.CharField("Отчество", max_length=200, null=True,blank=True)

    email = models.EmailField("Email", blank=False, unique=True)

    birth_date = models.DateField("Дата рождения", max_length=200, null=True,blank=True)

    sex = models.CharField(verbose_name="Пол",choices=(("Мужской","Мужской"),("Женский","Женский")),max_length=100,
                           null=True,blank=False)
    avatar = models.ImageField(verbose_name="Аватар пользователя", null=True,blank=True)

    objects = UserManager()

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []


    def __str__(self):
        return f'{self.first_name} {self.last_name} {self.patronymic}'


