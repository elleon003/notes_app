from django.db import migrations
from django.utils.text import slugify

def fix_empty_slugs(apps, schema_editor):
    # Fix Category slugs
    Category = apps.get_model('ideas', 'Category')
    for category in Category.objects.filter(slug=''):
        base_slug = slugify(category.name)
        if not base_slug:
            base_slug = 'untitled'
        category.slug = f"{base_slug}-{category.user.id}"
        category.save()

    # Fix Tag slugs
    Tag = apps.get_model('ideas', 'Tag')
    for tag in Tag.objects.filter(slug=''):
        base_slug = slugify(tag.name)
        if not base_slug:
            base_slug = 'untitled'
        tag.slug = f"{base_slug}-{tag.user.id}"
        tag.save()

class Migration(migrations.Migration):
    dependencies = [
        ('ideas', '0003_auto_20240428_2038'),  # Update this to your actual previous migration
    ]

    operations = [
        migrations.RunPython(fix_empty_slugs, reverse_code=migrations.RunPython.noop),
    ]
