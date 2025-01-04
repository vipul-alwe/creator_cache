from django.db import models
from django.core.exceptions import ValidationError
from django.utils import timezone


# -----------------------
# 1. User Model
# -----------------------
class AppUsers(models.Model):
    full_name = models.CharField(max_length=200)
    email = models.EmailField(unique=True)  # Enforce uniqueness
    password = models.CharField(max_length=255)  # Store hashed passwords
    team_name = models.CharField(max_length=200)
    ts = models.DateTimeField(auto_now_add=True)  # Timestamp when created

    def __str__(self):
        return self.full_name


# -----------------------
# 2. Main Data Model
# -----------------------
class MainData(models.Model):
    creator_name = models.CharField(max_length=200, null=False)
    channel_link = models.URLField(max_length=500, null=True, blank=True)  # Auto-generated
    ucid = models.CharField(max_length=100, unique=True, null=True, blank=True)
    gender = models.CharField(max_length=50, null=True, blank=True)
    language = models.CharField(max_length=100, null=True, blank=True)
    genre = models.CharField(max_length=100, null=True, blank=True)
    ig_handle = models.CharField(max_length=200, unique=True, null=True, blank=True)
    ig_link = models.URLField(max_length=500, null=True, blank=True)  # Auto-generated
    ig_subs = models.IntegerField(null=True, blank=True)
    pct_13_17 = models.FloatField(null=True, blank=True)
    yt_gen_z_13_24 = models.FloatField(null=True, blank=True)
    rpr = models.FloatField(null=True, blank=True)
    contacts = models.TextField(null=False)  # Mandatory
    contact_number = models.CharField(max_length=15, null=True, blank=True)
    email_id = models.EmailField(max_length=200, null=True, blank=True)
    median_views = models.IntegerField(null=True, blank=True)
    campaign_name = models.CharField(max_length=200, null=False)  # Mandatory
    date = models.DateField(null=False)  # Mandatory
    brand_name = models.CharField(max_length=200, null=True, blank=True)
    trend_type = models.CharField(max_length=100, null=True, blank=True)
    current_cost = models.FloatField(null=False)  # Mandatory
    current_deliverables = models.TextField(null=False)  # Mandatory

    def clean(self):
        # Ensure either `ucid` or `ig_handle` is provided
        if not self.ucid and not self.ig_handle:
            raise ValidationError("Either 'ucid' or 'ig_handle' must be provided.")
        
        # Ensure either `contact_number` or `email_id` is provided
        if not self.contact_number and not self.email_id:
            raise ValidationError("Either 'contact_number' or 'email_id' must be provided.")

    def save(self, *args, **kwargs):
        # Auto-generate `channel_link` and `ig_link`
        if self.ucid:
            self.channel_link = f"https://www.youtube.com/channel/{self.ucid}"
        if self.ig_handle:
            self.ig_link = f"https://www.instagram.com/{self.ig_handle}"

        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.creator_name} - {self.campaign_name}"


# -----------------------
# 3. Temporary CSV Data Model
# -----------------------
class TempCSVData(models.Model):
    transaction_id = models.BigIntegerField(unique=True)
    uploaded_by = models.ForeignKey(AppUsers, on_delete=models.CASCADE)
    data = models.JSONField()  # Store CSV data as JSON temporarily
    upload_date = models.DateTimeField(auto_now_add=True)
    campaign_name = models.CharField(max_length=255, default='NA')

    # Add a status field for the transaction (Pending, Approved, Rejected)
    status = models.CharField(
        max_length=50,
        choices=[('Pending', 'Pending'), ('Approved', 'Approved'), ('Rejected', 'Rejected')],
        default='Pending'
    )

    def clean(self):
        """
        Ensure mandatory fields exist and invalid fields are not present.
        """
        mandatory_fields = [
            'creator_name', 'current_cost', 'current_deliverables',
            'contacts', 'campaign_name', 'date'
        ]

        # Validate mandatory fields
        for field in mandatory_fields:
            if field not in self.data:
                raise ValidationError(f"Mandatory field '{field}' is missing from the uploaded data.")

        # Validate either `ucid` or `ig_handle`
        if not self.data.get('ucid') and not self.data.get('ig_handle'):
            raise ValidationError("Either 'ucid' or 'ig_handle' must be provided in the uploaded data.")

        # Validate either `contact_number` or `email_id`
        if not self.data.get('contact_number') and not self.data.get('email_id'):
            raise ValidationError("Either 'contact_number' or 'email_id' must be provided in the uploaded data.")

        # Prevent inclusion of `channel_link` and `ig_link` in the uploaded data
        if 'channel_link' in self.data or 'ig_link' in self.data:
            raise ValidationError("Fields 'channel_link' and 'ig_link' should not be included in the uploaded data.")

    def __str__(self):
        return f"Temp Data - Transaction {self.transaction_id}"

# -----------------------
# 4. Transaction Log Model
# -----------------------
class TransactionLog(models.Model):
    transaction = models.ForeignKey(TempCSVData, on_delete=models.CASCADE)
    approved_by = models.ForeignKey(AppUsers, on_delete=models.SET_NULL, null=True, blank=True)
    status = models.CharField(
        max_length=50,
        choices=[
            ('Pending', 'Pending'),
            ('Approved', 'Approved'),
            ('Rejected', 'Rejected')
        ],
        default='Pending'
    )
    approval_date = models.DateTimeField(null=True, blank=True)
    comments = models.TextField(null=True, blank=True)
    campaign_name = models.CharField(max_length=255, default='NA') 

    def __str__(self):
        return f"Transaction {self.transaction.transaction_id} - {self.status}"


# -----------------------
# 5. The Vault
# -----------------------
class Vault(models.Model):
    # Unique Identifiers
    ucid = models.CharField(max_length=255, null=True, blank=True, unique=True)
    ig_handle = models.CharField(max_length=255, null=True, blank=True, unique=True)

    # Creator Information (Pulled from unique identifiers)
    creator_name = models.CharField(max_length=255)
    channel_link = models.URLField(null=True, blank=True)
    gender = models.CharField(max_length=50, null=True, blank=True)
    language = models.CharField(max_length=100, null=True, blank=True)
    genre = models.CharField(max_length=100, null=True, blank=True)
    ig_link = models.URLField(null=True, blank=True)
    ig_subs = models.IntegerField(null=True, blank=True)
    pct_13_17 = models.FloatField(null=True, blank=True)
    yt_genz_13_24 = models.FloatField(null=True, blank=True)
    rpr = models.FloatField(null=True, blank=True)

    # Most Recent Entry Details
    contacts = models.CharField(max_length=255, null=True, blank=True)
    contact_name = models.CharField(max_length=255, null=True, blank=True)
    email_id = models.EmailField(null=True, blank=True)
    median_views = models.IntegerField(null=True, blank=True)
    campaign_name = models.CharField(max_length=255, null=True, blank=True)
    brand_name = models.CharField(max_length=255, null=True, blank=True)
    trend_type = models.CharField(max_length=100, null=True, blank=True)
    last_cost = models.FloatField(null=True, blank=True)
    last_deliverable = models.CharField(max_length=255, null=True, blank=True)
    date_of_activation = models.DateField(null=True, blank=True)

    # Metadata
    last_updated = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"{self.creator_name} - {self.ucid or self.ig_handle}"