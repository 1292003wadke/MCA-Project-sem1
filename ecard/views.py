from django.shortcuts import render, redirect
from django.core.mail import send_mail
from django.contrib.auth.decorators import login_required
from .models import UserProfile, User
from .forms import UserProfileForm, UserRegistrationForm  # Assuming you have this form

# User Registration View
def user_registration(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.save()  # Save the user first, so we can associate a UserProfile

            # Create or get the associated UserProfile
            user_profile, created = UserProfile.objects.get_or_create(user=user)
            user_profile.encrypt_data()  # Encrypt sensitive data in the profile
            user_profile.save()

            # Generate virtual e-card for the user (using data from user_profile)
            e_card = user_profile.generate_virtual_e_card()

            # Send the virtual e-card to the user's email
            send_mail(
                'Your Virtual E-Card',
                f'Your virtual e-card is:\n\n{e_card}',
                'your_email@gmail.com',  # Replace with your email
                [user.email],             # Use the user's email, not mobile_number
            )

            return redirect('registration_success')
    else:
        form = UserRegistrationForm()

    return render(request, 'users/registration_form.html', {'form': form})

# Registration Success View
def registration_success(request):
    return render(request, 'users/registration_success.html')

# Admin Dashboard View
def admin_dashboard(request):
    # Assuming 'verified' is a field on UserProfile
    users = User.objects.filter(userprofile__status="In Process")  # Or use the relevant field in UserProfile
    return render(request, 'users/admin_dashboard.html', {'users': users})

# Verify User
def verify_user(request, user_id):
    user = User.objects.get(id=user_id)
    # Assuming 'verified' field is in the UserProfile model
    user_profile = user.userprofile
    user_profile.status = "Approved"  # Update the status
    user_profile.ecard_generated = True  # Set e-card generated flag to True
    user_profile.save()

    # Send email notification to the user
    send_mail(
        'Verification Successful',
        'Your registration has been successfully verified.',
        'your_email@gmail.com',  # Replace with your email
        [user.email],  # Send to the user's email address
    )

    return redirect('admin_dashboard')

@login_required
def profile(request):
    user_profile, created = UserProfile.objects.get_or_create(user=request.user)
    if request.method == "POST":
        form = UserProfileForm(request.POST, instance=user_profile)
        if form.is_valid():
            form.save()
            return redirect("profile")
    else:
        form = UserProfileForm(instance=user_profile)
    return render(request, "profile.html", {"form": form, "profile": user_profile})
