from django.contrib import admin
from forum.models import *

class AnswerInline(admin.StackedInline):
    model = Answer
    can_delete = True
    max_num = 10
    fk_name = 'question'

class QuestionAdmin(admin.ModelAdmin):
    list_display = ('question_text','author')
    inlines = [AnswerInline,]
    fieldsets = (
       (None, {'fields':(('question_text','body_markdown','author','upvotes','downvotes','tags','views'))}),
    )

admin.site.register(Question, QuestionAdmin)

