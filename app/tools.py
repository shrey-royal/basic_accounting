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
from django.utils.timezone import make_aware
from django.views.decorators.http import require_POST



from django.contrib import messages


def packing_slip_new(request):
    if request.method == 'POST':
        form = Packing_slip_new(request.POST)
        if form.is_valid():
            form.save()
            return redirect('index')  # Replace 'success_url' with the URL you want to redirect to after successful form submission
    else:
        form = Packing_slip_new()
    
    selected_data = Selected.objects.values_list('bill_no', 'date')
    context = {
        'selected_data': selected_data,
        'form': form,
    }
    return render(request, 'tools/packing_slip_new.html', context)



def packing_slip(request):
    selected_data = Selected.objects.values_list('bill_no', flat=True)
    bundle_data = Bundle.objects.filter(status=True, bill_no__isnull=False)
    bundle_data_list = list(bundle_data)  # Convert bundle_data queryset to a list
    context = {
        'selected_data': selected_data,
        'bundle_data': bundle_data_list,
    }
    return render(request, 'tools/packing_slip.html', context)



def remove_data(request):
    if request.method == 'POST':
        selected_date = request.POST.get('date')

        if selected_date:
            # Perform deletion of records before the selected date
            # Example logic to delete Packing records older than the selected date
            packings_to_delete = Packing.objects.filter(date_packing__lt=selected_date)
            packings_to_delete.delete()

            # Redirect to the same page or any desired URL after deletion
            return redirect('remove_data')  # Redirect to the same view or modify the URL

    # Handle GET requests here
    packings = Packing.objects.all()
    return render(request, 'tools/remove_data.html', {'packings': packings})