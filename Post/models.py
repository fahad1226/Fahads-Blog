from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from django.urls import reverse
from django.conf import settings


class Post(models.Model):

    title = models.CharField(max_length=150)
    content = models.TextField()
    date = models.DateTimeField(default=timezone.now)
    author = models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE)
    likes = models.ManyToManyField(settings.AUTH_USER_MODEL,blank=True,related_name='posts_likes')

    def __str__(self):

        return self.title

    def get_absolute_url(self):

        return reverse('post-detail',kwargs={'pk':self.pk})

    def get_like_url(self):

        return reverse('post-likes',kwargs={'pk':self.pk})

    # def get_absolute_url(self):
    #
    #     return reverse('user-detail',kwargs={'username':self.username})


class Comments(models.Model):

    post = models.ForeignKey(Post,on_delete=models.CASCADE,related_name="comments")
    author = models.ForeignKey(User,on_delete=models.CASCADE,)
    content = models.TextField()
    created = models.DateTimeField(auto_now_add=True)
    approved = models.BooleanField(default=False)

    def approved(self):

        self.approved = True
        self.save()

    def __str__(self):

        return f'{self.content} by {self.author} Comments'

        #return '{}-{}'.format(self.post.title,str(self.user.username))
