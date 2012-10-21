from django.http import HttpResponse, Http404,HttpResponseRedirect
from django.core.context_processors import csrf
from django.shortcuts import render_to_response
from django.template import RequestContext
from contact.models import *

from django.core.urlresolvers import reverse

def contact(request):
  if request.method == 'POST':
    form = ContactForm(request.POST)
    if form.is_valid():
        # send mail lol
      return HttpResponseRedirect(reverse('contact_success')) # Redirect after POST
  else:
    form = ContactForm() # An unbound form

  return render_to_response('contact/contact.html', {'form':form},context_instance=RequestContext(request))

