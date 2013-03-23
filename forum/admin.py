from django.contrib import admin
from forum.models import *


class AnswerInline(admin.StackedInline):
    model = Answer
    can_delete = True
    max_num = 10
    fk_name = 'question'

class ReplyInline(admin.StackedInline):
    model = Post
    can_delete = True
    max_num = 10

class QuestionAdmin(admin.ModelAdmin):
    list_display = ('question_text', 'author')
    inlines = [AnswerInline, ]
    fieldsets = (
       (None, {'fields':(('question_text','body_markdown',
            'author','upvotes','downvotes','tags','views')
            )}),
    )

admin.site.register(Question, QuestionAdmin)

class DiscussionAdmin(admin.ModelAdmin):
    list_display = ('subject','author','date_created')
    inlines = [ReplyInline,]
    prepopulated_fields = {'slug': ('subject',)}

admin.site.register(Thread, DiscussionAdmin)

class BoardAdmin(admin.ModelAdmin):
    list_display = ('name','slug','date_created')
    prepopulated_fields = {'slug': ('name',)}

admin.site.register(DiscussionBoard, BoardAdmin)
