from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from django.utils.text import slugify
from django.db.models.signals import pre_save, post_delete
from django.dispatch import receiver
from django.shortcuts import reverse, redirect
import PIL

# Create your models here.

def upload_location(instance, filename, *args, **kwargs):
    file_path = 'media/{author_id}/{title}-{filename}'.format(
        author_id=str(instance.author.id), title=str(instance.title), filename= filename
    )
    return file_path

class Post(models.Model):
    title = models.CharField(max_length=100)
    content = models.TextField()
    date_posted = models.DateTimeField(default=timezone.now)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    image = models.ImageField(upload_to=upload_location, null=False, blank=False)
    slug = models.SlugField(blank=True, unique=False)


    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('post-detail', kwargs={'pk': self.pk})


@receiver(post_delete, sender=Post)
def submission_delete(sender, instance, **kwargs):
    instance.image.delete(False)

def pre_save_post_receiver(sender, instance, *args, **kwargs):
    if not instance.slug:
        instance.slug = slugify(instance.author.username + "-" + instance.title)
pre_save.connect(pre_save_post_receiver, sender=Post)


class DateTimeTest(models.Model):
    date = models.DateTimeField(null=True, blank=True)

class Appointment(models.Model):
    blaze = models.CharField(max_length=20)
    email = models.EmailField(null=True)
    date = models.DateField(null=True, blank=True)
    time = models.TimeField(default=timezone.now().strftime('%H'))
    confirmed = models.BooleanField(default=False)
