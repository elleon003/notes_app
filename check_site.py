import os
import django

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "app.settings.dev")
django.setup()

from django.contrib.sites.models import Site

with open('site_config.txt', 'w') as f:
    f.write("Current Site Configuration:\n")
    for site in Site.objects.all():
        f.write(f"ID: {site.id}, Domain: {site.domain}, Name: {site.name}\n")

    f.write("\nAttempting to update Site with ID 1:\n")
    try:
        site = Site.objects.get(id=1)
        site.domain = 'alive-cleanly-flamingo.ngrok-free.app'
        site.name = 'Notes App'
        site.save()
        f.write(f"Updated Site - ID: {site.id}, Domain: {site.domain}, Name: {site.name}\n")
    except Exception as e:
        f.write(f"Error updating Site: {str(e)}\n")

print("Check site_config.txt for results")