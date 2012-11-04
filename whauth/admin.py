from django import forms
from django.contrib import admin
from django.contrib.auth.models import Group
from django.contrib.auth.admin import UserAdmin as DjangoUserAdmin
from django.contrib.auth.forms import ReadOnlyPasswordHashField

from whauth.models import User

class UserCreationForm(forms.ModelForm):
    password1 = forms.CharField(label='Password', widget=forms.PasswordInput)
    password2 = forms.CharField(label='Password Confirmation', widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ('username',)

    def clean_password2(self):
        password1 = self.cleaned_data.get('password1')
        password2 = self.cleaned_data.get('password2')
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError('Passwords do not match')
        return password2

    def save(self, commit=True):
        user = super(UserCreationForm, self).save(commit=False)
        user.set_password(self.cleaned_data['password1'])
        if commit:
            user.save()
        return user

class UserChangeForm(forms.ModelForm):
    password = ReadOnlyPasswordHashField()

    class Meta:
        model = User

class UserAdmin(DjangoUserAdmin):
    form = UserChangeForm
    add_form = UserCreationForm

    # username, fbid, email, role, use_gravatar
    list_display = ('username', 'fbid', 'email', 'role', 'use_gravatar')
    list_filter = ('role',)
    fieldsets = (
            (None, {
                'fields': ('email', 'password')
                }),
            ('Personal Info', {
                'classes': ('collapse',),
                'fields': ('role', 'use_gravatar')},)
            )
    #add_fieldsets = (
    #    (None, {
    #        'fields': ('email', 'password1', 'password2')}),
    #)
    search_fields = ('username',)
    ordering = ('role',)
    filter_horizontal = () 

admin.site.register(User, UserAdmin)
admin.site.unregister(Group)
