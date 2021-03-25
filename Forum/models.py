from django.db import models
from django.conf import settings
from django.urls import reverse
from django.contrib.auth.models import User

    

class Discussion(models.Model):
    title = models.CharField(max_length=200,null=True,blank=True)
    creator = models.ForeignKey(User, on_delete=models.CASCADE,null=True)  #settings.AUTH_USER_MODEL
    qustion = models.TextField()
    qustion_date = models.DateTimeField(auto_now_add=True)
    qustion_updated = models.DateField(auto_now=True)
    image=models.ImageField(upload_to='post_images', blank=True, null=True)
    category = models.ForeignKey('Category',on_delete=models.CASCADE, null=True, blank=True)
    view_count=models.IntegerField(default=0)
   # slug=models.SlugField(blank=True,unique=True)  

    def __str__(self):
        return str(self.creator) + '---' + str(self.title)
 
    # def get_absolute_url(self):
    #     return reverse('user_feeds:articale-detail', kwargs={'pk':self.pk})

    class Meta:
        ordering = ['-qustion_date']



class Category(models.Model):
    name = models.CharField(max_length=200)
   
    def __str__(self):
        return self.name



class Answer(models.Model):
    post = models.ForeignKey('Discussion', on_delete=models.CASCADE, related_name='discussion')
    created_by = models.ForeignKey(User,on_delete=models.CASCADE,blank=True, null=True)          
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



        






