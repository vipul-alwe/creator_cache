from rest_framework import serializers
from .models import Users, Creators, Campaigns, CreatorCampaign, DataUploadTransaction

class UsersSerializer(serializers.ModelSerializer):
    class Meta:
        model = Users
        fields = '__all__'


class CreatorsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Creators
        fields = '__all__'
        read_only_fields = ['channel_link', 'ig_link']  # Auto-generated fields


class CampaignsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Campaigns
        fields = '__all__'


class CreatorCampaignSerializer(serializers.ModelSerializer):
    class Meta:
        model = CreatorCampaign
        fields = '__all__'


class DataUploadTransactionSerializer(serializers.ModelSerializer):
    uploaded_by = serializers.StringRelatedField()  # Converts related user to a string representation
    approval_by = serializers.StringRelatedField()  # Same for the approver

    class Meta:
        model = DataUploadTransaction
        fields = '__all__'
        read_only_fields = ['upload_date', 'status', 'approval_by']  # Prevent these from being modified
