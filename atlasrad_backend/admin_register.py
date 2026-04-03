"""
AtlasRad - Enregistrement au panneau d'administration Django.
"""
from django.contrib import admin
from accounts.models import User
from analyses.models import Analysis


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ['username', 'email', 'first_name', 'last_name', 'role', 'hospital', 'is_active']
    list_filter = ['role', 'is_active', 'is_staff']
    search_fields = ['username', 'email', 'first_name', 'last_name', 'hospital']
    ordering = ['-date_joined']


@admin.register(Analysis)
class AnalysisAdmin(admin.ModelAdmin):
    list_display = ['id', 'user', 'modality', 'description', 'ai_model', 'status', 'confidence_score', 'created_at']
    list_filter = ['status', 'modality', 'created_at']
    search_fields = ['user__username', 'patient_id', 'result']
    ordering = ['-created_at']
    readonly_fields = ['created_at', 'updated_at']
