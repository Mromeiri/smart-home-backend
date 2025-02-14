
from django.contrib import admin
from .models import *
@admin.register(AppUser)
class AppUsersAdmin(admin.ModelAdmin):
    
    list_display = ('username', 'email', 'phone', 'date_registration', 'is_active','solde')
    search_fields = ('username', 'email', 'phone')
    ordering = ('-date_registration',)
    readonly_fields=('solde',)

@admin.register(ContactMessage)
class ContactMessageAdmin(admin.ModelAdmin):
    list_display = ('user', 'email', 'subject', 'message')
    search_fields = ('user__username', 'email', 'subject', 'message')
    def has_add_permission(self, request):
        return False

    def has_delete_permission(self, request, obj=None):
        return False
    def has_change_permission(self, request, obj=None):
        return False

@admin.register(Notification)
class NotificationAdmin(admin.ModelAdmin):
    readonly_fields=('isread',)
    list_display = ('user', 'date', 'title', 'isread')
    search_fields = ('user__username', 'title', 'isread')

@admin.register(NotificationML)
class NotificationMLAdmin(admin.ModelAdmin):
    readonly_fields=('isread',)
    list_display = ('user', 'date', 'title', 'isread','detail')
    search_fields = ('user__username', 'title', 'isread')
@admin.register(Announcement)
class AnnouncementAdmin(admin.ModelAdmin):
    list_display = ('date', 'title')
    search_fields = ('title',)


@admin.register(ReadAnnouncement)
class ReadAnnouncementAdmin(admin.ModelAdmin):
    list_display = ('announcement', 'user')
