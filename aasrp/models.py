"""
Our Models
"""

# Django
from django.contrib.auth.models import User
from django.db import models
from django.utils import timezone
from django.utils.translation import gettext as _

# Alliance Auth
from allianceauth.eveonline.models import EveCharacter

# Alliance Auth (External Libs)
from eveuniverse.models import EveType

# AA SRP
from aasrp.managers import SettingManager


def get_sentinel_user():
    """
    Get or create sentinel user
    :return:
    """

    return User.objects.get_or_create(username="deleted")[0]


class SingletonModel(models.Model):
    """
    SingletonModel
    """

    class Meta:  # pylint: disable=too-few-public-methods
        """
        Model meta definitions
        """

        abstract = True

    def save(self, *args, **kwargs):
        """
        Save action

        :param args:
        :type args:
        :param kwargs:
        :type kwargs:
        :return:
        :rtype:
        """

        if self.__class__.objects.count():
            self.pk = self.__class__.objects.first().pk

        super().save(*args, **kwargs)

    def delete(self, *args, **kwargs):
        """
        Delete action

        :param args:
        :type args:
        :param kwargs:
        :type kwargs:
        :return:
        :rtype:
        """

        pass  # pylint: disable=unnecessary-pass


class AaSrp(models.Model):
    """
    Meta model for app permissions
    """

    class Meta:  # pylint: disable=too-few-public-methods
        """
        General definitions
        """

        verbose_name = "AA-SRP"
        managed = False
        default_permissions = ()
        permissions = (
            # Can open the SRP app and submit SRP requests
            ("basic_access", "Can access the AA-SRP module"),
            # Can create SRP links
            ("create_srp", "Can create new SRP links"),
            # Can manage the complete SRP module
            ("manage_srp", "Can manage SRP"),
            # Can manage SRP requests only
            ("manage_srp_requests", "Can manage SRP requests"),
        )


class FleetType(models.Model):
    """
    FleetType
    """

    id = models.AutoField(primary_key=True)

    name = models.CharField(
        max_length=254,
        help_text=_("Descriptive name of your fleet type"),
        verbose_name=_("Name"),
    )

    is_enabled = models.BooleanField(
        default=True,
        db_index=True,
        help_text=_("Whether this fleet type is active or not"),
        verbose_name=_("Is enabled"),
    )

    class Meta:  # pylint: disable=too-few-public-methods
        """
        AFatLinkType :: Meta
        """

        default_permissions = ()
        verbose_name = _("Fleet Type")
        verbose_name_plural = _("Fleet Types")

    def __str__(self) -> str:
        """
        Return the objects string name

        :return:
        :rtype:
        """

        return str(self.name)


class SrpLink(models.Model):
    """
    SRP link model
    """

    class Status(models.TextChoices):
        """
        Choices for SRP status
        """

        ACTIVE = "Active", _("Active")
        CLOSED = "Closed", _("Closed")
        COMPLETED = "Completed", _("Completed")

    srp_name = models.CharField(max_length=254, default="", verbose_name=_("SRP Name"))
    srp_status = models.CharField(
        max_length=9,
        choices=Status.choices,
        default=Status.ACTIVE,
        verbose_name=_("SRP Status"),
    )
    srp_code = models.CharField(max_length=16, default="", verbose_name=_("SRP Code"))
    fleet_commander = models.ForeignKey(
        EveCharacter,
        related_name="+",
        null=True,
        blank=True,
        default=None,
        on_delete=models.SET_NULL,
        verbose_name=_("Fleet Commander"),
    )
    fleet_doctrine = models.CharField(
        max_length=254, default="", verbose_name=_("Doctrine")
    )

    fleet_type = models.ForeignKey(
        FleetType,
        related_name="+",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        default=None,
        help_text=_("The SRP link fleet type, if it's set"),
        verbose_name=_("Fleet Type"),
    )

    fleet_time = models.DateTimeField(verbose_name=_("Fleet Time"))
    aar_link = models.CharField(
        max_length=254, blank=True, default="", verbose_name=_("AAR Link")
    )

    creator = models.ForeignKey(
        User,
        related_name="+",
        null=True,
        blank=True,
        default=None,
        on_delete=models.SET(value=get_sentinel_user),
        help_text=_("Who created the SRP link?"),
        verbose_name=_("Creator"),
    )

    class Meta:  # pylint: disable=too-few-public-methods
        """
        Meta definitions
        """

        default_permissions = ()
        verbose_name = _("SRP Link")
        verbose_name_plural = _("SRP Links")

    def __str__(self) -> str:
        """
        Return the objects string name

        :return:
        :rtype:
        """

        return str(self.srp_name)

    @property
    def total_cost(self):
        """
        Total cost for this SRP link

        :return:
        :rtype:
        """

        return sum(
            int(r.payout_amount)
            for r in self.srp_requests.filter(request_status=SrpRequest.Status.APPROVED)
        )

    @property
    def total_requests(self):
        """
        Number of total SRP requests

        :return:
        :rtype:
        """

        return self.srp_requests.count()

    @property
    def pending_requests(self):
        """
        Number of pending SRP requests

        :return:
        :rtype:
        """

        return self.srp_requests.filter(
            request_status=SrpRequest.Status.PENDING
        ).count()

    @property
    def approved_requests(self):
        """
        Number of approved SRP requests

        :return:
        :rtype:
        """

        return self.srp_requests.filter(
            request_status=SrpRequest.Status.APPROVED
        ).count()

    @property
    def rejected_requests(self):
        """
        Number of rejected SRP requests

        :return:
        :rtype:
        """

        return self.srp_requests.filter(
            request_status=SrpRequest.Status.REJECTED
        ).count()

    @property
    def requests(self):
        """
        All SRP requests

        :return:
        :rtype:
        """

        return self.srp_requests.all()


class SrpRequest(models.Model):
    """
    SRP Request model
    """

    class Status(models.TextChoices):
        """
        Choices for SRP Request status
        """

        PENDING = "Pending", _("Pending")
        APPROVED = "Approved", _("Approved")
        REJECTED = "Rejected", _("Rejected")

    request_code = models.CharField(
        max_length=254, default="", verbose_name=_("Request Code")
    )
    creator = models.ForeignKey(
        User,
        related_name="+",
        null=True,
        blank=True,
        default=None,
        on_delete=models.SET(value=get_sentinel_user),
        help_text=_("Who created the SRP link?"),
        verbose_name=_("Creator"),
    )
    character = models.ForeignKey(
        EveCharacter,
        related_name="+",
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        verbose_name=_("Character"),
    )
    ship_name = models.CharField(
        max_length=254, default="", verbose_name=_("Ship Type")
    )
    ship = models.ForeignKey(
        EveType,
        related_name="srp_requests",
        null=True,
        blank=True,
        default=None,
        on_delete=models.SET_NULL,
        verbose_name=_("Ship Type"),
    )
    killboard_link = models.CharField(
        max_length=254, default="", verbose_name=_("Killboard Link")
    )
    additional_info = models.TextField(
        blank=True, default="", verbose_name=_("Additional Information")
    )
    request_status = models.CharField(
        max_length=8,
        choices=Status.choices,
        default=Status.PENDING,
        verbose_name=_("Request Status"),
    )
    payout_amount = models.BigIntegerField(default=0, verbose_name=_("Payout Amount"))
    srp_link = models.ForeignKey(
        SrpLink,
        related_name="srp_requests",
        on_delete=models.CASCADE,
        verbose_name=_("SRP Link"),
    )
    loss_amount = models.BigIntegerField(default=0, verbose_name=_("Loss Amount"))
    post_time = models.DateTimeField(
        default=timezone.now, verbose_name=_("Request Time")
    )
    reject_info = models.TextField(
        blank=True, default="", verbose_name=_("Reject Reason")
    )

    class Meta:  # pylint: disable=too-few-public-methods
        """
        Meta definitions
        """

        default_permissions = ()
        verbose_name = _("Request")
        verbose_name_plural = _("Requests")

    def __str__(self):
        """
        Return the objects string name

        :return:
        :rtype:
        """

        # AA SRP
        from aasrp.helper.character import (  # pylint: disable=import-outside-toplevel
            get_main_character_from_user,
        )

        character_name = self.character.character_name
        user_name = get_main_character_from_user(self.creator)
        ship = self.ship.name
        request_code = self.request_code

        return _(
            "{character_name} ({user_name}) SRP Request for: {ship} ({request_code})"
        ).format(
            character_name=character_name,
            user_name=user_name,
            ship=ship,
            request_code=request_code,
        )


class Insurance(models.Model):
    """
    Insurance Model
    """

    srp_request = models.ForeignKey(
        SrpRequest,
        on_delete=models.CASCADE,
        related_name="insurance",
        verbose_name=_("SRP Request"),
    )
    insurance_level = models.CharField(
        max_length=254, default="", verbose_name=_("Insurance Level")
    )
    insurance_cost = models.FloatField(verbose_name=_("Insurance Cost"))
    insurance_payout = models.FloatField(verbose_name=_("Insurance Payout"))

    class Meta:  # pylint: disable=too-few-public-methods
        """
        Meta definitions
        """

        default_permissions = ()
        verbose_name = _("Ship Insurance")
        verbose_name_plural = _("Ship Insurances")


class RequestComment(models.Model):
    """
    SRP Request Comments model
    """

    class Type(models.TextChoices):
        """
        Choices for comment types
        """

        COMMENT = "Comment", _("Comment")
        REQUEST_ADDED = "Request Added", _("SRP Request Added")
        REQUEST_INFO = "Request Information", _("Additional Information")
        REJECT_REASON = "Reject Reason", _("Reject Reason")
        STATUS_CHANGE = "Status Changed", _("Status Changed")
        REVISER_COMMENT = "Reviser Comment", _("Reviser Comment")

    comment = models.TextField(blank=True, default="", verbose_name=_("Comment"))

    comment_type = models.CharField(
        max_length=19,
        choices=Type.choices,
        default=Type.COMMENT,
        verbose_name=_("Comment Type"),
    )

    creator = models.ForeignKey(
        User,
        related_name="+",
        null=True,
        blank=True,
        default=None,
        on_delete=models.SET(value=get_sentinel_user),
        verbose_name=_("Creator"),
    )

    srp_request = models.ForeignKey(
        SrpRequest,
        related_name="srp_request_comments",
        null=True,
        blank=True,
        default=None,
        on_delete=models.CASCADE,
        verbose_name=_("SRP Request"),
    )

    comment_time = models.DateTimeField(
        default=timezone.now,
        null=True,
        blank=True,
        # Translators: This is the time when the comment was made
        verbose_name=_("Comment Time"),
    )

    new_status = models.CharField(
        max_length=8,
        choices=SrpRequest.Status.choices,
        blank=True,
        default="",
        # Translators: New SRP request status that might have been set
        verbose_name=_("New SRP Request Status"),
    )

    class Meta:  # pylint: disable=too-few-public-methods
        """
        Meta definitions
        """

        default_permissions = ()
        verbose_name = _("Comment")
        verbose_name_plural = _("Comments")


class UserSetting(models.Model):
    """
    User settings
    """

    user = models.ForeignKey(
        User,
        related_name="+",
        null=True,
        blank=True,
        default=None,
        on_delete=models.SET(value=get_sentinel_user),
        verbose_name=_("User"),
    )

    disable_notifications = models.BooleanField(
        default=False, verbose_name=_("Disable Notifications")
    )

    class Meta:  # pylint: disable=too-few-public-methods
        """
        Meta definitions
        """

        default_permissions = ()
        verbose_name = _("User Settings")
        verbose_name_plural = _("User Settings")


class Setting(SingletonModel):
    """
    SRP module settings
    """

    class Field(models.TextChoices):
        """
        Choices for Setting.Field
        """

        SRP_TEAM_DISCORD_CHANNEL_ID = "srp_team_discord_channel_id", _(
            "SRP Team Discord Channel ID"
        )

    srp_team_discord_channel_id = models.PositiveBigIntegerField(
        null=True,
        default=None,
        blank=True,
        verbose_name=Field.SRP_TEAM_DISCORD_CHANNEL_ID.label,  # pylint: disable=no-member
    )

    objects = SettingManager()

    class Meta:  # pylint: disable=too-few-public-methods
        """
        Meta definitions
        """

        default_permissions = ()
        verbose_name = _("setting")
        verbose_name_plural = _("settings")

    def __str__(self) -> str:
        """
        Return the objects string name

        :return:
        :rtype:
        """

        return str(_("AA-SRP Settings"))
