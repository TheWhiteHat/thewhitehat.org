from django.http import HttpResponse
from django.shortcuts import render_to_response
from django.template import RequestContext
from blog.models import Entry
from datetime import datetime

def index(request, page=1):
    return ''

# view a single entry
def entry_detail(request, slug):
    entry = Entry.objects.get(slug=slug)
    entry.date = entry.date_modified
    
    return render_to_response('blog/entry.html', {'entry':entry})

# view a list of all entries in time order potentially filtered by
# author, tag, or category
def entry_list(request):
    return ''
