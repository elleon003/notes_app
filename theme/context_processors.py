from django.conf import settings

def turnstile_settings(request):
    return {
        'settings': {
            'TURNSTILE_SITEKEY': settings.TURNSTILE_SITEKEY,
        }
    }
