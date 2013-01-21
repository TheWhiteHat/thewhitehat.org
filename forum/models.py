from django.db import models
from django.core.urlresolvers import reverse
from blog.models import Category, Tag
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes import generic
from django.template.defaultfilters import slugify
from whauth.models import User
import datetime

class Vote(models.Model):
    DIRECTIONS = (('up','Up'),('down','Down'))
    direction = models.CharField(max_length=4,choices=DIRECTIONS)
    content_type = models.ForeignKey(ContentType)
    object_id = models.PositiveIntegerField()
    content_object = generic.GenericForeignKey('content_type','object_id')
    user = models.ForeignKey(User)

class Votable(models.Model):
    upvotes = models.IntegerField(default=0)
    downvotes = models.IntegerField(default=0)
    votes = generic.GenericRelation(Vote,null=True)
    abstract = True

    def vote(self, direction, user):
        if direction == 'up':
            self.upvotes+=1
        elif direction == 'down':
            self.downvotes+=1
        self.save()
        vote = Vote(direction=direction,content_object=self,user=user)
        vote.save()

class Question(Votable):
    question_text = models.CharField(max_length=126)
    slug = models.SlugField(unique=True)
    body = models.TextField()
    author = models.ForeignKey(User)
    date_posted = models.DateTimeField(auto_now_add=True)
    lasted_edited = models.DateTimeField(auto_now=True)
    category = models.ForeignKey(Category)
    tags = models.ManyToManyField(Tag)
    views = models.IntegerField()

    def __unicode__(self):
        return self.slug

    def get_absolute_url(self):
        return reverse('question_detail', args=(self.slug,))

    def save(self, *args, **kwargs):
        if not self.id:
            now = datetime.datetime.now()
            self.slug = slugify(self.question_text)[0:37]+now.strftime("%m%d%Y%M%S")
        super(Question, self).save(*args, **kwargs)


class Answer(Votable):
    question = models.ForeignKey(Question)
    body = models.TextField()
    author = models.ForeignKey(User)
    date_posted = models.DateTimeField(auto_now_add=True)
    lasted_edited = models.DateTimeField(auto_now=True)

class AnswerComment(models.Model):
    answer = models.ForeignKey(Answer)
    body = models.CharField(max_length=126)
    author = models.ForeignKey(User)
    date_posted = models.DateTimeField(auto_now_add=True)
    lasted_edited = models.DateTimeField(auto_now=True)

    def __unicode__(self):
        return self.author.username + " to " + self.answer.question.id
