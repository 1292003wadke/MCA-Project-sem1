from django.contrib import admin
from .models import UserProfile, ECard

@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ("user", "aadhaar", "pan", "mobile_number", "status", "ecard_generated")
    list_filter = ("status", "ecard_generated")
    search_fields = ("user__username", "aadhaar", "pan")

    def approve_user(self, request, queryset):
        # Approve the user and update the related ECard
        queryset.update(status="Approved")
        
        # Update ECard generation status for users who are approved
        for user_profile in queryset:
            ecard = ECard.objects.filter(user=user_profile.user).first()
            if ecard:
                ecard.ecard_generated = True
                ecard.save()

    approve_user.short_description = "Approve selected users"

    def reject_user(self, request, queryset):
        queryset.update(status="Rejected")
        
        # Reset the ECard generation status when user is rejected
        for user_profile in queryset:
            ecard = ECard.objects.filter(user=user_profile.user).first()
            if ecard:
                ecard.ecard_generated = False
                ecard.save()

    reject_user.short_description = "Reject selected users"

    actions = [approve_user, reject_user]

@admin.register(ECard)
class ECardAdmin(admin.ModelAdmin):
    list_display = ("user", "ecard_generated", "issued_at")
    list_filter = ("ecard_generated",)
    search_fields = ("user__username",)
