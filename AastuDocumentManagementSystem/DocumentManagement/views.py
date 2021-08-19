from django.shortcuts import render

from .forms import SignInForm
from .models import User


# Create your views here.
def signIn(request):
    form = SignInForm()
    if request.method == "POST":
        form = SignInForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            print(User.objects.all())

    return render(request, 'SignIn.html', {
        'form': form
    })
