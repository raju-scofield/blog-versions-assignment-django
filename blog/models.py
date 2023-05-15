from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class BlogPost(models.Model):
    blog_id = models.BigAutoField(primary_key=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=300)
    description = models.TextField()
    body_text = models.TextField()
    creation_date = models.DateTimeField(auto_now_add=True)
    update_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title


class Comment(models.Model):
    comment_id = models.BigAutoField(primary_key=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    author_email = models.EmailField()
    comment_text = models.TextField()
    creation_date = models.DateTimeField(auto_now_add=True)
    post_id = models.ForeignKey(BlogPost, on_delete=models.CASCADE)
    parent_comment_id = models.ForeignKey('self', on_delete=models.CASCADE, null=True, blank=True, related_name='replies')

    def __str__(self):
        return self.comment_text

class BlogVersions(models.Model):
    blog_version_id = models.BigAutoField(primary_key=True)
    blog_id = models.ForeignKey(BlogPost, on_delete=models.CASCADE)
    version = models.IntegerField()
    title = models.CharField(max_length=300)
    description = models.TextField()
    body_text = models.TextField()
    modified_date = models.DateField(auto_now_add=True)

    def __str__(self):
        return str(self.blog_version_id)
