"""Class-based views of the public website pages."""

from django.contrib import messages
from django.http import HttpResponseRedirect
from django.urls import reverse_lazy
from django.views.generic import CreateView, TemplateView

from website.forms import ContactForm, NewsletterForm
from website.models import Contact, Newsletter


class IndexView(TemplateView):
    """Landing page."""

    template_name = 'website/index.html'


class AboutView(TemplateView):
    """Static "about us" page."""

    template_name = 'website/about.html'


class ContactView(CreateView):
    """Store a contact ticket, then reload the page with a flash message."""

    model = Contact
    form_class = ContactForm
    template_name = 'website/contact.html'
    # Redirect after a successful POST so a refresh cannot resend the ticket.
    success_url = reverse_lazy('website:contact')

    def form_valid(self, form):
        messages.success(self.request, 'Your ticket was submitted '
                                       'successfully.')
        return super().form_valid(form)

    def form_invalid(self, form):
        messages.error(self.request, 'Your ticket could not be submitted.')
        return super().form_invalid(form)


class NewsletterSubscribeView(CreateView):
    """Footer subscription form: POST only, always back to the home page."""

    model = Newsletter
    form_class = NewsletterForm
    http_method_names = ['post']
    success_url = reverse_lazy('website:index')

    def form_valid(self, form):
        messages.success(self.request, 'Your newsletter subscription was '
                                       'submitted successfully.')
        return super().form_valid(form)

    def form_invalid(self, form):
        messages.error(self.request, 'Your newsletter subscription could not '
                                     'be submitted.')
        # The form lives in the footer of every page, so there is no template
        # of its own to render the errors into. ``success_url`` is used
        # directly because ``get_success_url()`` needs a saved object.
        return HttpResponseRedirect(self.success_url)

