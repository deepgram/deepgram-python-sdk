from django.shortcuts import render

def index(request):
    return render(request, 'transcript/index.html')