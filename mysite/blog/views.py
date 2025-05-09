from django.shortcuts import render, get_object_or_404
from django.http import Http404
from .models import Post
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.views.generic import ListView

#
class PostListView(ListView):
    model = Post
    template_name = 'blog/post/list.html'
    context_object_name = 'posts'
    paginate_by = 1

    def get_queryset(self):
        return Post.objects.filter(status=Post.Status.PUBLISHED).order_by('-publish')

def post_detail(request,year, month, day, post):

    post = get_object_or_404(Post, status=Post.Status.PUBLISHED,
                            slug=post,
                            publish__year=year,
                            publish__month=month,
                            publish__day=day
                            )
    return render(request, 'blog/post/detail.html', {'post': post})