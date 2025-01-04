from rest_framework import serializers
from .models import Vault

class VaultSerializer(serializers.ModelSerializer):
    class Meta:
        model = Vault
        fields = [
            'creator_name', 'channel_link', 'gender', 'language', 'genre',
            'ig_link', 'ig_subs', 'pct_13_17', 'yt_genz_13_24', 'rpr'
        ]
