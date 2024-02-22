from django.shortcuts import render, redirect
from website.forms import ContactForm, NewsletterForm
from django.contrib import messages
from django.http import HttpResponseRedirect



def index_view(request):
    return render(request, 'website/index.html')


def about_view(request):
    return render(request, 'website/about.html')


def contact_view(request):
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            name = form.save(commit=False)
            name.name = 'unknown'
            name.save()
            messages.success(request, 'your ticket submited successfully')
        else:
            messages.error(request, 'your ticket didnt submited')
        
    form = ContactForm()
    return render(request, 'website/contact.html', {'form':form})

def about_view(request):
    return render(request, 'website/about.html')


def newsletter_view(request):
    if request.method == 'POST':
        form = NewsletterForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'your newsletter submited successfully')
            return HttpResponseRedirect('/')
        else:
            messages.error(request, 'your newsletter didnt submited')
            return HttpResponseRedirect('/')