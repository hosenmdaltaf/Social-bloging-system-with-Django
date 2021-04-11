from django.shortcuts import render,get_object_or_404,redirect,HttpResponseRedirect
from django.urls import reverse_lazy
from django.contrib import messages
from django.contrib.auth.models import User
from django.views.generic import (
     DetailView,
     CreateView,
     ListView,
    #  DeleteView
)
from django.views.generic.edit import(
        DeleteView,
        UpdateView
)
from .forms import CommentForm 
from profiles.models import Profile
from user_feeds.models import Post
from user_feeds.models import Comment
from Forum.models import Discussion
from itertools import chain
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse


# def sidebar(request):
#     latest = Post.objects.order_by('-post_date')[:5]
#     latets_forum_question = Discussion.objects.order_by('-qustion_date')[:3]
#     return render(request,'user_feeds/sidebar.html',
#     {'latest':latest,'latets_forum_question':latets_forum_question})


def userFeedpage(request):
    latest= Post.objects.order_by('-post_date')[:5]
    latets_forum_question = Discussion.objects.order_by('-qustion_date')[:3]

    allposts =Post.objects.all()
    # post = get_object_or_404(Post, id=id)

    # fav = bool

    # if post.favourites.filter(id=request.user.id).exists():
    #     fav = True
    
    search_input = request.GET.get('search-area') or ''
    allprofile = Profile.objects.all()
    if search_input:
        allprofile = allprofile.filter(user__startswith=search_input)
    else:
        messages.success(request,f"Sorry we dont't find any user on this name..........." )


    
   
   #get logged in user profile
    profile = Profile.objects.get(user=request.user)

    # following_posts = allposts.exclude(author__user=profile.followers.all())

    users = profile.followers.all()

    users |= User.objects.filter(pk=request.user.pk)

    following_posts = allposts.filter(author__user__id__in = users)

    
    return render(request,'user_feeds/my_feed.html',{'allposts':following_posts,
    'latest':latest,'latets_forum_question':latets_forum_question,'search_input':search_input })


@ login_required
def like(request):
    if request.POST.get('action') == 'post':
        result = ''
        id = int(request.POST.get('postid'))
        post = get_object_or_404(Post, id=id)
        if post.likes.filter(id=request.user.id).exists():
            post.likes.remove(request.user)
            post.like_count -= 1
            result = post.like_count
            post.save()
        else:
            post.likes.add(request.user)
            post.like_count += 1
            result = post.like_count
            post.save()

        return JsonResponse({'result': result, })


@ login_required
def favourite_list(request):
    new = Post.objects.filter(favourites=request.user)
    return render(request,
                  'user_feeds/favourites.html',
                  {'new': new})


@ login_required
def favourite_add(request, id):
    post = get_object_or_404(Post, id=id)
    if post.favourites.filter(id=request.user.id).exists():
        post.favourites.remove(request.user)
    else:
        post.favourites.add(request.user)
    return HttpResponseRedirect(request.META['HTTP_REFERER'])



#post Create page view
class PostCreateView(CreateView):
    model=Post
    fields=['title','image','content','category']
    template_name='user_feeds/post_create_form.html'
    success_url = reverse_lazy("user_feeds:profile-page")

  
    def form_valid(self,form):
        # # form.instance.author =self.request.user
        form.instance.author =self.request.user.profile
        return super().form_valid(form)

   
# #Detailpage view
# class PostDetailView(DetailView):
#     model=Post
#     context_object_name = 'details'
#     template_name='user_feeds/detail.html'

#     def get_context_data(self,*args,**kwargs):
#         context = super().get_context_data(*args,**kwargs)
#         context['latest']= Post.objects.order_by('-date')[:5]
#         return context

#     def get_queryset(self):
#          return Post.objects.all()


def postdetail(request,id): 
    details=Post.objects.get(id=id)
    post = get_object_or_404(Post, id=id)
    latest= Post.objects.order_by('-post_date')[:5]
    latets_forum_question = Discussion.objects.order_by('-qustion_date')[:3]
   
    comments_form = CommentForm()   

    if request.method == 'POST': 
        comments_form = CommentForm(request.POST )  
        if comments_form.is_valid(): 
            comments_form.instance.created_by = request.user.profile
            comment = comments_form.save(commit=False)
            comment.post = details
            comments_form.save() 
            return redirect("user_feeds:articale-detail", id=post.id )  
        else: 
            comments_form = CommentForm() 

    comments=Comment.objects.filter(post=post)
    return render(request,'user_feeds/detail.html',{'details':details,
    'comments':comments,'latest':latest,'latets_forum_question':latets_forum_question })

#  ,'comments':comments

#post Update page view
class PostUpdateView(UpdateView):
    model = Post
    fields ='__all__'
    # fields = ['title','image','details']
    template_name='user_feeds/post_update_form.html'
    success_url = reverse_lazy("user_feeds:profile-page")

    def form_valid(self,form):
        form.instance.author =self.request.user
        return super().form_valid(form)


#post Delete page view
class PostDeleteView(DeleteView):
    model=Post
    template_name='user_feeds/post_delete_form.html'
    success_url = reverse_lazy("user_feeds:profile-page")