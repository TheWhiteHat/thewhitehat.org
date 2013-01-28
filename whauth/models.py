from django.db import models
from django.contrib.auth.models import (AbstractBaseUser, BaseUserManager)
from django.conf import settings
from django import forms
from whauth.backends import AuthBackend
import re

class UserManager(BaseUserManager):
    def create_user(self, username, password=None, **other_fields):
        if not username:
            raise ValueError('username required')

        try:
            fbid = other_fields['fbid']
        except KeyError:
            fbid = None

        if not password and not fbid:
            raise ValueError('either a password or facebook id required')

        user = self.model(username=username)
        if password:
            user.set_password(password)

        if fbid:
            # verify
            user.fbid = fbid

        try: user.role = other_fields['role']
        except KeyError: pass

        try: user.email = other_fields['email']
        except KeyError: pass

        user.save(using=self._db)
        return user

    def create_superuser(self, username, password, **other_fields):
        other_fields['role'] = User.ADMIN
        return self.create_user(username,  password, **other_fields)

class User(AbstractBaseUser):
    objects = UserManager()

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = []

    BANNED = -1
    INACTIVE = 0
    NORMAL = 1
    WRITER = 2
    MOD = 3
    ADMIN = 4

    ROLE_CHOICES = (
        (BANNED, 'banned'), (INACTIVE, 'inactive'),
        (NORMAL, 'normal'),
        (WRITER, 'writer'),
        (MOD, 'moderator'),
        (ADMIN, 'admin'),
    )

    username = models.CharField(max_length=42, unique=True, db_index=True)
    fbid = models.CharField(max_length=126, blank=True, db_index=True)
    email = models.EmailField(blank=True)
    role = models.SmallIntegerField(choices=ROLE_CHOICES, default=NORMAL)
    use_gravatar = models.BooleanField(default=False)

    def get_full_name(self):
        return self.username

    def get_short_name(self):
        return self.username

    def __unicode__(self):
        return self.username

    @property
    def is_active(self):
        return self.role > 0

    @property
    def is_staff(self):
        return self.role > self.NORMAL

    @property
    def is_admin(self):
        return self.role == self.ADMIN

    def has_perm(self, perm, obj=None):
        return self.is_staff # todo change this to limit perms for writers and mods

    def has_module_perms(self, mod):
        return self.is_staff # also change like ^

    # forum-specific functions:

    class CannotVote(Exception):
        pass

    class AlreadyVoted(Exception):
        pass
    
    # vote on an a given object.    
    def vote_on_object(self,obj,direction):
        from forum.models import Vote
        try:
            vote = obj.votes.get(user=self) 
            if vote.direction == direction:
                raise self.AlreadyVoted()
            else:
                vote.direction = direction
                vote.save()
                if direction == 'up':
                    obj.downvotes-=1
                    obj.upvotes+=1
                else:
                    obj.upvotes-=1
                    obj.downvotes+=1
                obj.save()
        except AttributeError:
            raise self.CannotVote()

        except Vote.DoesNotExist:
            vote = Vote(direction=direction,content_object=obj,user=self) 
            vote.save() 
            if direction == 'up':
                obj.upvotes+=1
            else:
                obj.downvotes+=1
            obj.save()
    # end forum-specifc functions

class UsernameField(forms.CharField):
    def clean(self,value):
        super(UsernameField,self).clean(value)
        try:
            User.objects.get(username=value)
            raise forms.ValidationError("Username in use. Please choose another.")
        except User.DoesNotExist:
            return value

class NewUserForm(forms.Form):
    username = UsernameField(max_length=50)
    password = forms.CharField(widget=forms.PasswordInput,min_length=5)
    password_confirm = forms.CharField(widget=forms.PasswordInput,min_length=5)
    email = forms.EmailField()
    email_confirm = forms.EmailField()

    def clean_email(self):
        if self.data['email'] != self.data['email_confirm']:
                raise forms.ValidationError("Emails don't match.")
        return self.data['email']

    def clean_password(self):
        if self.data['password'] != self.data['password_confirm']:
            raise forms.ValidationError("Passwords don't match.")
        if not re.compile('^[a-zA-Z]\w{5,25}$').match(self.data['password']):
            raise forms.ValidationError("Invalid password. Be more secure.")
        return self.data['password']
                                   
    def clean(self,*args, **kwargs):
        self.clean_email()
        self.clean_password()
        return super(NewUserForm, self).clean(*args, **kwargs)

class FBTokenField(forms.CharField):
    def clean(self,value):
        super(FBTokenField,self).clean(value)
        auth = AuthBackend()
        fbid = auth.get_fbid(value)
        if fbid is None:
            raise forms.ValidationError("Invalid token: "+value)
        else:
            try:
                User.objects.get(fbid=fbid)
                raise forms.ValidationError("Fb id already registered")
            except User.DoesNotExist:
                return fbid
    
class NewFBUserForm(forms.Form):
    fbtoken = FBTokenField()
    username = UsernameField()
