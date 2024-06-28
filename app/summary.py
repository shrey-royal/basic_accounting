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
from .report import *
from decimal import Decimal  # Import Decimal for precise arithmetic operations
from django.utils import timezone
from collections import defaultdict
from datetime import datetime, timedelta


from django.contrib import messages


def customer_report(request):
    customers = Customer.objects.all()
    packings = Packing.objects.all()
    context = {
        'customers': customers,
        'packings': packings,
    }
    return render(request, 'summary/customer_report.html', context)


def dispatch_summary(request):
    selected_data = Selected.objects.values_list('bill_no', flat=True)
    bundle_data = Bundle.objects.filter(status=True, bill_no__isnull=False)
    
    # Fetch related data using select_related or prefetch_related as needed
    bundle_data_list = list(bundle_data.select_related('bundle_entry'))

    context = {
        'selected_data': selected_data,
        'bundle_data': bundle_data_list,
    }
    return render(request, 'summary/dispatch_summary.html', context)


def transport_report(request):
    # Fetch selected items and related data
    selected_items = Selected.objects.filter(bill_no__isnull=False)

    # Fetch distinct vehicle numbers from packing_slip_new
    vehicle_numbers = packing_slip_new.objects.values_list('vehicle_no', flat=True).distinct()

    # Prepare data structure to collect data for each bill_no
    data_by_bill_no = {}

    for selected in selected_items:
        bill_no = selected.bill_no
        if bill_no not in data_by_bill_no:
            data_by_bill_no[bill_no] = {
                'vehicle_no': None,
                'date': selected.date,
                'point': selected.packing.point,  # Assuming point has a name field
                'quality': selected.packing.quality,  # Assuming quality has a name field
                'bundles': [],
                'party_name': selected.name,
                'bill_no': bill_no,  # Ensure bill_no is added to the dictionary
            }

    # Populate vehicle_no for each bill_no
    for bill_no, data in data_by_bill_no.items():
        packing_slip = packing_slip_new.objects.filter(bill_no=bill_no).first()
        if packing_slip:
            data['vehicle_no'] = packing_slip.vehicle_no

    # Populate bundles for each bill_no
    for selected in selected_items:
        bill_no = selected.bill_no
        bundles = Bundle.objects.filter(bundle_entry__id=selected.packing.id)
        for bundle in bundles:
            bundle_info = {
                'weight': bundle.weight,
            }
            data_by_bill_no[bill_no]['bundles'].append(bundle_info)

    context = {
        'data_by_bill_no': data_by_bill_no.values(),
        'vehicle_numbers': vehicle_numbers,
    }

    return render(request, 'summary/transport_report.html', context)