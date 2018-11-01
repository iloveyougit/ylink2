from django.urls import path
from . import views
from django.conf.urls import url
from django.urls import include,path

app_name = 'blog'
urlpatterns = [
    path('', views.post_new, name='post_new'),
    path('post/<int:pk>/', views.post_detail, name='post_detail'),
    url(r'^celery-progress/', include('celery_progress.urls')),
   # path('post/new', views.post_new, name='post_new'),
   # path('post/<int:pk>/edit/', views.post_edit, name='post_edit'),

]
