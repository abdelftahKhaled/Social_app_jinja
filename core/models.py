from django.db import models
from django.contrib.auth.models import User


class Profile(models.Model):
    user=models.OneToOneField(User,on_delete=models.CASCADE)
    image=models.ImageField(upload_to="profile_picture",default="blank-profile-picture.png")
    cuver=models.ImageField(upload_to="cuver_picture",null=True,default="download (1).jfif")
    locatios=models.TextField(max_length=50,null=True,)
    bio=models.TextField(max_length=50,null=True,)
    def __str__(self):

        return self.user.username

class Post(models.Model):
    host= models.ForeignKey(User,on_delete=models.CASCADE)   
    image=models.ImageField(upload_to="Post_image",null=True)
    caption=models.CharField(max_length=100,null=True)
    upload=models.DateTimeField(auto_now_add=True)
   #edit=models.DateTimeField(auto_add=True,)
    no_likes=models.BigIntegerField(default=0,)

    def __str__(self):
        return self.caption
class follower(models.Model):
      
      user=models.ForeignKey(User,on_delete=models.CASCADE)
      Follower=models.CharField(max_length=50,)


class like(models.Model):
      post=models.ForeignKey(Post,on_delete=models.CASCADE)
      person_liker=models.ForeignKey(User,on_delete=models.CASCADE)
      upload=models.DateTimeField(auto_now_add=True)

class Comment(models.Model):

     post=models.ForeignKey(Post,on_delete=models.CASCADE)
     person_comment=models.ForeignKey(User,on_delete=models.CASCADE)
     upload=models.DateTimeField(auto_now_add=True)
     body=models.CharField(max_length=50)
     def __str__(self):
            return self.body
      
     
