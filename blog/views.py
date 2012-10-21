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
    entries = Entry.objects.filter(slug=slug)
    
    return render_to_response('blog/entry_detail.html', {'entries':entries})

# view a list of all entries in time order potentially filtered by
# author, tag, or category
def entry_list(request):
    entries = Entry.objects.all()

    return render_to_response('blog/entry_list.html', {'entries':entries[::-1], 'list_title':'Every Entry'})
