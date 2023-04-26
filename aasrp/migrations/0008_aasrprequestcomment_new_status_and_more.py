# Generated by Django 4.0.7 on 2022-08-04 19:18

# Django
import django.db.models.deletion
import django.utils.timezone
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("eveonline", "0016_character_names_are_not_unique"),
        ("aasrp", "0007_aasrprequestcomment_comment_time_and_more"),
    ]

    operations = [
        migrations.AddField(
            model_name="aasrprequestcomment",
            name="new_status",
            field=models.CharField(
                blank=True,
                choices=[
                    ("Pending", "Pending"),
                    ("Approved", "Approved"),
                    ("Rejected", "Rejected"),
                ],
                default="",
                max_length=8,
            ),
        ),
        migrations.AlterField(
            model_name="aasrprequest",
            name="character",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                related_name="+",
                to="eveonline.evecharacter",
            ),
        ),
        migrations.AlterField(
            model_name="aasrprequestcomment",
            name="comment",
            field=models.TextField(blank=True, default=""),
        ),
        migrations.AlterField(
            model_name="aasrprequestcomment",
            name="comment_time",
            field=models.DateTimeField(
                default=django.utils.timezone.now, null=True, blank=True
            ),
        ),
    ]
