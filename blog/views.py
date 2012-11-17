from django.shortcuts import render
from blog.models import Entry, Tag, Category


# the top 5 blog posts in order from newest to oldest
def index(request, page=1):
    entries = Entry.objects.order_by('-date_created').select_related()[:5]

    return render(request, 'blog/index.html', {
        'entries': entries,
        'categories': Category.objects.all(),
        'tags': Tag.objects.all()}
        )


# view the detail(s) of single entry
def entry_detail(request, slug):
    entry = Entry.objects.select_related().get(slug=slug)

    return render(request, 'blog/entry_detail.html', {'entry': entry})


# view a list of all entries in time order potentially filtered by
# author, tag, or category
def entry_list(request, **kwargs):
    entries = Entry.objects.order_by('-date_created').only('headline', 'date_created', 'slug')
    if 'author' in kwargs:
        entries = entries.filter(author__username=kwargs['author'])
        title = kwargs['author']
        limitby = 'by ' + kwargs['author']
    elif 'category' in kwargs:
        entries = entries.filter(category__name=kwargs['category'])
        title = kwargs['category'] + ' category'
        limitby = 'in the category ' + kwargs['category']
    elif 'tag' in kwargs:
        entries = entries.filter(tags__name=kwargs['tag'])
        title = kwargs['tag'] + ' tagged'
        limitby = 'tagged ' + kwargs['tag']
    else:
        title = 'Archive'
        limitby = None

    # user entry_list2.html for verybueno's listing technique.
    return render(request, 'blog/entry_list.html', {
        'entries': entries,
        'title': title,
        'limitby': limitby}
        )
