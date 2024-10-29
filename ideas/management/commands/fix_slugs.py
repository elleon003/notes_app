from django.core.management.base import BaseCommand
from django.utils.text import slugify
from django.db import connection
from ideas.models import Category, Tag

class Command(BaseCommand):
    help = 'Fix empty or problematic slugs in Categories and Tags'

    def column_exists(self, table, column):
        with connection.cursor() as cursor:
            cursor.execute("""
                SELECT COUNT(*)
                FROM information_schema.columns
                WHERE table_name = %s
                AND column_name = %s;
            """, [table, column])
            return cursor.fetchone()[0] > 0

    def handle(self, *args, **options):
        # Check if slug columns exist
        category_slug_exists = self.column_exists('ideas_category', 'slug')
        tag_slug_exists = self.column_exists('ideas_tag', 'slug')

        if not category_slug_exists:
            self.stdout.write(self.style.WARNING('Category slug column does not exist yet. Please run migrations first.'))
            return

        if not tag_slug_exists:
            self.stdout.write(self.style.WARNING('Tag slug column does not exist yet. Please run migrations first.'))
            return

        # Fix Categories
        empty_slug_categories = Category.objects.filter(slug='')
        if empty_slug_categories.exists():
            self.stdout.write(self.style.WARNING(f'Fixing {empty_slug_categories.count()} categories with empty slugs...'))
            for category in empty_slug_categories:
                base_slug = slugify(category.name)
                if not base_slug:
                    base_slug = 'untitled'
                category.slug = f"{base_slug}-{category.user.id}"
                category.save()
                self.stdout.write(f'  - Fixed Category ID: {category.id}, New slug: {category.slug}')
        else:
            self.stdout.write(self.style.SUCCESS('No categories with empty slugs found.'))

        # Fix duplicate category slugs
        from django.db.models import Count
        duplicate_category_slugs = Category.objects.values('slug').annotate(
            count=Count('id')).filter(count__gt=1)
        if duplicate_category_slugs.exists():
            self.stdout.write(self.style.WARNING(
                f'Fixing {duplicate_category_slugs.count()} duplicate category slugs...'))
            for dup in duplicate_category_slugs:
                categories = Category.objects.filter(slug=dup['slug'])
                for i, category in enumerate(categories[1:], 1):  # Skip first one
                    base_slug = slugify(category.name)
                    if not base_slug:
                        base_slug = 'untitled'
                    category.slug = f"{base_slug}-{category.user.id}-{i}"
                    category.save()
                    self.stdout.write(f'  - Fixed Category ID: {category.id}, New slug: {category.slug}')
        else:
            self.stdout.write(self.style.SUCCESS('No duplicate category slugs found.'))

        # Fix Tags
        empty_slug_tags = Tag.objects.filter(slug='')
        if empty_slug_tags.exists():
            self.stdout.write(self.style.WARNING(f'\nFixing {empty_slug_tags.count()} tags with empty slugs...'))
            for tag in empty_slug_tags:
                base_slug = slugify(tag.name)
                if not base_slug:
                    base_slug = 'untitled'
                tag.slug = f"{base_slug}-{tag.user.id}"
                tag.save()
                self.stdout.write(f'  - Fixed Tag ID: {tag.id}, New slug: {tag.slug}')
        else:
            self.stdout.write(self.style.SUCCESS('\nNo tags with empty slugs found.'))

        # Fix duplicate tag slugs
        duplicate_tag_slugs = Tag.objects.values('slug').annotate(
            count=Count('id')).filter(count__gt=1)
        if duplicate_tag_slugs.exists():
            self.stdout.write(self.style.WARNING(
                f'Fixing {duplicate_tag_slugs.count()} duplicate tag slugs...'))
            for dup in duplicate_tag_slugs:
                tags = Tag.objects.filter(slug=dup['slug'])
                for i, tag in enumerate(tags[1:], 1):  # Skip first one
                    base_slug = slugify(tag.name)
                    if not base_slug:
                        base_slug = 'untitled'
                    tag.slug = f"{base_slug}-{tag.user.id}-{i}"
                    tag.save()
                    self.stdout.write(f'  - Fixed Tag ID: {tag.id}, New slug: {tag.slug}')
        else:
            self.stdout.write(self.style.SUCCESS('No duplicate tag slugs found.'))
