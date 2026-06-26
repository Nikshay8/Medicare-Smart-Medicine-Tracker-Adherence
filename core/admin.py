from django.contrib import admin
from .models import Medicine, MedicineLog, Caregiver


@admin.register(Medicine)
class MedicineAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'user', 'time')
    search_fields = ('name', 'user__username')
    list_filter = ('time', 'user')


@admin.register(MedicineLog)
class MedicineLogAdmin(admin.ModelAdmin):
    list_display = ('id', 'medicine', 'status', 'date', 'alert_sent')
    search_fields = ('medicine__name', 'status')
    list_filter = ('status', 'date', 'alert_sent')


@admin.register(Caregiver)
class CaregiverAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'user', 'email')
    search_fields = ('name', 'email', 'user__username')