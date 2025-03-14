from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from .forms import RegistrationForm, LoginForm
from django.contrib.auth import get_user_model

User = get_user_model()  # Reference to the custom user model

# Home page view for login
def home(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user_obj = authenticate(request, username=username, password=password)  # Avoid conflict with global `User`
            if user_obj is not None:
                login(request, user_obj)
                return redirect('home')  # Redirect after login
            else:
                form.add_error(None, "Invalid login credentials.")
    else:
        form = LoginForm()

    return render(request, 'welcome.html', {'form': form})  # Pass form to the template

# Registration view
from django.shortcuts import render, redirect
from django.contrib.auth import get_user_model
from .forms import RegistrationForm

User = get_user_model()  # Reference to the custom user model


def register(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            email = form.cleaned_data['email']

            # Check if username or email already exists
            if User.objects.filter(username=username).exists():
                form.add_error('username', "This username is already taken.")
            else:
                user = form.save(commit=False)  # Create user but don't save yet
                user.set_password(form.cleaned_data["password"])  # Hash password
                user.save()  # Now save user with hashed password
                return redirect('home')  # Redirect to login/home page

    else:
        form = RegistrationForm()

    return render(request, 'register.html', {'form': form})  # Pass form to template
