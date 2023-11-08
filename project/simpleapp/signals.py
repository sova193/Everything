from django.conf import settings
from django.core.mail import EmailMultiAlternatives, send_mail
from django.db.models.signals import post_save, m2m_changed
from django.dispatch import receiver
from django.template.loader import render_to_string
from .models import Post, PostCategory, Feedback


def send_notifications(preview, pk, title, subscribers):
    html_content = render_to_string('post_created_email.html', {'text': preview, 'link': f'{settings.SITE_URL}/news/{pk}',})
    msg = EmailMultiAlternatives(subject=title, body='', from_email=settings.DEFAULT_FROM_EMAIL, to=subscribers,)

    msg.attach_alternative(html_content, 'text/html')
    msg.send()


@receiver(m2m_changed, sender=PostCategory)
def notify_about_news_post(sender, instance, **kwargs):
    categories = instance.category.all()
    subscribers: list[str] = []
    for category in categories:
        subscribers += category.subscribers.all()

    subscribers_emails = [s.email for s in subscribers]

    send_notifications(instance.preview(), instance.pk, instance.name, subscribers_emails)


@receiver(post_save, sender=Feedback)
def feedback_save(instance, **kwargs):
    post_user_email = instance.user.email
    send_mail(
        subject='Новый отзыв',
        message='На Ваше объявление оставлен отзыв',
        from_email='slavagnetov@yandex.ru',
        recipient_list=[post_user_email],
    )