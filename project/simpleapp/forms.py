from django import forms
from django.core.exceptions import ValidationError
from .models import Post, Feedback


class PostForm(forms.ModelForm):
    description = forms.CharField(min_length=20)

    class Meta:
        model = Post
        fields = ['name', 'description', 'category', 'author', 'type_post']

    def clean(self):
        cleaned_data = super().clean()
        description = cleaned_data.get("description")
        name = cleaned_data.get("name")

        if name == description:
            raise ValidationError(
                "Описание не должно быть идентично названию."
            )

        return cleaned_data


class ArticleForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['name', 'description', 'category', 'author', 'type_post']

    def clean(self):
        cleaned_data = super().clean()
        description = cleaned_data.get("description")
        name = cleaned_data.get("name")

        if name == description:
            raise ValidationError(
                "Описание не должно быть идентично названию."
            )

        return cleaned_data


class FeedbackForm(forms.ModelForm):
    class Meta:
        model = Feedback
        fields = [
            'post',
            'body_feedback',
            'user'
        ]
