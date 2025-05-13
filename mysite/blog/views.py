from django.shortcuts import render, get_object_or_404
from django.http import Http404
from .models import Post
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.views.generic import ListView
from django.core.mail import send_mail
from .forms import EmailPostForm
from django.views.decorators.http import require_POST
from .forms import CommentForm
from django.views.generic import ListView
from django.views.generic import DetailView
from django.views.generic import TemplateView
from django.views.generic import FormView
from django.views.generic import CreateView
from django.views.generic import UpdateView
from django.views.generic import DeleteView
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.csrf import csrf_protect
from django.views.decorators.csrf import ensure_csrf_cookie
from django.views.decorators.csrf import requires_csrf_token
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.csrf import csrf_protect
from django.views.decorators.csrf import ensure_csrf_cookie
from django.views.decorators.csrf import requires_csrf_token
from django.views.decorators.csrf import csrf_exempt
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
    comments = post.comments.filter(active=True)
    form = CommentForm()
    return render(request, 'blog/post/detail.html', {'post': post, 
                                                     'form': form,
                                                     'comments': comments})
def post_share(request, post_id):
    post = get_object_or_404(Post, id=post_id, status=Post.Status.PUBLISHED)
    sent =  False
    if request.method == 'POST':
        form = EmailPostForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            post_url = request.build_absolute_uri(post.get_absolute_url())
            subject = f"{cd['name']} recommends you read {post.title}"
            message = f"Read {post.title} at {post_url} \n {cd['name']}\'s comments: {cd['comments']}"
            send_mail(subject, message, 'na060553@gmail.com', [cd['to']])
            sent = True
    else:
        form = EmailPostForm()
    return render(request, 'blog/post/share.html', {'post': post,
                                                     'form': form,
                                                     'sent': sent})
from django.views.decorators.http import require_http_methods

from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse

@require_http_methods(["GET", "POST"])
def post_comment(request, post_id):
    post = get_object_or_404(Post, id=post_id, status=Post.Status.PUBLISHED)
    comment = None

    if request.method == 'POST':
        form = CommentForm(data=request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.post = post
            comment.save()
            # إعادة التوجيه إلى صفحة البوست بعد حفظ التعليق
            return redirect(post.get_absolute_url())
    else:
        form = CommentForm()

    return render(request, 'blog/post/comment.html', {'post': post,
                                                      'form': form, 'comment': comment})
