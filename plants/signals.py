# plants/signals.py
import qrcode
from io import BytesIO
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.core.files import File
from django.conf import settings
from django.urls import reverse

from .models import Plant, QRCode

@receiver(post_save, sender=Plant)
def generate_qr_code(sender, instance, created, **kwargs):
    if created:  # Only generate QR on plant creation
        # Generate URL for plant detail page
        base_url = settings.SITE_URL  # We'll add this to settings
        plant_url = f"{base_url}{reverse('plant_detail', kwargs={'pk': instance.pk})}"

        # Generate QR code with the URL
        qr = qrcode.QRCode(
            version=1,
            error_correction=qrcode.constants.ERROR_CORRECT_H,  # High error correction
            box_size=10,
            border=4,
        )

        qr.add_data(plant_url)
        qr.make(fit=True)

        # Create QR code image
        qr_image = qr.make_image(fill_color="black", back_color="white")

        # Save to buffer
        buffer = BytesIO()
        qr_image.save(buffer, format='PNG')
        buffer.seek(0)

        # Create or update QR code record
        qr_obj, created = QRCode.objects.get_or_create(plant=instance)
        qr_obj.qr_image.save(
            f"{instance.common_name.replace(' ', '_')}_qr.png",
            File(buffer),
            save=True
        )
        buffer.close()