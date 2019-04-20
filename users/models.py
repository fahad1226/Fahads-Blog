from django.db import models
from django.contrib.auth.models import User
from PIL import Image
from django.conf import settings
from django.urls import reverse_lazy

class Profile(models.Model):

    user = models.OneToOneField(settings.AUTH_USER_MODEL,on_delete=models.CASCADE,related_name='profile')
    image = models.ImageField(default='default.jpg',upload_to='profile_pics')
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    public_info = models.TextField()
    nick_name = models.CharField(max_length=150)
    following = models.ManyToManyField(settings.AUTH_USER_MODEL,blank=True,related_name='followed_by')



    def __str__(self):

        return f'{self.user.username} Profile'



    def save(self,**kwargs):

        super().save()

        img = Image.open(self.image.path)

        if img.height > 300 or img.width > 300:

            output_size = (300,300)
            img.thumbnail(output_size)
            img.save(self.image.path)

    def is_following(self,user,followed_by_user):

        user_profile,created = Profile.objects.get_or_create(user=user)
        if created:
            return True

        if followed_by_user in user_profile.following.all():
            return True
        else:
            return False

        return redirect('user-detail',username=username)




    def get_follower_url(self):

        return reverse_lazy('user-follow',kwargs={"username":self.user.username})

    def get_absolute_url(self):

        return reverse_lazy('user-detail',kwargs={"username":self.user.username})
