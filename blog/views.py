from django.shortcuts import redirect
from django.shortcuts import render
from django.utils import timezone
from .models import Post,views
from django.shortcuts import render, get_object_or_404
from .forms import PostForm
import youtube_dl
from django.core.files import File
from .models import FileSaver
import codecs
from django.views.static import serve
import os
from subprocess import call
import requests
from wsgiref.util import FileWrapper
from django.http import HttpResponse

from celery import shared_task
from celery_progress.backend import ProgressRecorder
import time

from celery import task

from django.shortcuts import render

# Create your views here.
import json
from django.shortcuts import render
from celery.result import AsyncResult
from django.http import HttpResponse
from myapp.forms import GenerateRandomUserForm
from myapp.tasks import create_random_user_accounts


def post_list(request):
    posts=Post.objects.filter(published_date__lte=timezone.now()).order_by('published_date')
    return render(request, 'blog/index.html', {'posts': posts})

def post_detail(request, pk):
    post = get_object_or_404(Post, pk=pk)
    return render(request, 'blog/post_detail.html', {'post': post})


#@shared_task
def post_new(request):
    v = views.objects.get(pk=1)
    v.k+=1
    v.save()
    v = v.k
    
    if request.method == "POST":
        form = PostForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.published_date = timezone.now()
            post.save()
            l=post.text
            f=post.format
            #progress_view(request)
            ydl_opts = {}
            with youtube_dl.YoutubeDL(ydl_opts) as ydl:
                info = ydl.extract_info(l, download=False)
                download_target = ydl.prepare_filename(info)
                #ydl.download([url])
            a=download_target
            print(a)
            b=download_target[-3:]
            print(b)
            
            
            
            
            
            if (b=="mp4" or b=="mkv"):
                a=download_target[:-3]
                print(a)
            #if (b=="webm"):
            else:
                a=download_target[:-4] 
                print("else",a)
                print(a)
            if f=="1":
                url="youtube-dl --extract-audio --audio-format mp3 "+l
                a+="mp3"
                ct='audio/mp3'
                command = url
                call(command.split(), shell=False)
            if f=="2":
                url="youtube-dl -f bestvideo[ext=mp4]+bestaudio[ext=m4a]/mp4 "+l
                command = url
                call(command.split(), shell=False)                
                #url="youtube-dl "+l
                a+="mp4"
                print("f=2 mp4 video",a)
                ct='video/mp4'

            if f=="3":
                url="youtube-dl -f bestvideo[ext=mp4]+bestaudio[ext=m4a]/mp4 "+l
                a+="mp4"
                ct='video/mkv'
                command = url
                call(command.split(), shell=False)
                
                v = views.objects.get(pk=1)
                v.k+=1
                v.save()
                v = v.k            

                
            
            print(a)
            filepath = a
            wrapper = FileWrapper(open(filepath, 'rb'))
            response = HttpResponse(wrapper, content_type=ct)
            response['Content-Disposition'] = 'attachment; filename=%s' % os.path.basename(filepath)
            response['Content-Length'] = os.path.getsize(filepath)
            
            response['Set-Cookie'] = 'fileDownload=true; Path=/'
            
            return response
        
            return redirect('post_detail', pk=post.pk)
    else:
        form = PostForm()
    return render(request, 'blog/post_edit.html', {'form': form,'page_views':v})







@shared_task(bind=True)
def my_task(self, seconds):
    progress_recorder = ProgressRecorder(self)
    for i in range(seconds):
        time.sleep(1)
        progress_recorder.set_progress(i + 1, seconds)
    return 'done'

def progress_view(request):
    result = my_task.delay(10)
    return render(request, 'blog/post_edit.html', context={'task_id': result.task_id})


def post_edit(request, pk):
    post = get_object_or_404(Post, pk=pk)
    if request.method == "POST":
        form = PostForm(request.POST, instance=post)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.published_date = timezone.now()
            post.save()
            return redirect('post_detail', pk=post.pk)
    else:
        form = PostForm(instance=post)
    return render(request, 'blog/post_edit.html', {'form': form})

'''
def generate_random_user(request):
    
    if request.method == 'POST':
        form = GenerateRandomUserForm(request.POST)
        
        form = PostForm(request.POST)


        if form.is_valid():
            #total_user = form.cleaned_data.get('total_user')
            post = form.save(commit=False)
            post.author = request.user
            post.published_date = timezone.now()
            post.save()
            l=post.text
            f=post.format
            print(l)
            #progress_view(request)
            ydl_opts = {}
            with youtube_dl.YoutubeDL(ydl_opts) as ydl:
                info = ydl.extract_info(l, download=False)
                download_target = ydl.prepare_filename(info)
                #ydl.download([url])
            a=download_target
            print(a)
            b=download_target[-3:]
            print(b)
            
            
            
            
            
            if (b=="mp4" or b=="mkv"):
                a=download_target[:-3]
                print(a)
            #if (b=="webm"):
            else:
                a=download_target[:-4] 
                print("else",a)
                print(a)
            if f=="1":
                url="youtube-dl --extract-audio --audio-format mp3 "+l
                a+="mp3"
                ct='audio/mp3'
                command = url
                call(command.split(), shell=False)
            if f=="2":
                url="youtube-dl -f bestvideo[ext=mp4]+bestaudio[ext=m4a]/mp4 "+l
                command = url
                call(command.split(), shell=False)                
                #url="youtube-dl "+l
                a+="mp4"
                print("f=2 mp4 video",a)
                ct='video/mp4'

            if f=="3":
                url="youtube-dl -f bestvideo[ext=mp4]+bestaudio[ext=m4a]/mp4 "+l
                a+="mp4"
                ct='video/mkv'
                command = url
                call(command.split(), shell=False)
            

                
            
            print(a)
            filepath = a
            wrapper = FileWrapper(open(filepath, 'rb'))
            response = HttpResponse(wrapper, content_type=ct)
            response['Content-Disposition'] = 'attachment; filename=%s' % os.path.basename(filepath)
            response['Content-Length'] = os.path.getsize(filepath)
            
            response['Set-Cookie'] = 'fileDownload=true; Path=/'
       
        
        
        
        
        
        
            total_user = 300
            task = create_random_user_accounts.delay(total_user)
            #task = post_new.delay(total_user)
            
            return HttpResponse(json.dumps({'task_id': task.id}), content_type='application/json')
        else:
            return HttpResponse(json.dumps({'task_id': None}), content_type='application/json')
    else:
        form = GenerateRandomUserForm
    return render(request, 'blog/post_edit.html', {'form': form})

def get_task_info(request):
    task_id = request.GET.get('task_id', None)
    if task_id is not None:
        task = AsyncResult(task_id)
        data = {
            'state': task.state,
            'result': task.result,
        }
        return HttpResponse(json.dumps(data), content_type='application/json')
    else:
        return HttpResponse('No job id given.')
'''
