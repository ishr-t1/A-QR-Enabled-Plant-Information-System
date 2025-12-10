from django.contrib import admin
from django.utils.html import format_html
from django.utils.safestring import mark_safe
from .models import Plant, PlantImage, QRCode, ReportIssue
from tinymce.widgets import TinyMCE
from django import forms


class PlantAdminForm(forms.ModelForm):
    class Meta:
        model = Plant
        fields = '__all__'
        widgets = {
            'local_names': TinyMCE(),
            'morphology': TinyMCE(),
            'chemical_const': TinyMCE(),
            'uses': TinyMCE(),
            'pharma_uses': TinyMCE(),
        }

class PlantImageInline(admin.TabularInline):
    model = PlantImage
    extra = 1

class QRCodeInline(admin.StackedInline):
    model = QRCode
    readonly_fields = ('qr_image', 'generated_at')
    extra = 0

    def has_add_permission(self, request, obj):
        return False  

@admin.register(Plant)
class PlantAdmin(admin.ModelAdmin):
    form = PlantAdminForm
    list_display = ['common_name', 'scientific_name', 'has_qr_code', 'created_at']
    list_filter = ['family', 'created_at']
    search_fields = ['common_name', 'scientific_name', 'family', 'local_names']
    inlines = [PlantImageInline, QRCodeInline]

    fieldsets = (
        ('Basic Information', {
            'fields': ('common_name', 'scientific_name', 'family')
        }),
        ('Detailed Information', {
            'fields': ('local_names', 'morphology', 'chemical_const', 'uses', 'pharma_uses'),
            'classes': ('collapse',)
        }),
    )

    def has_qr_code(self, obj):
        if hasattr(obj, 'qr_code'):
            return mark_safe('<span style="color: green;">✓ Yes</span>')
        return mark_safe('<span style="color: red;">✗ No</span>')
    has_qr_code.short_description = 'QR Code Generated'

@admin.register(PlantImage)
class PlantImageAdmin(admin.ModelAdmin):
    list_display = ['plant', 'description', 'uploaded_at']
    list_filter = ['uploaded_at']
    search_fields = ['plant__common_name', 'description']


@admin.register(QRCode)
class QRCodeAdmin(admin.ModelAdmin):
    list_display = ['plant', 'generated_at', 'qr_preview']
    readonly_fields = ('plant', 'qr_image', 'generated_at', 'qr_preview')

    # Disable add permission - QR codes are auto-generated
    def has_add_permission(self, request):
        return False

    # Disable change permission - QR codes shouldn't be edited
    def has_change_permission(self, request, obj=None):
        return False

    # Optional: disable delete if you want to keep all QR codes
    def has_delete_permission(self, request, obj=None):
        return True  # Change to False if you don't want deletion

    def qr_preview(self, obj):
        if obj.qr_image:
            return format_html(
                '<img src="{}" width="100" height="100" />',
                obj.qr_image.url
            )
        return "No QR Code"
    qr_preview.short_description = 'QR Code Preview'


@admin.register(ReportIssue)
class ReportIssueAdmin(admin.ModelAdmin):
    list_display = ['plant', 'issue_type','reported_at', 'reporter_name','reporter_email', 'status_badge']
    list_filter = ['status', 'issue_type', 'reported_at']
    search_fields = ['plant__common_name', 'issue_type', 'description', 'reporter_email']
    #list_editable=['status']
    # Update fields to include name and email
    readonly_fields = ('plant', 'issue_type', 'description', 'reported_at', 'reporter_name', 'reporter_email')

    # Fields to show in the edit form
    fields = ('plant', 'issue_type', 'description', 'reported_at', 'reporter_name', 'reporter_email', 'status')
    def has_add_permission(self, request):
        return False

    # Admin can only change status, not delete
    def has_delete_permission(self, request, obj=None):
        return True  # Change to False if you don't want admin to delete
    def status_badge(self, obj):
        colors = {
            'pending': 'orange',
            'reviewed': 'blue',
            'resolved': 'green'
        }
        return format_html(
            '<span style="background-color: {}; color: white; padding: 5px 10px; border-radius: 3px;">{}</span>',
            colors.get(obj.status, 'gray'),
            obj.get_status_display()
        )
    #status_badge.allow_tags = True
    status_badge.short_description = "Status"
    # it can be sorted by the underlying model field
    status_badge.admin_order_field = 'status'