from django.shortcuts import render,get_object_or_404,redirect
from django.urls import reverse_lazy
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


class UserFeedpageListView(ListView):
    model = Post
    # paginate_by = 10
    context_object_name = 'allposts'
    template_name='user_feeds/my_feed.html'

    def get_context_data(self,*args,**kwargs):
        context = super().get_context_data(*args,**kwargs)
        context['latest']= Post.objects.order_by('-post_date')[:5]
        return context

#post Create page view
class PostCreateView(CreateView):
    model=Post
    fields=['title','image','content','category']
    template_name='user_feeds/post_create_form.html'
    success_url = reverse_lazy("user_feeds:profile-page")

  
    # def form_valid(self,form):
    #     # form.instance.user = profile.request.user
    #     form.instance.user.id ==  self.profile.user.id
    #     return super().form_valid(form)

    def form_valid(self,form):
        form.instance.author =self.request.user
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
   
    comments_form = CommentForm()  

    if request.method == 'POST': 
        comments_form = CommentForm(request.POST ) 
        if comments_form.is_valid(): 
            # comments_form.instance.created_by = profile.request.user
            comment = comments_form.save(commit=False)
            comment.post = details
            comments_form.save() 
            return redirect("user_feeds:articale-detail", id=post.id )  
        else: 
            comments_form = CommentForm() 

    comments=Comment.objects.filter(post=post)
    return render(request,'user_feeds/detail.html',{'details':details,'comments':comments,'latest':latest})

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