from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login
from .forms import RegistrationForm, LoginForm

# Home page view for the root URL (same as login page)
def home(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('home')  # Redirect to the home page after successful login
            else:
                form.add_error(None, "Invalid login credentials.")
    else:
        form = LoginForm()

    return render(request, 'welcome.html', {'form': form})  # Pass form to the template

# Registration view
def register(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data['password'])  # Hash the password
            user.save()  # Save the user to the database
            return redirect('login')  # Redirect to login page after successful registration
    else:
        form = RegistrationForm()

    return render(request, 'register.html', {'form': form})  # Pass form to the template
