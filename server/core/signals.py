from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from django.utils import timezone
from .models import MainData, Vault
from django.db.models import Q


# -------------------------
# HANDLE CREATE/UPDATE SIGNAL
# -------------------------
@receiver(post_save, sender=MainData)
def update_vault_on_main_data_save(sender, instance, created, **kwargs):
    """
    Auto-update Vault entries whenever MainData is created or updated.
    """
    if created:
        # Identify creator based on UCID or IG Handle
        ucid = instance.ucid
        ig_handle = instance.ig_handle
        
        # Fetch all relevant entries
        queryset = MainData.objects.filter(
            Q(ucid=ucid) | Q(ig_handle=ig_handle)
        )

        # Get the first and latest entries
        first_entry = queryset.first()
        latest_entry = queryset.order_by('-date').first()
        
        if first_entry and latest_entry:
            Vault.objects.update_or_create(
                ucid=ucid,
                ig_handle=ig_handle,
                defaults={
                    # Basic Details
                    'creator_name': first_entry.creator_name,
                    'channel_link': first_entry.channel_link,
                    'gender': first_entry.gender,
                    'language': first_entry.language,
                    'genre': first_entry.genre,
                    'ig_link': first_entry.ig_link,
                    'ig_subs': first_entry.ig_subs,
                    'pct_13_17': first_entry.pct_13_17,
                    'yt_genz_13_24': first_entry.yt_gen_z_13_24,
                    'rpr': first_entry.rpr,
                    
                    # Latest Details
                    'contacts': latest_entry.contacts,
                    'contact_name': latest_entry.contact_number,
                    'email_id': latest_entry.email_id,
                    'median_views': latest_entry.median_views,
                    'campaign_name': latest_entry.campaign_name,
                    'brand_name': latest_entry.brand_name,
                    'trend_type': latest_entry.trend_type,
                    'last_cost': latest_entry.current_cost,
                    'last_deliverable': latest_entry.current_deliverables,
                    'date_of_activation': latest_entry.date,
                    
                    # Metadata
                    'last_updated': timezone.now()
                }
            )


# -------------------------
# HANDLE DELETE SIGNAL
# -------------------------
@receiver(post_delete, sender=MainData)
def update_vault_on_main_data_delete(sender, instance, **kwargs):
    """
    Update or remove Vault entries when a MainData entry is deleted.
    """
    ucid = instance.ucid
    ig_handle = instance.ig_handle
    
    # Check if there are remaining entries for the same ucid or ig_handle
    remaining_entries = MainData.objects.filter(
        Q(ucid=ucid) | Q(ig_handle=ig_handle)
    )

    if remaining_entries.exists():
        # If entries remain, update Vault with the latest remaining data
        first_entry = remaining_entries.first()
        latest_entry = remaining_entries.order_by('-date').first()
        
        Vault.objects.update_or_create(
            ucid=ucid,
            ig_handle=ig_handle,
            defaults={
                # Basic Details
                'creator_name': first_entry.creator_name,
                'channel_link': first_entry.channel_link,
                'gender': first_entry.gender,
                'language': first_entry.language,
                'genre': first_entry.genre,
                'ig_link': first_entry.ig_link,
                'ig_subs': first_entry.ig_subs,
                'pct_13_17': first_entry.pct_13_17,
                'yt_genz_13_24': first_entry.yt_genz_13_24,
                'rpr': first_entry.rpr,
                
                # Latest Details
                'contacts': latest_entry.contacts,
                'contact_name': latest_entry.contact_number,
                'email_id': latest_entry.email_id,
                'median_views': latest_entry.median_views,
                'campaign_name': latest_entry.campaign_name,
                'brand_name': latest_entry.brand_name,
                'trend_type': latest_entry.trend_type,
                'last_cost': latest_entry.current_cost,
                'last_deliverable': latest_entry.current_deliverables,
                'date_of_activation': latest_entry.date,
                
                # Metadata
                'last_updated': timezone.now()
            }
        )
    else:
        # If no entries remain, delete the Vault entry
        Vault.objects.filter(
            Q(ucid=ucid) | Q(ig_handle=ig_handle)
        ).delete()
