from django.shortcuts import render,get_object_or_404,redirect
from django.views.generic import TemplateView
from .models import Post
from django.views.generic import View,ListView,DetailView,CreateView,UpdateView,DeleteView,RedirectView
from django.contrib.auth.mixins import LoginRequiredMixin,UserPassesTestMixin
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.db.models import Q
from django.contrib.auth import update_session_auth_hash
from django.contrib import messages
from .forms import CommentsForm
from django.contrib.auth.forms import PasswordChangeForm
from users.models import Profile

"""Posts = [
    {
        'author':'Fahad Bin Munir',
        'title':'About Java',
        'content':'this is my first post about java programming language,hope u guys will like it',
        'date_posted':'January 28 2019'
    },

    {
        'author':'Jon Snow',
        'title':'About C Programming',
        'content':'this is my first post about C programming language,hope u guys will enjoy it',
        'date_posted':'January 28 2019'
    },

    {
        'author':'Rasik Hawk',
        'title':'About Meme',
        'content':'this is my first post about facebok meme,hope u guys will like it guyz',
        'date_posted':'January 28 2019'
    }

]
"""
@login_required
def Home(request):
    context={
        'my_posts':Post.objects.all(),
        'title':'Facebook',
    }
    return render(request,'home.html',context)

class PostListView(LoginRequiredMixin ,ListView):

    model = Post
    template_name = 'home.html'
    context_object_name = 'my_posts'
    ordering = ['-date']
    paginate_by = 4

    #searching function
    def get_queryset(self):
        result = super(PostListView, self).get_queryset()
        query = self.request.GET.get('q')

        #query = self.request.GET.get('q')
        if query:
            postresult = Post.objects.filter(
            Q(title__icontains=query) |
            Q(content__icontains=query)|
            Q(author__first_name__icontains = query)|
            Q(author__last_name__icontains = query)|
            Q(author__username__icontains = query)
            ).order_by('-date')
            result = postresult
        return result


class UserPostListView(LoginRequiredMixin ,ListView):

    model = Post
    template_name = 'user_post.html'
    context_object_name = 'my_posts'
    paginate_by = 4

    def get_success_url(self):

        username = self.kwargs['username']
        return reverse('post-user', kwargs={'username': username})

    def get_queryset(self):

        user = get_object_or_404(User,username=self.kwargs.get('username'))
        return Post.objects.filter(author=user).order_by('-date')



class UserDetailView(DetailView):

    #template_name = 'new_profile.html'
    template_name = 'profile.html'
    queryset = User.objects.all()

    def get_object(self):
        return get_object_or_404(User,username__iexact=self.kwargs.get('username'))


class PostDetailView(LoginRequiredMixin,DetailView):
    model = Post
    template_name = 'post_detail.html'


class PostLikeRedirect(RedirectView):

    def get_redirect_url(self,pk):

        obj = get_object_or_404(Post,pk=pk)
        url_ = obj.get_absolute_url()
        user = self.request.user
        if user.is_authenticated:
            if user in obj.likes.all():
                obj.likes.remove(user)
            else:
                obj.likes.add(user)
        return url_



def add_comment(request,pk):

    post = get_object_or_404(Post,pk=pk)
    form = CommentsForm(request.POST)

    if request.method == 'POST':

        if form.is_valid():
            comment = form.save(commit=False)
            comment.post = post
            comment.author = request.user
            comment.save()
            return redirect('post-detail',pk)

        else:

            form = CommentsForm()


    template = 'add_comments.html'
    context = {'form':form}

    return render(request,template,context)


class PostCreateView(LoginRequiredMixin,CreateView):

    model = Post
    fields = ['title','content']
    template_name = 'post_form.html'

    def form_valid(self,form):
        form.instance.author = self.request.user
        return super().form_valid(form)


class PostUpdateView(LoginRequiredMixin,UserPassesTestMixin,UpdateView):

    model = Post
    fields = ['title','content']
    template_name = 'post_form.html'

    def form_valid(self,form):
        form.instance.author = self.request.user
        return super().form_valid(form)

    def test_func(self):
        post = self.get_object()
        if self.request.user == post.author:
            return True
        return False



class PostDeleteView(LoginRequiredMixin,UserPassesTestMixin ,DeleteView):
    model = Post
    template_name = 'post_confirm_delete.html'
    success_url = '/'

    def test_func(self):
        post = self.get_object()
        if self.request.user == post.author:
            return True
        return False

@login_required
def change_password(request):
    if request.method == 'POST':
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            #update_session_auth_hash(request, user)  # Important!
            messages.success(request, 'Your password was successfully updated!')
            return redirect('login')
        else:
            messages.error(request, 'Please correct the error below.')
    else:
        form = PasswordChangeForm(request.user)
    return render(request, 'change_password.html', {
        'form': form
    })


def About(request):

    return render(request,'about.html',context={'title':'About-Facebook'})
