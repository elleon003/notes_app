from django.db import migrations, models

class Migration(migrations.Migration):
    dependencies = [
        ('ideas', '0004_fix_empty_slugs'),
    ]

    operations = [
        # Now add the unique constraints
        migrations.AlterField(
            model_name='category',
            name='slug',
            field=models.SlugField(max_length=100, unique=True),
        ),
        migrations.AlterField(
            model_name='tag',
            name='slug',
            field=models.SlugField(unique=True),
        ),
    ]
