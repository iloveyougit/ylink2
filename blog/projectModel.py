from django.db import models
from django.utils import timezone
TYPES = (  
    ('1','mp3'),
    ('2','mp4'),
    ('3','mkv'),

)
class views(models.Model):
    k = models.PositiveIntegerField(default = 0)
    
   
class Post(models.Model):
    title = models.CharField(max_length=200)
    text = models.CharField(max_length=200)
    created_date = models.DateTimeField(
            default=timezone.now)
    published_date = models.DateTimeField(
            blank=True, null=True)
    format    = models.CharField(max_length=3, choices=TYPES)

    def publish(self):
        self.published_date = timezone.now()
        self.save()

    def __str__(self):
        return self.title

