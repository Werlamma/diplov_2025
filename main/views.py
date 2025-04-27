from django.views.generic import TemplateView


class HomePageView(TemplateView):
    template_name = 'main/index.html'


class AboutPageView(TemplateView):
    template_name = 'main/about.html'


class ContactsPageView(TemplateView):
    template_name = 'main/contact.html'


class PartnersPageView(TemplateView):
    template_name = 'main/partners.html'


class PolicyPageView(TemplateView):
    template_name = 'main/policy.html'


