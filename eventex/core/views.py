from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404

# Create your views here.
from eventex.core.models import Speaker


def home(request):
    speakers = Speaker.objects.all()
    # speakers = [
    #     {'name': 'Grace Hopper', 'photo': 'http://hbn.link/hopper-pic'},
    #     {'name': 'Alan Turing', 'photo': 'http://hbn.link/turing-pic'}
    # ]
    return render(request, 'index.html', {'speakers': speakers})


def speaker_detail(request, slug):
    speaker = get_object_or_404(Speaker, slug=slug)
    # speaker = Speaker.objects.get(slug=slug)
    return render(request, 'core/speaker_detail.html', {'speaker': speaker})
