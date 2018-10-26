from django.db import models
from django.utils import timezone


TYPES = (  
    ('1','mp3'),
    ('2','mp4'),
    ('3','mkv'),

)
#class Format(models.Model):
#    name = models.CharField(max_length=3,choices=TYPES)
class Post(models.Model):
    author = models.ForeignKey('auth.User', on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    text = models.TextField()
    created_date = models.DateTimeField(
            default=timezone.now)
    published_date = models.DateTimeField(
            blank=True, null=True)
    format    = models.CharField(max_length=3, choices=TYPES)
    #format = models.ForeignKey(Format, on_delete=models.SET_NULL, null=True)

    def publish(self):
        self.published_date = timezone.now()
        self.save()

    def __str__(self):
        return self.title

class FileSaver(models.Model):

    myfile = models.FileField(upload_to="files/")

    class Meta:
        managed=False

