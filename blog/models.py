from django.db import models
from django.contrib.auth.models import User

# an over-arching category for entries. one cat. per entry.
class Category(models.Model):
    name = models.CharField(max_length=50)
    description = models.TextField()
    slug = models.SlugField(max_length=50)


# a more specific categorization for entries. multiple tags per entry.
class Tag(models.Model):
    name = models.CharField(max_length=50)


# an entry
class Entry(models.Model):  
    headline = models.CharField(max_length=100)
    content = models.TextField()
    date_posted = models.DateTimeField(auto_now=True)
    date_modifed = models.DateTimeField(auto_now=True)
    author = models.ForeignKey(User)
    comments_enabled = models.BooleanField(default=True)
    slug = models.SlugField(max_length=50)
    tags = models.ManyToManyField(Tag)
    category = models.ForeignKey(Category)
