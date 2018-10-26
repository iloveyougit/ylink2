 
from django.shortcuts import redirect
from django.shortcuts import render
from django.utils import timezone
from .models import Post
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
def post_list(request):
    posts=Post.objects.filter(published_date__lte=timezone.now()).order_by('published_date')
    return render(request, 'blog/post_list.html', {'posts': posts})

def post_detail(request, pk):
    post = get_object_or_404(Post, pk=pk)
    return render(request, 'blog/post_detail.html', {'post': post})

def post_new(request):
    if request.method == "POST":
        form = PostForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.published_date = timezone.now()
            post.save()
            l=post.text

            ydl_opts = {}
           
           
            url="youtube-dl --extract-audio --audio-format mp3 "+l
            command = url
            call(command.split(), shell=False)

            with youtube_dl.YoutubeDL(ydl_opts) as ydl:
                info = ydl.extract_info(l, download=False)
                download_target = ydl.prepare_filename(info)
                #ydl.download([url])
            a=download_target
            b=download_target[-3:]
            if (b!="mp4" or b!="mkv"):
                a=download_target[:-3]
            else:
                a=download_target[:-4]
                
            a+="mp3"
            print(a)
            filepath = a
           # return serve(request, os.path.basename(filepath), os.path.dirname(filepath))
            
            '''r = requests.get(path, allow_redirects=True)
            open('google.mp3', 'wb').write(r.content)
            '''
            wrapper = FileWrapper(open(filepath, 'rb'))
            response = HttpResponse(wrapper, content_type='audio/mp3')
            response['Content-Disposition'] = 'attachment; filename=%s' % os.path.basename(filepath)
            response['Content-Length'] = os.path.getsize(filepath)
            return response
        
            return redirect('post_detail', pk=post.pk)
    else:
        form = PostForm()
    return render(request, 'blog/post_edit.html', {'form': form})



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
