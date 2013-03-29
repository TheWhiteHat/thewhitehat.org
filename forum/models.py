from django.db import models
from django.core.urlresolvers import reverse
from blog.models import Tag
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes import generic
from django.template.defaultfilters import slugify
from whauth.models import User
import datetime
from django import forms
from forum.utils import render_markdown
from django.conf import settings
from mptt.models import MPTTModel, TreeForeignKey

class Vote(models.Model):
    """An vote in a direction, on any object"""
    DIRECTIONS = (('up', 'Up'), ('down', 'Down'))
    direction = models.CharField(max_length=4, choices=DIRECTIONS)
    content_type = models.ForeignKey(ContentType)
    object_id = models.PositiveIntegerField()
    content_object = generic.GenericForeignKey('content_type', 'object_id')
    user = models.ForeignKey(User)


class Votable(models.Model):
    """An object that can have votes given to it"""
    upvotes = models.IntegerField(default=0)
    downvotes = models.IntegerField(default=0)
    votes = generic.GenericRelation(Vote, null=True)
    abstract = True

    def vote(self, direction, user):
        if direction == 'up':
            self.upvotes += 1
        elif direction == 'down':
            self.downvotes += 1
        self.save()
        vote = Vote(direction=direction, content_object=self, user=user)
        vote.save()


class Question(Votable):
    question_text = models.CharField(max_length=126)
    slug = models.SlugField(unique=True)
    body_html = models.TextField(blank=True)
    body_markdown = models.TextField()
    author = models.ForeignKey(User)
    date_posted = models.DateTimeField(auto_now_add=True)
    lasted_edited = models.DateTimeField(auto_now=True)
    # category = models.ForeignKey(Category)
    tags = models.ManyToManyField(Tag)
    views = models.IntegerField(default=0)
    answers_count = models.IntegerField(default=0)

    def __unicode__(self):
        return self.slug

    def get_absolute_url(self):
        return reverse('question_detail', args=(self.slug,))

    def save(self, *args, **kwargs):
        if not self.id:
            now = datetime.datetime.now()
            self.slug = slugify(
                self.question_text)[0:37] + now.strftime("%m%d%Y%M%S")

        self.body_html = render_markdown(self.body_markdown)
        super(Question, self).save(*args, **kwargs)


class Answer(Votable):
    question = models.ForeignKey(Question)
    body_markdown = models.TextField()
    body_html = models.TextField()
    author = models.ForeignKey(User)
    date_posted = models.DateTimeField(auto_now_add=True)
    lasted_edited = models.DateTimeField(auto_now=True)

    def __init__(self, *args, **kwargs):
        # create a reference for detecting if markdown was changed.
        # that way we don't have to re-render upon save after vote.
        super(Answer, self).__init__(*args, **kwargs)
        self._old_body_md = self.body_markdown

    def save(self, *args, **kwargs):
        if not self.id:
            self.question.answers_count += 1
            self.question.save()

        if self._old_body_md != self.body_markdown:
            self.body_html = render_markdown(self.body_markdown)

        super(Answer, self).save(*args, **kwargs)

    def delete(self, *args, **kwargs):
        self.question.answers_count -= 1
        self.question.save()

        super(Answer, self).delete(*args, **kwargs)


class AnswerComment(models.Model):
    """A comment on an answer to a question"""
    answer = models.ForeignKey(Answer)
    body = models.CharField(max_length=126)
    author = models.ForeignKey(User)
    date_posted = models.DateTimeField(auto_now_add=True)
    lasted_edited = models.DateTimeField(auto_now=True)

    def __unicode__(self):
        return self.author.username + " to " + self.answer.question.id


class SubmitAnswerForm(forms.Form):
    """A form to submit an answer to a question"""
    answer_body = forms.CharField(widget=forms.Textarea)
    qid = forms.IntegerField()


class NewQuestionForm(forms.Form):
    """A form for posting a new question to the questions site"""
    question_text = forms.CharField(label="Question",
                                    initial="Be clear and concise..."
                                   )
    body_text = forms.CharField(widget=forms.Textarea, label="Details")
    tagslist = forms.CharField(label="Tags")


class EditForm(forms.Form):
    """A form for handling edits to a question or answer, etc."""
    body_markdown = forms.CharField(widget=forms.Textarea)
    objid = forms.IntegerField()
    objtype = forms.CharField()


class Board(models.Model):
    """A board with a specific category of topics"""
    name = models.CharField(max_length=26)
    slug = models.SlugField()
    description = models.CharField(max_length=100)
    date_created = models.DateTimeField(auto_now_add=True)

    def __unicode__(self):
        return self.name

    def get_absolute_url(self):
        return reverse("thread_list",args=(self.slug,1))


class ThreadIcon(models.Model):
    """An icon for a discussion, might be useful for labelling
    moods of a thread"""
    name = models.CharField(max_length=26)
    icon = models.CharField(max_length=100,
            default="/static/img/thread-icons/")

    def __unicode__(self):
        return self.name


class Thread(models.Model):
    """A discussion thread"""
    subject = models.CharField(max_length=300)
    board = models.ForeignKey(Board)
    slug = models.SlugField()
    author = models.ForeignKey(User)
    date_created = models.DateTimeField(auto_now=True)
    posts_count = models.IntegerField(default=0)
    views_count = models.IntegerField(default=0)
    date_posted = models.DateTimeField(auto_now=True)
    is_sticky = models.BooleanField(default=False)
    icon = models.ForeignKey(ThreadIcon, blank=True, null=True)

    def __unicode__(self):
        return self.subject

    def get_absolute_url(self):
        return reverse('thread_detail', args=(self.slug,1,))

    def save(self, *args, **kwargs):
        if not self.id:
            now = datetime.datetime.now()
            self.slug = slugify(
                self.subject)[0:37] + now.strftime("%m%d%Y%M%S")

        super(Thread, self).save(*args, **kwargs)



class Post(MPTTModel,Votable):
    """A post in a  discussion thread. Tree structured."""
    thread = models.ForeignKey(Thread)
    author = models.ForeignKey(User)
    date_posted = models.DateTimeField(auto_now=True)
    date_edited = models.DateTimeField(auto_now=True)
    body_markdown = models.TextField()
    body_html = models.TextField(blank=True)

    #for tree organization, don't modify
    parent = TreeForeignKey('self', null=True, blank=True, related_name='children')

    def __init__(self, *args, **kwargs):
        # create a reference for detecting if markdown was changed.
        # that way we don't have to re-render upon save after vote.
        super(Post, self).__init__(*args, **kwargs)
        self._old_body_md = self.body_markdown

    def __unicode__(self):
        return "Post "+str(self.id)+" by "+self.author.username+" in  "+self.thread.subject

    def get_absolute_url(self):
        return reverse('post_detail', args=(self.id,))

    def save(self, *args, **kwargs):
        # TODO: how to inherit both votable and a markdowned save()?
        if not self.id:
            self.thread.posts_count += 1
            self.thread.save()

        if self._old_body_md != self.body_markdown:
            self.body_html = render_markdown(self.body_markdown)

        super(Post, self).save(*args, **kwargs)

    def delete(self, *args, **kwargs):
        self.thread.posts_count -= 1
        self.thread.save()

        super(Post, self).delete(*args, **kwargs)


class BoardField(forms.CharField):
    """A field to make sure that the board exists."""
    def clean(self,value):
        super(BoardField,self).clean(value)
        try:
            Board.objects.get(id=value)
            return value
        except Board.DoesNotExist:
            raise forms.ValidationError("Invalid Board Id.")

class IconField(forms.IntegerField):
    """A field to make sure that the icon exists."""
    def clean(self,value):
        super(IconField,self).clean(value)
        if value == 0:
            return None
        try:
            ThreadIcon.objects.get(id=value)
            return value
        except ThreadIcon.DoesNotExist:
            raise forms.ValidationError("Invalid Icon Id.")

class NewThreadForm(forms.Form):
    """A form for posting a new thread to board """
    thread_subject = forms.CharField(label="Subject",
                                    initial="Be clear and concise..."
                                   )
    body_text = forms.CharField(widget=forms.Textarea, label="Details")
    board_id = BoardField(widget=forms.HiddenInput)
    thread_icon = IconField()



class PostField(forms.IntegerField):
    """A field to make sure that a post exists"""
    def clean(self,value):
        super(PostField,self).clean(value)
        try:
            Post.objects.get(id=value)
            return value
        except Post.DoesNotExist:
            raise forms.ValidationError("Invalid post id.")


class NewPostForm(forms.Form):
    """A form for replying to a or post."""
    body_text = forms.CharField(widget=forms.Textarea)
    reply_to = PostField(widget=forms.HiddenInput)
