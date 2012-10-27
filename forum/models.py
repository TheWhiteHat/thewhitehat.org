from django.db import models
from django.core.urlresolvers import reverse
from blog.models import Category,Tag
from django.contrib.auth.models import User

class Question(models.Model):
    question = models.CharField(max_length=126)
    slug = models.SlugField(unique=True)
    body = models.TextField()
    author = models.ForeignKey(User)
    date_posted = models.DateTimeField(auto_now_add = True)
    lasted_edited = models.DateTimeField(auto_now = True)
    category = models.ForeignKey(Category)
    tags = models.ManyToManyField(Tag)
    upvotes = models.IntegerField()
    downvotes = models.IntegerField()
    views = models.IntegerField()
    
    def __unicode__(self):
        return self.slug

    def get_absolute_url(self):
        return reverse('question_detail',args=(self.slug,)) 
    
    
class Answer(models.Model):
    question = models.ForeignKey(Question)
    body = models.TextField()
    author = models.ForeignKey(User)
    date_posted = models.DateTimeField(auto_now_add = True)
    lasted_edited = models.DateTimeField(auto_now = True)
    upvotes = models.IntegerField()
    downvotes = models.IntegerField()

    def __unicode__(self):
        return self.author.first_name + " " + self.question.slug

class AnswerComment(models.Model):
    answer = models.ForeignKey(Answer)
    body = models.CharField(max_length=126)
    author = models.ForeignKey(User)
    date_posted = models.DateTimeField(auto_now_add = True)
    lasted_edited = models.DateTimeField(auto_now = True)
