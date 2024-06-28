from django.shortcuts import render, redirect
from django.contrib import messages
from django.shortcuts import render, get_object_or_404
from django.template.loader import render_to_string
from django.http import HttpResponse
from .forms import *
from .master import *
from .models import *
from .entry import *
from .modify import *
from decimal import Decimal  # Import Decimal for precise arithmetic operations
from django.utils import timezone
from collections import defaultdict
from datetime import datetime, timedelta


from django.contrib import messages


def packing_book(request):
    packings = Packing.objects.all()  # Fetch all records from Packing model
    return render(request, 'report/packing_book.html', {'packings': packings})


def stock_book(request):
    packings = Packing.objects.prefetch_related('bundles').filter(bundles__status=False).distinct()
    return render(request, 'report/stock_book.html', {'packings': packings})


def dispatch_book(request):
    packings = Packing.objects.prefetch_related('bundles').filter(bundles__status=True).distinct()
    selected = Selected.objects.all()

    return render(request, 'report/dispatch_book.html', {'packings': packings,'selected': selected})


def size_book(request):
    packings = Packing.objects.all()  # Fetch all records from Packing model
    sizes = Packing.objects.values_list('bundles__sizes', flat=True).distinct()  # Get unique sizes
    return render(request, 'report/size_book.html', {'packings': packings, 'sizes': sizes})

def stock_summary(request):
    # Fetch the packings and brands
    packings = Packing.objects.prefetch_related('bundles').all()
    brands = Brand.objects.all()

    # Group the data
    grouped_data = {}
    for packing in packings:
        for bundle in packing.bundles.all():
            key = (packing.point, packing.quality, packing.brand.brand)
            if key not in grouped_data:
                grouped_data[key] = {
                    'point': packing.point,
                    'quality': packing.quality,
                    'sizes_weights': {},
                    'count': 0,
                    'total_weight': Decimal(0),  # Initialize as Decimal
                    'brand': packing.brand.brand,
                }
            size = bundle.sizes
            weight = Decimal(bundle.weight)
            if size in grouped_data[key]['sizes_weights']:
                grouped_data[key]['sizes_weights'][size] += weight
            else:
                grouped_data[key]['sizes_weights'][size] = weight

            grouped_data[key]['count'] += 1
            grouped_data[key]['total_weight'] += weight

    # Convert sizes_weights to a formatted string
    for item in grouped_data.values():
        item['sizes_weights'] = ', '.join(f'{size}={weight}' for size, weight in item['sizes_weights'].items())

    # Convert the grouped data to a list
    grouped_data_list = list(grouped_data.values())

    return render(request, 'report/stock_summary.html', {
        'packings': grouped_data_list,
        'brands': brands,
    })



def lot_summary(request):
    # Get the date from the request
    date_filter = request.GET.get('date', None)
    
    # Parse the date if provided, otherwise default to today's date
    if date_filter:
        date_filter = datetime.strptime(date_filter, '%Y-%m-%d')
    else:
        date_filter = timezone.now()

    # Fetch the packings and brands, filtered by date
    packings = Packing.objects.prefetch_related('bundles').filter(date_packing__lte=date_filter).all()
    brands = Brand.objects.all()

    # Group the data by lot_no, point, and quality
    grouped_data = {}
    for packing in packings:
        key = (packing.lot_no, packing.point, packing.quality)
        if key not in grouped_data:
            grouped_data[key] = {
                'date_packing': packing.date_packing,
                'lot_no': packing.lot_no,
                'point': packing.point,
                'quality': packing.quality,
                'sizes_weights': {},
                'count': 0,
                'total_weight': Decimal(0),  # Initialize as Decimal
            }
        for bundle in packing.bundles.all():
            size = bundle.sizes
            weight = Decimal(bundle.weight)
            if size in grouped_data[key]['sizes_weights']:
                grouped_data[key]['sizes_weights'][size] += weight
            else:
                grouped_data[key]['sizes_weights'][size] = weight

            grouped_data[key]['count'] += 1
            grouped_data[key]['total_weight'] += weight

    # Convert sizes_weights to a formatted string
    for item in grouped_data.values():
        item['sizes_weights'] = ', '.join(f'{size}={weight}' for size, weight in item['sizes_weights'].items())

    # Convert the grouped data to a list
    grouped_data_list = list(grouped_data.values())

    return render(request, 'report/lot_summary.html', {
        'packings': grouped_data_list,
        'brands': brands,
    })


def production_register(request):
    # Get the date range from the request
    start_date = request.GET.get('start_date', None)
    end_date = request.GET.get('end_date', None)
    
    # Parse the dates if provided, otherwise default to a wide range
    if start_date and end_date:
        start_date = datetime.strptime(start_date, '%Y-%m-%d')
        end_date = datetime.strptime(end_date, '%Y-%m-%d')
    else:
        start_date = timezone.now() - timezone.timedelta(days=365)  # Default to last 365 days
        end_date = timezone.now()

    # Fetch the packings and brands, filtered by date range
    packings = Packing.objects.prefetch_related('bundles').filter(date_packing__range=(start_date, end_date)).all()
    brands = Brand.objects.all()

    # Group the data by date and lot_no, point, and quality
    data_by_date = defaultdict(list)
    for packing in packings:
        for bundle in packing.bundles.all():
            item = {
                'date_packing': packing.date_packing,
                'lot_no': packing.lot_no,
                'weight': Decimal(bundle.weight),
                'bundle': bundle.bundle,
                'quality': packing.quality,  # Assuming `name` is a field in `Quality` model
                'point': packing.point,  # Assuming `name` is a field in `Point` model
                'brand': packing.brand  # Assuming `name` is a field in `Brand` model
            }
            data_by_date[packing.date_packing].append(item)

    # Compute totals for each date
    grouped_data = []
    for date_packing, items in data_by_date.items():
        date_total_weight = sum(item['weight'] for item in items)
        date_total_bundles = len(items)
        for item in items:
            grouped_data.append(item)
        # Append the total row for the current date
        grouped_data.append({
            'date_packing': date_packing,
            'lot_no': 'Total',
            'weight': date_total_weight,
            'bundle': date_total_bundles,
            'quality': '',
            'point': '',
            'brand': ''
        })

    return render(request, 'report/production_register.html', {
        'packings': grouped_data,
        'brands': brands,
    })



def lot_register(request):
    # Get the date range from the request
    start_date = request.GET.get('start_date', None)
    end_date = request.GET.get('end_date', None)
    
    # Parse the dates if provided, otherwise default to a wide range
    if start_date and end_date:
        start_date = datetime.strptime(start_date, '%Y-%m-%d')
        end_date = datetime.strptime(end_date, '%Y-%m-%d')
    else:
        start_date = timezone.now() - timezone.timedelta(days=365)  # Default to last 365 days
        end_date = timezone.now()

    # Fetch the packings and brands, filtered by date range
    packings = Packing.objects.prefetch_related('bundles').filter(date_packing__range=(start_date, end_date)).all()[:5]

    # Group the data by date and lot_no, point, and quality
    data_by_date = defaultdict(list)
    for packing in packings:
        for bundle in packing.bundles.all():
            pack_kgs = packing.total_weight if packing.total_weight else 0
            lot_weight = packing.lot_kgs if packing.lot_kgs else 0
            shortage = lot_weight - float(pack_kgs) if lot_weight else 0
            percentage = (shortage / lot_weight) * 100 if lot_weight else 0

            item = {
                'lot_no': packing.lot_no,
                'quality': packing.quality,
                'lot_weight': lot_weight,
                'sheet': bundle.sheet,
                'bundle': bundle.bundle,
                'pack_kgs': pack_kgs,
                'shortage': shortage,
                'percentage': percentage,
            }
            data_by_date[packing.date_packing].append(item)

    # Compute totals for each date
    grouped_data = []
    for date_packing, items in data_by_date.items():
        date_total_weight = sum(item['lot_weight'] for item in items)
        date_total_bundles = len(items)
        for item in items:
            grouped_data.append(item)
        # Append the total row for the current date
        grouped_data.append({
            'lot_no': 'Total',
            'quality': '',
            'lot_weight': date_total_weight,
            'sheet': '',
            'bundle': date_total_bundles,
            'pack_kgs': '',
            'shortage': '',
            'percentage': ''
        })

    return render(request, 'report/lot_register.html', {
        'packings': grouped_data,
    })