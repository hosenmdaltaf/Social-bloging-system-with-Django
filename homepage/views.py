from django.shortcuts import render
# from django.views.generic.list import ListView
from user_feeds.models import Post
from user_feeds.models import Category


# class HomepageListView(ListView):
#     model = Post
#     paginate_by = 8
#     context_object_name = 'allpostinhome'
#     template_name='homepage/homepage.html'
  

def home(request):
    
    category = request.GET.get('category')
    if category == None:
        allpostinhome = Post.objects.all()
    else:
        allpostinhome = Post.objects.filter(category__name=category)
    categories = Category.objects.all()
   
    return render(request,'homepage/homepage.html',{'allpostinhome':allpostinhome,'categories':categories})


# def latest(request):
#     latest= Post.objects.order_by('-post_date')[:5]


#     return render(request,'homepage/homepage.html',{'latest':latest})

#  #Detailpage view
# class PostDetailView(DetailView):
#     model=Post
#     context_object_name = 'allpostinhome-details'
#     template_name='user_feeds/detail.html'

