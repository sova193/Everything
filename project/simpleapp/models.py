from allauth.account.forms import SignupForm
from django.db import models
from django.core.validators import MinValueValidator
from django.urls import reverse
from django.contrib.auth.models import User, Group
from django import forms
from django.contrib.auth.forms import UserCreationForm
from datetime import datetime


class Author(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.user}'


class Category(models.Model):
    name = models.CharField(max_length=100, unique=True)
    subscribers = models.ManyToManyField(User, related_name='subscriptions')

    def __str__(self):
            return self.name.title()


class Post(models.Model):
    tanks = 'TNK'
    hils = 'HIL'
    dd = 'DD'
    merchants = 'MCH'
    guild_masters = 'GMA'
    quest_givers = 'QMA'
    blacksmiths = 'BLM'
    tanners = 'TAN'
    potion_makers = 'PMK'
    spell_masters = 'SMA'

    CATEGORY_CHOICES = (
        (tanks, 'Танки'),
        (hils, 'Хилы'),
        (dd, 'ДД'),
        (merchants, 'Торговцы'),
        (guild_masters, 'Гилдмастеры'),
        (quest_givers, 'Квестгиверы'),
        (blacksmiths, 'Кузнецы'),
        (tanners, 'Кожевники'),
        (potion_makers, 'Зельевары'),
        (spell_masters, 'Мастера заклинаний'),
    )
    type_post = models.CharField(max_length=20, choices=CATEGORY_CHOICES)
    pub_date = models.DateTimeField(auto_now_add=True)
    author = models.ForeignKey(Author, on_delete=models.CASCADE)
    name = models.CharField(
        max_length=50,
        unique=True,
    )
    description = models.TextField()

    category = models.ManyToManyField(
        Category,
        through='PostCategory',
        related_name='PostCategory',
    )
    rating = models.FloatField(
        validators=[MinValueValidator(0.0)], default=0.0
    )
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    def preview(self):
        preview = f'{self.description[:124]}...'
        return preview

    def __str__(self):
        return f'{self.name.title()}: {self.description[:20]}'

    def get_absolute_url(self):
        return reverse('post_detail', args=[str(self.id)])


class PostCategory(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)


class BaseRegisterForm(UserCreationForm):
    email = forms.EmailField(label = "Email")
    first_name = forms.CharField(label = "Имя")
    last_name = forms.CharField(label = "Фамилия")

    class Meta:
        model = User
        fields = ("username",
                  "first_name",
                  "last_name",
                  "email",
                  "password1",
                  "password2", )


class BasicSignupForm(SignupForm):
    def save(self, request):
        user = super(BasicSignupForm, self).save(request)
        basic_group = Group.objects.get(name='common')
        basic_group.user_set.add(user)
        return user


class Feedback(models.Model):
    body_feedback = models.TextField()
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    post = models.ForeignKey(Post, on_delete=models.CASCADE, null=True)