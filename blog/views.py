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
    entries = Entry.objects.order_by('-date_created')

    ## Sort the entries into groups by month. Probably a better way to
    ## do this

    final = []
    temp = []
    curr = entries[0].date_created.month

    for q in entries:
        d = q.date_created.month
        if d < curr:
            curr = d
            final.append(temp)
            temp = []
        temp.append(q)

    final.append(temp)

    return render_to_response('blog/entry_list.html', {'entries':final, 'list_title':'Every Entry'})
