 
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
            
            ydl_opts = {}
            with youtube_dl.YoutubeDL(ydl_opts) as ydl:
                info = ydl.extract_info(l, download=False)
                download_target = ydl.prepare_filename(info)
            a=download_target
            print(a)
            b=download_target[-3:]
            print(b)
            
            if (b=="mp4" or b=="mkv"):
                a=download_target[:-3]
                print(a)
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
            
            return response
        
            return redirect('post_detail', pk=post.pk)
    else:
        form = PostForm()
    return render(request, 'blog/post_edit.html', {'form': form,'page_views':v})
