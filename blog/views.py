from django.shortcuts import render

# for class based views instead of login_required decorator we have the LoginRequiredMixin. See how it's passed in PostCreateView view
# to make sure that only the logged in user can update their content and not other's content we use UserPassesTestMixin
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin

from django.views.generic import (ListView, 
        DetailView,
        CreateView,
        UpdateView,
        DeleteView,
)
from .models import Post

# FBV
def home(request):
    context = {
        'posts': Post.objects.all(),
    }
    return render(request, 'blog/home.html', context)

# CBV
class PostListView(ListView):
    model = Post
    template_name = "blog/home.html"
    '''
    Do not forget to define context_object_name, otherwise you'll have to call it as 
    (Django's default) object_list in your respective template and you do not want 
    that. Assign it more specific name like posts and then loop thorugh it
    '''
    context_object_name = "posts" 
    ordering = ['-date_posted']

'''
For the class PostDetailView we have not defined a context_object_name. Thus we will 
be using variables in our template as, like, object.author instead for post.author
like in home.html. Take a look at post_detail.html in templates
'''
class PostDetailView(DetailView):
    model = Post                  

class PostCreateView(LoginRequiredMixin, CreateView): 
    model = Post 
    fields = ['title', 'content'] 

    def form_valid(self, form):               # we are defining this because without this we'd get null error since django would not know the owner of the post
        form.instance.author = self.request.user
        return super().form_valid(form)       # this runs by default on CreateView but here we are making sure that is is run after our author is defined

class PostUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView): 
    model = Post 
    fields = ['title', 'content'] 

    def form_valid(self, form):               
        form.instance.author = self.request.user
        return super().form_valid(form)  

    def test_func(self):            # UserPassesTestMixin will run test_func function in order to see if our user passes certain test conditions
        post = self.get_object()    # We want to get the exact post we want to update. We can use UpdateView's get_object method

        if self.request.user == post.author:
            return True
        return False

class PostDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Post  
    success_url = "/"  # without this, our page would give "No URL to redirect to. Provide a success_url." error and would not delete the post. 

    def test_func(self):            
        post = self.get_object()    

        if self.request.user == post.author:
            return True
        return False


def about(request):
    return render(request, 'blog/about.html')