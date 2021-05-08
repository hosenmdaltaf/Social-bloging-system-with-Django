from django.shortcuts import render,redirect,get_object_or_404
from django.contrib.auth.forms import AuthenticationForm     #UserCreationForm,
from django.contrib.auth import login,logout
from django.contrib import messages
from .forms import UserRegisterForm
from profiles.models import Profile, Notification
from django.contrib.auth.models import User
from django.http import Http404
from django.urls import reverse_lazy
from django.views.generic import (
      DetailView,
    #   CreateView,
      UpdateView,
      ListView,
      DeleteView
)

from django.db.models import Q
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator

from django_private_chat2.models import DialogsModel


# @method_decorator(login_required, name='dispatch')
# class UserListView(ListView):
#     model = User
#     # These next two lines tell the view to index lookups by username
#     slug_field = 'username'
#     slug_url_kwarg = 'username'
#     template_name = 'profiles/chats.html'
#     login_url = '/profiles/login/'


@login_required(login_url ='/profiles/login/')
def follow_and_unfolow(request):
    if request.method =='POST':
        pk= request.POST.get('profile_pk')
        target_user= User.objects.get(pk=pk)
        existing_dialogs_model = DialogsModel.objects.filter(Q(user1=request.user, user2=target_user) | Q(user1=target_user, user2=request.user)).first()

        if target_user in request.user.profile.followers.all():
            notification_message = str(request.user.username) + " is unfollowed you"
            request.user.profile.followers.remove(target_user)
            if existing_dialogs_model:
                existing_dialogs_model.delete()
        else:
            notification_message = str(request.user.username) + " is following you"
            request.user.profile.followers.add(target_user)
            if (request.user in target_user.profile.followers.all()) and (not existing_dialogs_model):
                DialogsModel.objects.create(user1=request.user, user2=target_user)
        Notification.objects.create(sender=request.user, receiver=target_user, message=notification_message)
        return redirect(request.META.get('HTTP_REFERER'))
    return redirect('profiles:all_profile')


@login_required
def notification_view(request):
    notifications = Notification.objects.filter(receiver=request.user)
    return render(request,'profiles/notification.html',{'notifications':notifications})

    
@method_decorator(login_required, name='dispatch')
class Profile_list_View(ListView):
    model = Profile
    # paginate_by = 3
    context_object_name = 'profiles_list'
    template_name='profiles/profile_list.html'

    def get_queryset(self):
        return Profile.objects.all().exclude(user=self.request.user)


@method_decorator(login_required, name='dispatch')
class SearchResultsView(ListView):
    model = Profile
    template_name = 'profiles/search.html'
    context_object_name = 'profiles_list_search'

    def get_queryset(self): # new
        query = self.request.GET.get('q')
        object_list = Profile.objects.filter(
            Q(user__username__icontains=query) | Q(full_name__icontains=query)
        )
        return object_list



@method_decorator(login_required, name='dispatch')
class ProfileDetailView(DetailView):
    model = Profile
    context_object_name = 'profiles'
    template_name = 'profiles/user_profile_page.html' 

    def get_object(self,**kwargs):
        pk= self.kwargs.get('pk')
        view_profile = Profile.objects.get(pk=pk)
        return view_profile

    def get_context_data(self,*args,**kwargs):
        context = super().get_context_data(*args,**kwargs)
        view_profile = self.get_object()
        my_profile = Profile.objects.get(user=self.request.user)
        if view_profile.user in my_profile.followers.all():
            follow=True
        else:
            follow= False
        context['follow'] = follow 
        return context


@method_decorator(login_required, name='dispatch')
class ProfileUpdateView(UpdateView):
    model = Profile
    # context_object_name = 'profiles'
    fields=['profile_picture','bio','full_name','work','loaction','educations','email']
    template_name='profiles/profile_update_form.html'
    success_url = reverse_lazy("user_feeds:profile-page")

    # def form_valid(self,form):
    #     form.instance = self.request.user
    #     return super().form_valid(form)


@method_decorator(login_required, name='dispatch')
class ProfileDeleteView(DeleteView):
    model=Profile
    # context_object_name = 'profile_delete'
    template_name='profiles/profile_delete_form.html'
    success_url = reverse_lazy("homepage:article-list")



# def profiles_detail(request,id): 
    
#     profiles=Profile.objects.get(id=id)
#     # profiles = get_object_or_404(Profile, id=id)
#     # profiles= Profile.objects.get(user=request.user)
#     return render(request,'profiles/user_profile_page.html',{'profiles':profiles})


def signup(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            email = form.cleaned_data.get('email')
            messages.success(request,f'Your account has created ! You are now able to log in')
            return redirect ('profiles:login')
    else:
        form =UserRegisterForm()
    return render (request,'profiles/signup.html',{'form':form})

# def signup(request):
#     #user register form
#     if request.method == 'POST':
#         form = UserCreationForm(request.POST)
#         if form.is_valid():
#            user = form.save()
#             #log in user
#            login(request,user)
#            return redirect('accounts:login')
#     else:
#         form=UserCreationForm()

#     return render(request,'accounts/signup.html',{'form':form})

def login_view(request):
    if request.method == 'POST':
        form=AuthenticationForm(data=request.POST)
        if form.is_valid():
            #login the user
            user=form.get_user()
            login(request,user)
            return redirect('user_feeds:profile-page')
    else:
        form=AuthenticationForm()
    return render(request,'profiles/login.html',{'form':form})


@login_required(login_url ='/profiles/login/')
def logout_view(request):
    if request.method == 'POST':
        logout(request)
        return redirect('profiles:logout')
    return render(request,'profiles/logout.html')




