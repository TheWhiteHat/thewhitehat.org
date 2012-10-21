from django.http import HttpResponse
from django.shortcuts import render_to_response
from django.template import RequestContext
from blog.models import Entry
from datetime import datetime

# all of the blog posts in order
def index(request, page=1):
    return ''

# view the detail(s) of single entry
def entry_detail(request, slug):
    entry = Entry.objects.get(slug=slug)
    
    return render_to_response('blog/entry_detail.html', {'entry':entry})

# view a list of all entries in time order potentially filtered by
# author, tag, or category
def entry_list(request):
    entries = Entry.objects.all()

    return render_to_response('blog/entry_list.html', {'entries':entries, 'list_title':'Every Entry'})
