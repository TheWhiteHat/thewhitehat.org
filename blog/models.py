from django.db import models
from django.contrib.auth.models import User

# an over-arching category for entries. one cat. per entry.
class Category(models.Model):
    name = models.SlugField()
    description = models.CharField(max_length=126)

# a more specific categorization for entries. multiple tags per entry.
class Tag(models.Model):
    name = models.SlugField()

# a blog entry
class Entry(models.Model):  
    headline = models.CharField(max_length=126)
    author = models.ForeignKey(User, db_index=True)
    slug = models.SlugField()
    tags = models.ManyToManyField(Tag, related_name="entries", db_index=True)
    category = models.ForeignKey(Category, related_name="entries", db_index=True)
    content = models.TextField()
    date_created = models.DateTimeField(auto_now_add=True)
    date_modifed = models.DateTimeField(auto_now=True)
    enable_comments = models.BooleanField(default=True)
