from django.shortcuts import render,get_object_or_404
from django.views.generic import ListView,DetailView,CreateView,UpdateView,DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin,UserPassesTestMixin
from django.contrib.auth.models import User
from .models import Post

# Create your views here.

def home(request):
    context={'posts': Post.objects.all()}
    return render(request,'BlogApplication/home.html',context) #importing template home in view


class PostListView(ListView):
    model = Post
    template_name = 'BlogApplication/home.html'
    context_object_name = 'posts'
    ordering = ['-date_posted']
    paginate_by =2
class UserPostListView(ListView):
    model = Post
    template_name = 'BlogApplication/user_posts.html'
    context_object_name = 'posts'
    paginate_by = 2

    def get_queryset(self):
        user=get_object_or_404(User,username=self.kwargs.get('username'))
        return Post.objects.filter(author=user).order_by('-date_posted')

class PostDetailView(DetailView):
    model = Post

class PostCreateView(LoginRequiredMixin,CreateView):
    model = Post
    fields = ['title','content']
    def form_valid(self, form):
        form.instance.author=self.request.user
        return super().form_valid(form)

class PostUpdateView(LoginRequiredMixin,UserPassesTestMixin,UpdateView):
    model = Post
    fields = ['title','content']
    def form_valid(self, form):
        form.instance.author=self.request.user
        return super().form_valid(form)

    def test_func(self):
        post=self.get_object()
        if self.request.user== post.author:
            return True
        return False

class PostDeleteView(LoginRequiredMixin,UserPassesTestMixin,DeleteView):
    model = Post
    success_url = '/'

    def test_func(self):
        post=self.get_object()
        if self.request.user== post.author:
            return True
        return False

def about(request):
    return render(request,'BlogApplication/about.html',{'title':'About'}) #importing template about in view

def search_blog(request):
    query = request.GET.get('q', '')  # Get the search query from the 'q' parameter in the request GET parameters

    if query:
        results = Post.objects.filter(title__icontains=query)
    else:
        results = None

    return render(request, 'BlogApplication/search.html', {'results': results, 'query': query})

