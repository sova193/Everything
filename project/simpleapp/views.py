# Импортируем класс, который говорит нам о том,
# что в этом представлении мы будем выводить список объектов из БД
from apscheduler.schedulers.blocking import BlockingScheduler
from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.contrib.auth.models import User, Group
from django.core.mail import EmailMultiAlternatives
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import redirect, get_object_or_404, render
from django.template.loader import render_to_string
from django.views import View
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView, TemplateView
from django_apscheduler.jobstores import DjangoJobStore
from .mixins import LoginRequiredViewMixin
from .models import Post, BaseRegisterForm, Category, Feedback
from datetime import datetime
from .filters import PostFilter
from .forms import PostForm, ArticleForm, FeedbackForm
from django.urls import reverse_lazy


class PostList(ListView):
    model = Post
    ordering = '-pub_date'
    template_name = 'posts.html'
    context_object_name = 'posts'
    paginate_by = 10

    def get_queryset(self):
        queryset = super().get_queryset()
        self.filterset = PostFilter(self.request.GET, queryset)
        return self.filterset.qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['time_now'] = datetime.utcnow()
        context['next_sale'] = None
        context['filterset'] = self.filterset
        return context


class PostDetail(DetailView):
    model = Post
    template_name = 'post.html'
    context_object_name = 'post'


class PostCreate(PermissionRequiredMixin, CreateView):
    # Указываем нашу разработанную форму
    form_class = PostForm
    # модель товаров
    model = Post
    # и новый шаблон, в котором используется форма.
    template_name = 'post_edit.html'
    permission_required = ('simpleapp.add_post',)


class PostUpdate(PermissionRequiredMixin, LoginRequiredViewMixin, UpdateView):
    form_class = PostForm
    model = Post
    template_name = 'post_edit.html'
    success_url = '/news/'
    permission_required = ('simpleapp.change_post',)


class PostDelete(DeleteView):
    model = Post
    template_name = 'post_delete.html'
    success_url = reverse_lazy('post_list')


class SearchList(ListView):
    model = Post
    ordering = '-pub_date'
    template_name = 'news_search.html'
    context_object_name = 'posts'
    paginate_by = 10

    def get_queryset(self):
        queryset = super().get_queryset()
        self.filterset = PostFilter(self.request.GET, queryset)
        return self.filterset.qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['time_now'] = datetime.utcnow()
        context['next_sale'] = None
        context['filterset'] = self.filterset
        return context


class ArticleDetail(DetailView):
    model = Post
    template_name = 'post.html'
    context_object_name = 'post'


class ArticleCreateView(CreateView):
    model = Post
    form_class = ArticleForm
    template_name = 'article_edit.html'
    success_url = reverse_lazy('post_list')

    def form_valid(self, form):
        form.instance.type_post = Post.ARTICLE
        return super().form_valid(form)


class ArticleUpdateView(LoginRequiredViewMixin, UpdateView):
    model = Post
    form_class = ArticleForm
    template_name = 'post_edit.html'
    success_url = '/articles/'


class ArticleDeleteView(DeleteView):
    model = Post
    template_name = 'article_delete.html'
    success_url = reverse_lazy('post_list')


class IndexView(LoginRequiredMixin, TemplateView):
    template_name = 'index.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['is_not_authors'] = not self.request.user.groups.filter(name='authors').exists()
        return context


@login_required
def upgrade_me(request):
    user = request.user
    authors_group = Group.objects.get(name='authors')
    if not request.user.groups.filter(name='authors').exists():
        authors_group.user_set.add(user)
    return redirect('/')


class BaseRegisterView(CreateView):
    model = User
    form_class = BaseRegisterForm
    success_url = '/'


class CategoryListView(ListView):
    model = Post
    template_name = 'category_list.html'
    context_object_name = 'category_news_list'

    def get_queryset(self):
        self.category = get_object_or_404(Category, id=self.kwargs['pk'])
        queryset = Post.objects.filter(category=self.category).order_by('-pub_date')
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['is_not_subscriber'] = self.request.user not in self.category.subscribers.all()
        context['category'] = self.category
        return context


@login_required
def subscribe(request, pk):
    user = request.user
    category = Category.objects.get(id=pk)
    category.subscribers.add(user)

    message = 'Вы успешно подписались рассылку'
    return render(request, 'subscribe.html', {'category':category, 'message':message})


def weekly_news(request):
    today = datetime.datetime.now()
    last_week = today - datetime.timedelta(days=7)
    posts = Post.objects.filter(date__gte=last_week)
    categories = set(posts.values_list('category__name', flat=True))
    subscribers = set(Category.objects.filter(name__in=categories).values_list('subscribers__email', flat=True))
    html_content = render_to_string('weekly_news.html', {'link': settings.SITE_URL, 'posts': posts})

    msg = EmailMultiAlternatives(
        subject='Weekly News', body='', from_email=settings.DEFAULT_FROM_EMAIL, to=subscribers,
    )

    msg.attach_alternative(html_content, 'text/html')
    msg.send()

    return HttpResponse("Weekly news sent successfully!")


class FeedbackList(LoginRequiredMixin, ListView):
    model = Feedback
    template_name = 'feedbacks.html'
    context_object_name = 'feedbacks'
    paginate_by = 6
    pk_url_kwarg = "post_id"

    def get_queryset(self):
        post_id = self.kwargs['post_id']
        return Feedback.objects.filter(post=post_id)


class FeedbackListUser(LoginRequiredMixin, ListView):
    model = Feedback
    template_name = 'feedbacks_user.html'
    context_object_name = 'feedbacks_user'
    paginate_by = 6
    pk_url_kwarg = "post_id"

    def get_queryset(self):
        post_id = self.kwargs['post_id']
        return Feedback.objects.filter(post=post_id)


class FeedbackDetail(DetailView):
    model = Feedback
    template_name = 'feedback.html'
    context_object_name = 'feedback'


@login_required
def feedback_create(request):
    form = FeedbackForm
    if request.method == 'POST':
        form = FeedbackForm(request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect('/')
    return render(request, 'feedback_edit.html', {'form': form})


class FeedbackDelete(LoginRequiredMixin, DeleteView):
    model = Post
    template_name = 'feedback_delete.html'
    success_url = reverse_lazy('post')
    
    
class FeedAccept(View):
    model = Feedback
    template_name = 'feed_accept.html'
    context_object_name = 'feed_accept'

    def get(self, request, accept_alert=None):
        accept_alert.delay()
        return request


def filter_posts(request):
    current_user = request.user
    posts = Post.objects.filter(user=current_user)
    return render(request, 'user_posts.html', {'posts': posts})


class PostDetailUser(LoginRequiredMixin, DetailView):
    model = Post
    template_name = 'post_user.html'
    context_object_name = 'post_user'