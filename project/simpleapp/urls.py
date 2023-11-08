from django.urls import path

from . import views
from .views import PostList, PostDetail, PostCreate, PostUpdate, PostDelete, SearchList, ArticleCreateView, \
   ArticleUpdateView, ArticleDeleteView, BaseRegisterView, IndexView, upgrade_me, CategoryListView, subscribe, \
   FeedbackDetail, FeedbackList, FeedbackListUser, FeedbackDelete, FeedAccept, PostDetailUser, filter_posts
from django.contrib.auth.views import LoginView, LogoutView

urlpatterns = [
   path('posts/', PostList.as_view(), name='post_list'),
   path('posts/<int:pk>', PostDetail.as_view(), name='post_detail'),
   path('posts/create/',  PostCreate.as_view(), name='create_post'),
   path('posts/<int:pk>/edit/', PostUpdate.as_view(), name='post_update'),
   path('posts/<int:pk>/delete/', PostDelete.as_view(), name='post_delete'),
   path('posts/search/', SearchList.as_view(), name='news_search'),
   path('articles/create/', ArticleCreateView.as_view(), name='create_article'),
   path('articles/<int:pk>/edit/', ArticleUpdateView.as_view(), name='article_update'),
   path('articles/<int:pk>/delete/', ArticleDeleteView.as_view(), name='article_delete'),
   path('login/', LoginView.as_view(template_name='login.html'), name='login'),
   path('logout/', LogoutView.as_view(template_name='logout.html'), name='logout'),
   path('signup/', BaseRegisterView.as_view(template_name='signup.html'), name='signup'),
   path('sing/', IndexView.as_view()),
   path('upgrade/', upgrade_me, name='upgrade'),
   path('categories/<int:pk>', CategoryListView.as_view(), name='category_list'),
   path('categories/<int:pk>/subscribe', subscribe, name='subscribe'),
   path('feedback/<int:pk>/', FeedbackDetail.as_view(), name='feedback'),
   path('feedbacks/<int:post_id>/', FeedbackList.as_view(), name='feedbacks'),
   path('feedbacks_user/<int:post_id>/', FeedbackListUser.as_view(), name='feedbacks_user'),
   path('delete_feed/<int:pk>', FeedbackDelete.as_view(), name='feedback_delete'),
   path('accept/', FeedAccept.as_view(), name='feed_accept'),
   path('post_user/<int:pk>/', PostDetailUser.as_view(), name='post_user'),
   path('user_posts/', filter_posts, name='user_posts'),
   path('<int:pk>/', PostDetail.as_view(), name='post'),
]