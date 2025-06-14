from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from django.urls import reverse
from taggit.managers import TaggableManager

class Post(models.Model):

    class Status(models.TextChoices):
        DRAFT = 'draft', 'Draft'
        PUBLISHED = 'published', 'Published'
    title = models.CharField(max_length=200)
    content = models.TextField()
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='blog_posts')
    publish = models.DateTimeField(default=timezone.now)
    status = models.CharField(max_length=10, choices=Status.choices, default=Status.DRAFT)
    slug = models.SlugField(max_length=200, unique=True, unique_for_date='publish')
    body = models.TextField()
    tags = TaggableManager()   
    class Meta:
        ordering = ['-publish']
        indexes = [
            models.Index(fields=['-publish']),
        ]
    def __str__(self):
        return self.title
    def get_absolute_url(self):
        return reverse('blog:post_detail', args=[
            self.publish.year,
            self.publish.month,
            self.publish.day,
            self.slug,
        ])
class Comment(models.Model):
        post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comments')
        name = models.CharField(max_length=80)
        email = models.EmailField()
        body = models.TextField()
        created = models.DateTimeField(auto_now_add=True)
        updated = models.DateTimeField(auto_now=True)
        active = models.BooleanField(default=True)
    
        class Meta:
            ordering = ['created']
            indexes = [
                models.Index(fields=['created']),
            ]
        def __str__(self):
            return f'Comment by {self.name} on {self.post}'