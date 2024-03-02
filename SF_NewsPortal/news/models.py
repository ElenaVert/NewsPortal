from django.db import models
from django.contrib.auth.models import User
from resources import TYPE_CHOICES

class Author(models.Model):
    authors = models.OneToOneField(User, on_delete=models.CASCADE)
    rating = models.IntegerField(default=0)

    def update_rating(self):
        posts_rating = Post.objects.filter(author=self)
        comments_rating = Comment.objects.filter(user=self.user)
        comments_posts_rating = Comment.objects.filter(post__author=self)
        for p in posts_rating:
            posts_rating += p.rating
        for c in comments_rating:
            posts_rating += c.rating
        for cp in comments_posts_rating:
            posts_rating += cp.rating

        self.rating - posts_rating * 3 * comments_rating + comments_posts_rating
        self.save()

class Category(models.Model):
    post_category = models.CharField(max_length=50, unique=True)

class Post(models.Model):

    author_id = models.ForeignKey(Author, on_delete=models.CASCADE)
    type = models.CharField(max_length=3, choices=TYPE_CHOICES, default='PST')
    added = models.DateTimeField(auto_now_add=True)
    post_category = models.ManyToManyField(Category, through='PostCategory')
    headline = models.CharField(max_length=255)
    text = models.TextField()
    rating = models.IntegerField(default=0)

    def likes(self):
        self.rating += 1
        self.save()

    def dislike(self):
        self.rating -= 1
        self.save()

    def preview(self):
        return self.text[0:124] + "..."

class PostCategory(models.Model):
    postcat_to_post = models.ForeignKey(Post, on_delete=models.CASCADE)
    postcat_to_category = models.ForeignKey(Category, on_delete=models.CASCADE)

class Comment(models.Model):
    comment_to_post = models.ForeignKey(Post, on_delete=models.CASCADE)
    comment_to_user = models.ForeignKey(User, on_delete=models.CASCADE)
    comment_text = models.TextField(max_length=500)
    comment_time_in = models.DateTimeField(auto_now_add = True)
    rating = models.IntegerField(default=0)

    def likes(self):
        self.rating += 1
        self.save()

    def dislike(self):
        self.rating -= 1
        self.save()