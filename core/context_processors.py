from .models import Profile


def profile_context(request):
    """Inject the logged-in user's Profile into every template context."""
    if request.user.is_authenticated:
        try:
            return {'profile': Profile.objects.get(user=request.user)}
        except Profile.DoesNotExist:
            pass
    return {}
