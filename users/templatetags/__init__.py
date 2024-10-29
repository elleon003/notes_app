from django import template
from django.conf import settings
from django.utils.safestring import mark_safe

register = template.Library()

@register.simple_tag
def turnstile_widget():
    return mark_safe(
        f'<div class="cf-turnstile mb-4" data-sitekey="{settings.TURNSTILE_SITEKEY}"></div>'
    )

@register.simple_tag
def turnstile_script():
    return mark_safe(
        '<script src="https://challenges.cloudflare.com/turnstile/v0/api.js" async defer></script>'
    )
