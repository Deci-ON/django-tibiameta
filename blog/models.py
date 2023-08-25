from django.db import models
from django.utils import timezone  
from ckeditor_uploader.fields import RichTextUploadingField
from ckeditor.fields import RichTextField

# Create your models here.
class Post(models.Model):
    author = models.CharField(max_length=255)
    title = models.CharField(max_length=255)
    subtitle = models.CharField(max_length=255)
    resume = RichTextField(null=True, blank=True)
    content = RichTextUploadingField()
    imagem_capa = models.ImageField(null=True, blank=True, upload_to='static/blog/')
    date_publi = models.DateTimeField(default=timezone.now())

    def __str__(self):
        return self.title