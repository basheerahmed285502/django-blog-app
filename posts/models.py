from django.db import models
from django.contrib.auth.models import User

# Create your models here.


class Tag(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name


class Post(models.Model):
    title = models.CharField(max_length=60)
    content = models.TextField()
    published_date = models.DateTimeField(auto_now_add=True)
    tags = models.ManyToManyField(Tag, related_name="posts")
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="posts")
    post_image = models.ImageField(
        upload_to="post_images", blank=True, null=True)

    def __str__(self):
        return self.title


class Comment(models.Model):
    comment = models.TextField()
    post = models.ForeignKey(
        Post, on_delete=models.CASCADE, related_name="comments")
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="comments")

    def __str__(self):
        return f"Comment by {self.user.username} on {self.post.title}"
