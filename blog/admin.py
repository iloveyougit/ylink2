from django.contrib import admin

# Register your models here.
from .models import Post,views

admin.site.register(Post)
admin.site.register(views)
