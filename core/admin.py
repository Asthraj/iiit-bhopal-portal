from django.contrib import admin
from .models import Profile, Subject, Assignment, Submission, Note


@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display  = ('user', 'role', 'branch', 'is_verified')
    list_filter   = ('role', 'branch', 'is_verified')
    search_fields = ('user__username', 'user__email')
    list_editable = ('is_verified',)   # Admin can tick verify directly from list view
    actions       = ['verify_users', 'unverify_users']

    def verify_users(self, request, queryset):
        queryset.update(is_verified=True)
        self.message_user(request, f"{queryset.count()} user(s) verified successfully.")
    verify_users.short_description = "✅ Verify selected users"

    def unverify_users(self, request, queryset):
        queryset.update(is_verified=False)
        self.message_user(request, f"{queryset.count()} user(s) unverified.")
    unverify_users.short_description = "❌ Unverify selected users"


admin.site.register(Subject)
admin.site.register(Assignment)
admin.site.register(Submission)
admin.site.register(Note)
