# Generated by Django 3.2.23 on 2024-02-07 06:46

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('restaurant', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='restaurant',
            name='owner',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='owner', to=settings.AUTH_USER_MODEL),
        ),
        migrations.CreateModel(
            name='Follow',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('poster', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='poster_follows', to=settings.AUTH_USER_MODEL)),
                ('poster_follower', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='user_being_followed', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]