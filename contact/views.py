from django.http import HttpResponseRedirect
from contact.models import *
from django.shortcuts import render
from django.core.urlresolvers import reverse

def contact(request):
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            # send mail lol
            return HttpResponseRedirect(reverse('contact_success'))  # Redirect after POST
    else:
        form = ContactForm()  # An unbound form

    return render(request, 'contact/contact.html', {'form': form})
