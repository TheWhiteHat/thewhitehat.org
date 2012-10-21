from django.db import models
from django.core.urlresolvers import reverse
from django.contrib.auth.models import User

# an over-arching category for entries. one cat. per entry.
class Category(models.Model):
    name = models.SlugField()
    description = models.CharField(max_length=126)

    def __unicode__(self):
        return self.name

    class Meta:
        verbose_name_plural = 'categories'

# a more specific categorization for entries. multiple tags per entry.
class Tag(models.Model):
    name = models.SlugField()

    def __unicode__(self):
        return self.name

# a blog entry
class Entry(models.Model):  
    headline = models.CharField(max_length=126)
    slug = models.SlugField()
    author = models.ForeignKey(User, db_index=True)
    category = models.ForeignKey(Category, related_name="entries", db_index=True)
    content = models.TextField()
    enable_comments = models.BooleanField(default=True)
    tags = models.ManyToManyField(Tag, related_name="entries", db_index=True)
    date_created = models.DateTimeField(auto_now_add=True)
    date_modified = models.DateTimeField(auto_now=True)

    def __unicode__(self):
        return self.headline

    def get_absolute_url(self):
        return reverse('entry_detail', args=(self.slug,))

    class Meta:
        verbose_name_plural = 'entries'

# a simple page, that is not a blog, like an 'about us',gallery, etc.
class Page(models.Model):
    headline = models.CharField(max_length=126)
    slug = models.SlugField()
    content = models.TextField()
    date_modified = models.DateTimeField(auto_now=True,auto_now_add=True)
    
