from django.db import models
from django.contrib.auth.models import (AbstractBaseUser, BaseUserManager)
from django.conf import settings

#error raised when login error
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
        (BANNED, 'banned'),
        (INACTIVE, 'inactive'),
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


