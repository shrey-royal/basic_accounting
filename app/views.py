from django.shortcuts import render,redirect
from .models import Homepage
# Import the PartyForm
from django.contrib.auth.decorators import login_required



@login_required
def index(request):
    context = {
        'username': request.user.username,
    }
    return render(request, 'index.html', context)


def main(request):
    home = Homepage.objects.all()
    return render(request, 'main.html')
