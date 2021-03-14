from django.db import models
from django.conf import settings
from django.urls import reverse
# from account.models import Account
# from taggit.managers import TaggableManager
from django.contrib.auth.models import User
from profiles.models import Profile


class Post(models.Model):
    title = models.CharField(max_length=200,null=True,blank=True)
    author = models.ForeignKey(Profile, on_delete=models.CASCADE,null=True)  #settings.AUTH_USER_MODEL
    content = models.TextField()
    post_date = models.DateTimeField(auto_now_add=True)
    post_updated = models.DateField(auto_now=True)
    image=models.ImageField(upload_to='post_images', blank=True, null=True)
    category = models.ForeignKey('Category',on_delete=models.CASCADE, null=True, blank=True)
    # tags = TaggableManager()
#     rating = models.IntegerField()
#     security=
#    comment
#    share
    view_count=models.IntegerField(default=0)
   # slug=models.SlugField(blank=True,unique=True)

    def __str__(self):
        return str(self.author) + '---' + str(self.title)
 
    # def get_absolute_url(self):
    #     return reverse('user_feeds:articale-detail', kwargs={'pk':self.pk})

    class Meta:
        ordering = ['-post_date']



class Category(models.Model):
    name = models.CharField(max_length=200)
   
    def __str__(self):
        return self.name



class Comment(models.Model):
    post = models.ForeignKey('Post', on_delete=models.CASCADE, related_name='comments')
    created_by = models.ForeignKey(Profile,on_delete=models.CASCADE,blank=True, null=True)          
    text = models.TextField(blank=True, null=True )
    created_date = models.DateTimeField(auto_now_add=True)
    approved_comment = models.BooleanField(default=False)

    objects = models.Manager()
    def approve(self):
        self.approved_comment = True
        self.save()

    class Meta:
        ordering = ['-created_date']

    def __str__(self):
        return str(self.created_by)



        





