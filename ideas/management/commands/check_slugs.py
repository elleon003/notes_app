from django.core.management.base import BaseCommand
from ideas.models import Category, Tag

class Command(BaseCommand):
    help = 'Check for empty or problematic slugs in Categories and Tags'

    def handle(self, *args, **options):
        # Check Categories
        empty_slug_categories = Category.objects.filter(slug='')
        if empty_slug_categories.exists():
            self.stdout.write(self.style.WARNING(f'Found {empty_slug_categories.count()} categories with empty slugs:'))
            for category in empty_slug_categories:
                self.stdout.write(f'  - Category ID: {category.id}, Name: "{category.name}", User ID: {category.user_id}')
        else:
            self.stdout.write(self.style.SUCCESS('No categories with empty slugs found.'))

        # Check for duplicate category slugs
        from django.db.models import Count
        duplicate_category_slugs = Category.objects.values('slug').annotate(
            count=Count('id')).filter(count__gt=1)
        if duplicate_category_slugs.exists():
            self.stdout.write(self.style.WARNING(
                f'Found {duplicate_category_slugs.count()} duplicate category slugs:'))
            for dup in duplicate_category_slugs:
                categories = Category.objects.filter(slug=dup['slug'])
                self.stdout.write(f'  Slug "{dup["slug"]}" is used by:')
                for cat in categories:
                    self.stdout.write(f'    - Category ID: {cat.id}, Name: "{cat.name}", User ID: {cat.user_id}')
        else:
            self.stdout.write(self.style.SUCCESS('No duplicate category slugs found.'))

        # Check Tags
        empty_slug_tags = Tag.objects.filter(slug='')
        if empty_slug_tags.exists():
            self.stdout.write(self.style.WARNING(f'\nFound {empty_slug_tags.count()} tags with empty slugs:'))
            for tag in empty_slug_tags:
                self.stdout.write(f'  - Tag ID: {tag.id}, Name: "{tag.name}", User ID: {tag.user_id}')
        else:
            self.stdout.write(self.style.SUCCESS('\nNo tags with empty slugs found.'))

        # Check for duplicate tag slugs
        duplicate_tag_slugs = Tag.objects.values('slug').annotate(
            count=Count('id')).filter(count__gt=1)
        if duplicate_tag_slugs.exists():
            self.stdout.write(self.style.WARNING(
                f'Found {duplicate_tag_slugs.count()} duplicate tag slugs:'))
            for dup in duplicate_tag_slugs:
                tags = Tag.objects.filter(slug=dup['slug'])
                self.stdout.write(f'  Slug "{dup["slug"]}" is used by:')
                for tag in tags:
                    self.stdout.write(f'    - Tag ID: {tag.id}, Name: "{tag.name}", User ID: {tag.user_id}')
        else:
            self.stdout.write(self.style.SUCCESS('No duplicate tag slugs found.'))