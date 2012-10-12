from django.views.generic.base import *
from django.views.generic.detail import *
from django.views.generic.list import *

class AwareResponseMixin(TemplateResponseMixin):
    def get_template_names(self):
        names = super(AwareResponseMixin,self).get_template_names()
        format = self.kwargs.get('format','html')
        if format != 'html':
            names = [n[:-4]+format for n in names]
        return names

    def render_to_response(self,context):
        response = super(AwareResponseMixin,self).render_to_response(context)
        format = self.kwargs.get('format','html')
        if format != 'html':
            response['content-type'] = 'application/' + format
        return response

class AwareDetailView(AwareResponseMixin,DetailView):
    """Renders a content-aware view of an object, depending on the "format" parameter in the
    view's kwargs"""

class AwareListView(AwareResponseMixin,ListView):
    """Renders a content-aware view of a list of objects, depending on the "format" parameter
    in the view's kwargs"""
