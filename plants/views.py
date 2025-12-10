
from django.shortcuts import render, get_object_or_404, redirect
from .models import Plant,  ReportIssue
from django.contrib import messages
from django.db.models import Q
import random

def custom_500_view(request):
    """
    Custom view for 500 errors.
    The response uses the 500.html template.
    """
    return render(request, '500.html', status=500)


# Create your views here.
def home(request):
    """Display home page with random 3 plants (carousel style)"""
    all_plants = list(Plant.objects.all())
    random.shuffle(all_plants)   # shuffle order
    plants = all_plants[:6]      # take only 6 random plants

    context = {
        'plants': plants,
    }
    return render(request, 'plants/home.html', context)

def plant_detail(request, pk):
    """Display detailed plant information when QR code is scanned"""
    plant = get_object_or_404(Plant, pk=pk)

    context = {
        'plant': plant,
    }

    return render(request, 'plants/plant_detail.html', context)

def search_plants(request):
    """Search plants by name, family, or scientific name"""
    query = request.GET.get('q', '').strip()

    if query:
        # Search in common_name, scientific_name, family, and local_names
        results = Plant.objects.filter(
            Q(common_name__icontains=query) |
            Q(scientific_name__icontains=query) |
            Q(family__icontains=query) |
            Q(local_names__icontains=query)
        ).distinct()
    else:
        results = None

    # Get all plants for when no search query
    all_plants = Plant.objects.all()
    context = {
        'query': query,
        'results': results,
        'all_plants': all_plants,
    }

    return render(request, 'plants/search_results.html', context)

def report_issue(request, pk):
    """Handle issue reporting for a plant"""
    plant = get_object_or_404(Plant, pk=pk)

    if request.method == 'POST':
         #Get NEW FIELDS
        reporter_name = request.POST.get('reporter_name')
        reporter_email = request.POST.get('reporter_email')
        issue_type = request.POST.get('issue_type')
        description = request.POST.get('description')

        if issue_type and description:
            ReportIssue.objects.create(
                plant=plant,
                issue_type=issue_type,
                description=description,
                reporter_name=reporter_name,
                reporter_email=reporter_email,
                status='pending'
            )
            messages.success(request, 'Thank you! Your report has been submitted successfully.')
        else:
            messages.error(request, 'Please fill in all required fields.')
    return redirect('plant_detail', pk=pk)