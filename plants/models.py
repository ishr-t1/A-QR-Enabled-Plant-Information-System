from django.db import models
#from ckeditor.fields import RichTextField
from tinymce.models import HTMLField

# Plant Table
class Plant(models.Model):
    common_name = models.CharField(max_length=100)
    scientific_name = models.CharField(max_length=100)
    family = models.CharField(max_length=100)
    local_names = HTMLField(blank=True)
    morphology = HTMLField(blank=True)
    chemical_const =HTMLField(blank=True, verbose_name="Chemical Constituents")
    uses = HTMLField(blank=True, verbose_name="Traditional Uses")
    pharma_uses = HTMLField(blank=True, verbose_name="Pharmaceutical Uses")
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['common_name']

    def __str__(self):
        return f"{self.common_name} ({self.scientific_name})"

# PlantImage Table
class PlantImage(models.Model):
    plant = models.ForeignKey(Plant, on_delete=models.CASCADE, related_name='images')
    image = models.ImageField(upload_to='plant_images/')
    description = models.CharField(max_length=200, blank=True)
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Image of {self.plant.common_name}"

# QRCode Table
class QRCode(models.Model):
    plant = models.OneToOneField(Plant, on_delete=models.CASCADE, related_name='qr_code')
    qr_image = models.ImageField(upload_to='qrcodes/')
    generated_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"QR Code for {self.plant.common_name}"


# ReportIssue Table
class ReportIssue(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('reviewed', 'Reviewed'),
        ('resolved', 'Resolved'),
    ]

    plant = models.ForeignKey(Plant, on_delete=models.CASCADE, related_name='issues')
    issue_type = models.CharField(max_length=100)
    description = models.TextField()
    reporter_name = models.CharField(max_length=100, blank=True, null=True)
    reporter_email = models.EmailField(blank=True, null=True)
    reported_at = models.DateTimeField(auto_now_add=True)

    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')

    class Meta:
        ordering = ['-reported_at']

    def __str__(self):
        return f"Issue: {self.issue_type} - {self.plant.common_name}"