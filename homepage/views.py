from django.shortcuts import render
# from django.views.generic.list import ListView
from user_feeds.models import Post
from user_feeds.models import Category
from django.core.paginator import Paginator


# class HomepageListView(ListView):
#     model = Post
#     paginate_by = 8
#     context_object_name = 'allpostinhome'
#     template_name='homepage/homepage.html'
  

def home(request):

    category = request.GET.get('category')
    if category == None:
        posts = Post.objects.all()
    else:
        posts = Post.objects.filter(category__name=category)
    categories = Category.objects.all()

    # posts = Post.objects.all()
    paginator = Paginator( posts , 6) # Show 6 contacts per page.
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

   

   
    return render(request,'homepage/homepage.html',{'posts':page_obj,'categories':categories,})

    # 'allpostinhome':allpostinhome,
    # 'categories':categories,


# def latest(request):
#     latest= Post.objects.order_by('-post_date')[:5]


#     return render(request,'homepage/homepage.html',{'latest':latest})

#  #Detailpage view
# class PostDetailView(DetailView):
#     model=Post
#     context_object_name = 'allpostinhome-details'
#     template_name='user_feeds/detail.html'

