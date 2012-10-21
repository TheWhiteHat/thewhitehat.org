from django.http import HttpResponse
from django.shortcuts import render_to_response
from django.template import RequestContext
from blog.models import Entry
from datetime import datetime

# the top 5 blog posts in order from newest to oldest
def index(request, page=1):
    entries = Entry.objects.order_by('date_created')[::-1]

    return render_to_response('blog/index.html', {'entries':entries[:5]})

# view the detail(s) of single entry
def entry_detail(request, slug):
    entry = Entry.objects.get(slug=slug)
    
    return render_to_response('blog/entry_detail.html', {'entry':entry})

# view a list of all entries in time order potentially filtered by
# author, tag, or category
def entry_list(request):
    entries = Entry.objects.order_by('-date_created')
    
    # user entry_list2.html for verybueno's listing technique.
    return render_to_response('blog/entry_list.html', {'entries':entries, 'list_title':'Every Entry'})

