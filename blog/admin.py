from django.contrib import admin

from blog import models

class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'description')
admin.site.register(models.Category, CategoryAdmin)

class TagAdmin(admin.ModelAdmin):
    list_display = ('name',)
admin.site.register(models.Tag, TagAdmin)

class EntryAdmin(admin.ModelAdmin):
    list_display = ('headline', 'author', 'category', 'date_created')
    prepopulated_fields = {'slug': ('headline',)}
    filter_horizontal = ('tags',)
admin.site.register(models.Entry, EntryAdmin)
