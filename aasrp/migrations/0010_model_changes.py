# Generated by Django 4.0.10 on 2023-06-22 16:13

# Django
import django.db.models.deletion
import django.utils.timezone
from django.conf import settings
from django.db import migrations, models

# AA SRP
import aasrp.models


class Migration(migrations.Migration):
    dependencies = [
        ("eveuniverse", "0010_alter_eveindustryactivityduration_eve_type_and_more"),
        ("eveonline", "0017_alliance_and_corp_names_are_not_unique"),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ("aasrp", "0009_add_fleet_type_to_srp_link"),
    ]

    operations = [
        migrations.CreateModel(
            name="Setting",
            fields=[
                (
                    "id",
                    models.AutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "srp_team_discord_channel_id",
                    models.PositiveBigIntegerField(
                        blank=True,
                        default=None,
                        null=True,
                        verbose_name="SRP Team Discord Channel ID",
                    ),
                ),
            ],
            options={
                "verbose_name": "setting",
                "verbose_name_plural": "settings",
                "default_permissions": (),
            },
        ),
        migrations.RenameModel(
            old_name="AaSrpInsurance",
            new_name="Insurance",
        ),
        migrations.RenameModel(
            old_name="AaSrpRequestComment",
            new_name="RequestComment",
        ),
        migrations.RenameModel(
            old_name="AaSrpLink",
            new_name="SrpLink",
        ),
        migrations.RenameModel(
            old_name="AaSrpRequest",
            new_name="SrpRequest",
        ),
        migrations.RenameModel(
            old_name="AaSrpUserSettings",
            new_name="UserSetting",
        ),
        migrations.AlterModelOptions(
            name="fleettype",
            options={
                "default_permissions": (),
                "verbose_name": "Fleet Type",
                "verbose_name_plural": "Fleet Types",
            },
        ),
        migrations.AlterModelOptions(
            name="requestcomment",
            options={
                "default_permissions": (),
                "verbose_name": "Comment",
                "verbose_name_plural": "Comments",
            },
        ),
        migrations.AlterModelOptions(
            name="srprequest",
            options={
                "default_permissions": (),
                "verbose_name": "Request",
                "verbose_name_plural": "Requests",
            },
        ),
        migrations.AlterField(
            model_name="fleettype",
            name="is_enabled",
            field=models.BooleanField(
                db_index=True,
                default=True,
                help_text="Whether this fleet type is active or not",
                verbose_name="Is enabled",
            ),
        ),
        migrations.AlterField(
            model_name="fleettype",
            name="name",
            field=models.CharField(
                help_text="Descriptive name of your fleet type",
                max_length=254,
                verbose_name="Name",
            ),
        ),
        migrations.AlterField(
            model_name="insurance",
            name="insurance_cost",
            field=models.FloatField(verbose_name="Insurance Cost"),
        ),
        migrations.AlterField(
            model_name="insurance",
            name="insurance_level",
            field=models.CharField(
                default="", max_length=254, verbose_name="Insurance Level"
            ),
        ),
        migrations.AlterField(
            model_name="insurance",
            name="insurance_payout",
            field=models.FloatField(verbose_name="Insurance Payout"),
        ),
        migrations.AlterField(
            model_name="insurance",
            name="srp_request",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                related_name="insurance",
                to="aasrp.srprequest",
                verbose_name="SRP Request",
            ),
        ),
        migrations.AlterField(
            model_name="requestcomment",
            name="comment",
            field=models.TextField(blank=True, default="", verbose_name="Comment"),
        ),
        migrations.AlterField(
            model_name="requestcomment",
            name="comment_time",
            field=models.DateTimeField(
                blank=True,
                default=django.utils.timezone.now,
                null=True,
                verbose_name="Comment Time",
            ),
        ),
        migrations.AlterField(
            model_name="requestcomment",
            name="comment_type",
            field=models.CharField(
                choices=[
                    ("Comment", "Comment"),
                    ("Request Added", "SRP Request Added"),
                    ("Request Information", "Additional Information"),
                    ("Reject Reason", "Reject Reason"),
                    ("Status Changed", "Status Changed"),
                    ("Reviser Comment", "Reviser Comment"),
                ],
                default="Comment",
                max_length=19,
                verbose_name="Comment Type",
            ),
        ),
        migrations.AlterField(
            model_name="requestcomment",
            name="creator",
            field=models.ForeignKey(
                blank=True,
                default=None,
                null=True,
                on_delete=models.SET(aasrp.models.get_sentinel_user),
                related_name="+",
                to=settings.AUTH_USER_MODEL,
                verbose_name="Creator",
            ),
        ),
        migrations.AlterField(
            model_name="requestcomment",
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
                verbose_name="New SRP Request Status",
            ),
        ),
        migrations.AlterField(
            model_name="requestcomment",
            name="srp_request",
            field=models.ForeignKey(
                blank=True,
                default=None,
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
                related_name="srp_request_comments",
                to="aasrp.srprequest",
                verbose_name="SRP Request",
            ),
        ),
        migrations.AlterField(
            model_name="srplink",
            name="aar_link",
            field=models.CharField(
                blank=True, default="", max_length=254, verbose_name="AAR Link"
            ),
        ),
        migrations.AlterField(
            model_name="srplink",
            name="creator",
            field=models.ForeignKey(
                blank=True,
                default=None,
                help_text="Who created the SRP link?",
                null=True,
                on_delete=models.SET(aasrp.models.get_sentinel_user),
                related_name="+",
                to=settings.AUTH_USER_MODEL,
                verbose_name="Creator",
            ),
        ),
        migrations.AlterField(
            model_name="srplink",
            name="fleet_commander",
            field=models.ForeignKey(
                blank=True,
                default=None,
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                related_name="+",
                to="eveonline.evecharacter",
                verbose_name="Fleet Commander",
            ),
        ),
        migrations.AlterField(
            model_name="srplink",
            name="fleet_doctrine",
            field=models.CharField(default="", max_length=254, verbose_name="Doctrine"),
        ),
        migrations.AlterField(
            model_name="srplink",
            name="fleet_time",
            field=models.DateTimeField(verbose_name="Fleet Time"),
        ),
        migrations.AlterField(
            model_name="srplink",
            name="fleet_type",
            field=models.ForeignKey(
                blank=True,
                default=None,
                help_text="The SRP link fleet type, if it's set",
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                related_name="+",
                to="aasrp.fleettype",
                verbose_name="Fleet Type",
            ),
        ),
        migrations.AlterField(
            model_name="srplink",
            name="srp_code",
            field=models.CharField(default="", max_length=16, verbose_name="SRP Code"),
        ),
        migrations.AlterField(
            model_name="srplink",
            name="srp_name",
            field=models.CharField(default="", max_length=254, verbose_name="SRP Name"),
        ),
        migrations.AlterField(
            model_name="srplink",
            name="srp_status",
            field=models.CharField(
                choices=[
                    ("Active", "Active"),
                    ("Closed", "Closed"),
                    ("Completed", "Completed"),
                ],
                default="Active",
                max_length=9,
                verbose_name="SRP Status",
            ),
        ),
        migrations.AlterField(
            model_name="srprequest",
            name="additional_info",
            field=models.TextField(
                blank=True, default="", verbose_name="Additional Information"
            ),
        ),
        migrations.AlterField(
            model_name="srprequest",
            name="character",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                related_name="+",
                to="eveonline.evecharacter",
                verbose_name="Character",
            ),
        ),
        migrations.AlterField(
            model_name="srprequest",
            name="creator",
            field=models.ForeignKey(
                blank=True,
                default=None,
                help_text="Who created the SRP link?",
                null=True,
                on_delete=models.SET(aasrp.models.get_sentinel_user),
                related_name="+",
                to=settings.AUTH_USER_MODEL,
                verbose_name="Creator",
            ),
        ),
        migrations.AlterField(
            model_name="srprequest",
            name="killboard_link",
            field=models.CharField(
                default="", max_length=254, verbose_name="Killboard Link"
            ),
        ),
        migrations.AlterField(
            model_name="srprequest",
            name="loss_amount",
            field=models.BigIntegerField(default=0, verbose_name="Loss Amount"),
        ),
        migrations.AlterField(
            model_name="srprequest",
            name="payout_amount",
            field=models.BigIntegerField(default=0, verbose_name="Payout Amount"),
        ),
        migrations.AlterField(
            model_name="srprequest",
            name="post_time",
            field=models.DateTimeField(
                default=django.utils.timezone.now, verbose_name="Request Time"
            ),
        ),
        migrations.AlterField(
            model_name="srprequest",
            name="reject_info",
            field=models.TextField(
                blank=True, default="", verbose_name="Reject Reason"
            ),
        ),
        migrations.AlterField(
            model_name="srprequest",
            name="request_code",
            field=models.CharField(
                default="", max_length=254, verbose_name="Request Code"
            ),
        ),
        migrations.AlterField(
            model_name="srprequest",
            name="request_status",
            field=models.CharField(
                choices=[
                    ("Pending", "Pending"),
                    ("Approved", "Approved"),
                    ("Rejected", "Rejected"),
                ],
                default="Pending",
                max_length=8,
                verbose_name="Request Status",
            ),
        ),
        migrations.AlterField(
            model_name="srprequest",
            name="ship",
            field=models.ForeignKey(
                blank=True,
                default=None,
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                related_name="srp_requests",
                to="eveuniverse.evetype",
                verbose_name="Ship Type",
            ),
        ),
        migrations.AlterField(
            model_name="srprequest",
            name="ship_name",
            field=models.CharField(
                default="", max_length=254, verbose_name="Ship Type"
            ),
        ),
        migrations.AlterField(
            model_name="srprequest",
            name="srp_link",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                related_name="srp_requests",
                to="aasrp.srplink",
                verbose_name="SRP Link",
            ),
        ),
        migrations.AlterField(
            model_name="usersetting",
            name="disable_notifications",
            field=models.BooleanField(
                default=False, verbose_name="Disable Notifications"
            ),
        ),
        migrations.AlterField(
            model_name="usersetting",
            name="user",
            field=models.ForeignKey(
                blank=True,
                default=None,
                null=True,
                on_delete=models.SET(aasrp.models.get_sentinel_user),
                related_name="+",
                to=settings.AUTH_USER_MODEL,
                verbose_name="User",
            ),
        ),
    ]
