from django.contrib import admin
from .models import AppUsers, TempCSVData, MainData, TransactionLog


# -------------------------
# 1. AppUsers Admin
# -------------------------
@admin.register(AppUsers)
class AppUsersAdmin(admin.ModelAdmin):
    list_display = ('id', 'full_name', 'email', 'team_name', 'ts')
    search_fields = ('full_name', 'email')
    list_filter = ('team_name',)


# -------------------------
# 2. TempCSVData Admin
# -------------------------
@admin.register(TempCSVData)
class TempCSVDataAdmin(admin.ModelAdmin):
    list_display = ('transaction_id', 'uploaded_by', 'upload_date', 'status')
    search_fields = ('transaction_id', 'uploaded_by__full_name')
    list_filter = ('status',)
    ordering = ('-upload_date',)


# -------------------------
# 3. MainData Admin
# -------------------------
@admin.register(MainData)
class MainDataAdmin(admin.ModelAdmin):
    list_display = ('creator_name', 'ucid', 'campaign_name', 'date', 'current_cost')
    search_fields = ('creator_name', 'ucid', 'campaign_name')
    list_filter = ('date', 'campaign_name')
    ordering = ('-date',)


# -------------------------
# 4. TransactionLog Admin
# -------------------------
@admin.register(TransactionLog)
class TransactionLogAdmin(admin.ModelAdmin):
    list_display = ('transaction', 'status', 'approved_by', 'approval_date', 'comments')
    search_fields = ('transaction__transaction_id', 'approved_by__full_name')
    list_filter = ('status', 'approval_date')
    ordering = ('-approval_date',)

