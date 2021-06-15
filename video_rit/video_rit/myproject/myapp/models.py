from django.db import models
from django.contrib.auth.models import User


# Create your models here.
class Video(models.Model):
    title = models.CharField(max_length=100)
    Description = models.CharField(max_length=200)
    keywords = models.CharField(max_length=50)
    video = models.FileField(upload_to='videos/')

    class Meta:
        verbose_name = 'video'
        verbose_name_plural = 'videos'

    def __str__(self):
        return self.title


class last_login(models.Model):
    username = models.CharField(max_length=20)
    password = models.CharField(max_length=20)


class video_details(models.Model):
    uploader = models.ForeignKey(User, on_delete=models.CASCADE)
    Date = models.DateField()
    video = models.ForeignKey(Video, on_delete=models.CASCADE)


class Search_words(models.Model):
    keywords = models.CharField(max_length=15)
    count = models.IntegerField()

    def __str__(self):
        return self.keywords + " " + str(self.count)


class feedback_model(models.Model):
    feedback = models.CharField(max_length=150)


class user_feedback(models.Model):
    username = models.ForeignKey(User, on_delete=models.CASCADE)
    feedback = models.ForeignKey(feedback_model, on_delete=models.CASCADE)
    Date = models.DateField()
    video = models.ForeignKey(Video, on_delete=models.CASCADE)


class chat_model(models.Model):
    username = models.ForeignKey(User, on_delete=models.CASCADE,null=True,blank=True)
    question = models.CharField(max_length=50)
    answer = models.CharField(max_length=300,null=True,blank=True)
