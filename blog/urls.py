from django.urls import path
from . import views
from django.conf.urls import url
from django.urls import include,path

#from myapp.views import generate_random_user, get_task_info


#app_name = 'blog'
urlpatterns = [
    path('', views.post_list, name='post_list'),
    path('post/new/', views.post_new, name='post_new'),
    path('post/<int:pk>/', views.post_detail, name='post_detail'),
   # path('generate-user/', views.generate_random_user, name='generate_random_user'),
   # path('get-task-info/', views.get_task_info, name='get_task_info'),    
    #url(r'^celery-progress/', include('celery_progress.urls')),
   # path('post/new', views.post_new, name='post_new'),
   # path('post/<int:pk>/edit/', views.post_edit, name='post_edit'),

]
