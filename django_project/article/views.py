from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.views.generic import ListView, DetailView, FormView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.views.generic.detail import SingleObjectMixin
from .models import Article
from django.urls import reverse_lazy, reverse
from .forms import CommentForm
# Create your views here.

class ArticleListView(ListView):
    model = Article
    template_name = "article_list.html"

# MANAGE DETAIL VIEW WITH COMMENTS
class CommentGet(DetailView):
    model = Article
    template_name = "article_detail.html"
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = CommentForm()
        return context

class CommentPost(SingleObjectMixin, FormView):
    model = Article
    form_class = CommentForm
    template_name = "article_detail.html"
    
    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        return super().post(request, *args, **kwargs)
    
    def form_valid(self, form):
        user = self.request.user
        comment = form.save(commit=False)
        comment.article = self.object
        comment.author = user
        comment.save()
        return super().form_valid(form)
    
    def get_success_url(self):
        article = self.get_object()
        return reverse("article_detail", kwargs={"slug": article.slug})

class ArticleDetailView(LoginRequiredMixin, DetailView):
    def get(self, request, *args, **kwargs):
        view = CommentGet.as_view()
        return view(request, *args, **kwargs)
    
    def post(self, request, *args, **kwargs):
        view = CommentPost.as_view()
        return view(request, *args, **kwargs)
# MANAGE DETAIL VIEW WITH COMMENTS


class ArticleUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Article
    fields = ("title", "body")
    template_name = "article_update.html"
    
    def test_func(self):
        return self.get_object().author == self.request.user

class ArticleDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Article
    template_name = "article_delete.html"
    success_url = reverse_lazy("home")
    
    def test_func(self):
        return self.get_object().author == self.request.user
    
class ArticleCreateView(LoginRequiredMixin ,CreateView):
    model = Article
    template_name = "article_create.html"
    fields = ("title", "body")
    success_url = reverse_lazy("home")
    
    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)