# Create your views here.

from django.shortcuts import render_to_response
from django.template.context import RequestContext

def test(request):
    return render_to_response('test.html', {}, context_instance=RequestContext(request))