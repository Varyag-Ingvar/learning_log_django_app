from django.shortcuts import render, redirect
from django.contrib.auth import login
from django.contrib.auth.forms import UserCreationForm


def register(request):
    """register a new user"""
    if request.method != 'POST':
        # return an empty form
        form = UserCreationForm
    else:
        # processing the completed form
        form = UserCreationForm(data=request.POST)

        if form.is_valid():
            new_user = form.save()
            # enter and redirect to the homepage
            login(request, new_user)
            return redirect('learning_logs:index')

    # returning empty or invalid form
    context = {'form': form}
    return render(request, 'registration/register.html', context)  # check path to template!!!


