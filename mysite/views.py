from django.views.generic import TemplateView

class Homepage(TemplateView):
    template_name = 'index.html'
    
class ThanksPage(TemplateView):
    template_name = 'thanks.html'