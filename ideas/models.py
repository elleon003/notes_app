from django.db import models
from django.conf import settings
from django.utils import timezone 
from django.utils.text import slugify


class Category(models.Model):
    name = models.CharField(max_length=100)
    slug = models.SlugField(max_length=100, unique=True)  # Removed blank=True
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='categories')

    def save(self, *args, **kwargs):
        # Always generate a slug, don't check if it's empty
        base_slug = slugify(self.name)
        if not base_slug:
            base_slug = 'untitled'  # Fallback for empty names
        self.slug = f"{base_slug}-{self.user.id}"
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name

    class Meta:
        unique_together = ['name', 'user']
        verbose_name_plural = 'Categories'


class Tag(models.Model):
    name = models.CharField(max_length=50)
    slug = models.SlugField(max_length=50, unique=True)  # Removed blank=True
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='tags')

    def save(self, *args, **kwargs):
        # Always generate a slug, don't check if it's empty
        base_slug = slugify(self.name)
        if not base_slug:
            base_slug = 'untitled'  # Fallback for empty names
        self.slug = f"{base_slug}-{self.user.id}"
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name

    class Meta:
        unique_together = ['name', 'user']


class Idea(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='ideas')
    content = models.TextField()
    side_notes = models.TextField(blank=True)
    start_date = models.DateTimeField(null=True, blank=True)
    due_date = models.DateTimeField(null=True, blank=True)
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, blank=True)
    tags = models.ManyToManyField(Tag, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.content[:50]}..." if len(self.content) > 50 else self.content

    class Meta:
        ordering = ['-created_at']
