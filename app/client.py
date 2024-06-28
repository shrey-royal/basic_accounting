from .models import *
from .forms import *
from django.shortcuts import render
from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import authenticate, login as django_login, logout
from django.contrib.auth.hashers import make_password
from django.http import HttpResponse
from django.contrib.auth.models import User 
from django.core.mail import send_mail
from django.conf import settings
import random
 # Assuming you're using Django's built-in User model

def register(request):
    if request.method == 'POST':
        full_name = request.POST.get('Full_Name', '')
        email = request.POST.get('Email', '')
        password = request.POST.get('Password', '')
        contact_no = request.POST.get('Contact_No', '')
        organization_name = request.POST.get('Organization_Name', '')
        address = request.POST.get('Address', '')
        
        # Check if the email already exists
        if User.objects.filter(email=email).exists():
            messages.error(request, f'Email "{email}" is already taken. Please choose a different one.')
            return render(request, 'register.html', {
                'full_name': full_name,
                'email': email,
                'password': password,
                'contact_no': contact_no,
                'organization_name': organization_name,
                'address': address
            })  # Render the registration form again with error message and filled data
        
        # Create a new user instance
        new_user = User.objects.create_user(username=email, email=email, password=password)
        
        # Set additional fields
        new_user.first_name = full_name  # Assuming full name is stored as first name
        new_user.contact_no = contact_no
        new_user.organization_name = organization_name
        new_user.address = address
        
        # Save the user to the database
        new_user.save()
        
        # Redirect to login page or any other page
        return render(request, 'login.html')
    
    elif request.method == 'GET':
        return render(request, 'register.html')  # Render the registration form initially
    
    else:
        return render(request, 'error.html')  # Handle other HTTP methods if needed


def login_view(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        
        # Authenticate the user
        user = authenticate(request, username=email, password=password)
        
        if user is not None:
            # User is authenticated, log them in
            django_login(request, user)
            messages.success(request, 'Login successful')
            return redirect('index')  # Redirect to the homepage
        else:
            # Authentication failed, display error message
            user_exists = User.objects.filter(email=email).exists()
            if not user_exists:
                messages.error(request, f'Email "{email}" does not exist.')
            else:
                messages.error(request, 'Incorrect password for the given email.')
    
    # If it's a GET request or authentication failed, render the login form
    return render(request, 'login.html')


def client_ForgotPassword(request):
    if request.method == "POST":
        fp = client_ForgotPassword_Form(request.POST)
        if fp.is_valid():
            email = fp.cleaned_data['email']
            is_email = User.objects.filter(email__iexact=email).exists()
            if is_email:
                OTP = random.randint(111111, 999999)
                subject = 'Password Reset OTP'
                message = f"Your OTP is {OTP}."
                email_from = settings.EMAIL_HOST_USER
                email_to = [email]
                send_mail(subject, message, email_from, email_to)

                request.session["reset_password_OTP"] = OTP
                request.session["reset_password_EMAIL"] = email
                request.session.set_expiry(900)  # 15 minutes
                return redirect('verify_otp')
            else:
                messages.error(request, "Email not found, please signup!")
                return redirect('register')
        else:
            messages.error(request, "Form is invalid")
    else:
        fp = client_ForgotPassword_Form()
    
    template = "forget_password.html"
    return render(request, template, {'form': fp})

def client_OtpVerify(request):
    if request.method == 'POST':
        omf = client_OtpVerify_Form(request.POST)
        if omf.is_valid():
            otp = omf.cleaned_data['otp']
            session_otp = request.session.get('reset_password_OTP')
            if str(otp) == str(session_otp):
                return redirect('reset_password')
            else:
                messages.error(request, "Please enter valid OTP")
                return redirect('verify_otp')

        else:
            messages.error(request, "Form is invalid")
    else:
        omf = client_OtpVerify_Form()
    
    template = "verify_otp.html"
    return render(request, template, {'form': omf})

def client_ResetPassword(request):
    if request.method == "POST":
        password = request.POST['password1']
        c_password = request.POST['password2']
        if password == c_password:
            email_var = request.session.get('reset_password_EMAIL')
            if email_var:
                usr = User.objects.get(email=email_var)
                usr.set_password(password)
                usr.save()
                request.session.flush()  # Clear all sessions
                return redirect('login')
            else:
                messages.error(request, "Session expired, please try again")
                return redirect('login')
        else:
            messages.error(request, "Passwords do not match")
    template = "reset_password.html"
    return render(request, template)

def logout_view(request):
    logout(request)
    return redirect('login')