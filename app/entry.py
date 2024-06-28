from django.shortcuts import render, redirect
from django.contrib import messages

from .forms import *
from .master import *
from .models import *


from django.contrib import messages

def packing(request):
    qualities = Quality.objects.all()
    points = Point.objects.all()
    brands = Brand.objects.all()

    if request.method == 'POST':
        form = PackingForm(request.POST)
        if form.is_valid():
            packing = form.save(commit=False)  # Save the Packing instance without committing to the database yet

            # Retrieve the total_weight from the form data
            total_weight = request.POST.get('total_weight', 0)
            packing.total_weight = total_weight

            packing.save()  # Now save the Packing instance with the total_weight

            # Process bundle data from multiple rows
            bundle_data = zip(
                request.POST.getlist('bundle'),
                request.POST.getlist('grade'),
                request.POST.getlist('sizes'),
                request.POST.getlist('sheet'),
                request.POST.getlist('weight'),
                request.POST.getlist('remarks')
            )
            for bundle, grade, size, sheet, weight, remark in bundle_data:
                bundle_instance = Bundle(
                    bundle_entry=packing,  # Associate with the current Packing
                    bundle=bundle,
                    grade=grade,
                    sizes=size,
                    sheet=sheet,
                    weight=weight,
                    remarks=remark,
                )
                bundle_instance.save()  # Save each Bundle instance

            return redirect('index')  # Replace 'index' with your actual success URL
        else:
            # Form is invalid, display error messages
            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(request, f"Error in {field}: {error}")
    else:
        form = PackingForm()

    return render(request, 'entry/packing.html', {'form': form, 'qualities': qualities, 'points': points, 'brands': brands})



def selectedpage(request):
    if request.method == 'POST':
        form = SPageForm(request.POST)
        if form.is_valid():
            quality_id = form.cleaned_data['quality'].id
            point_id = form.cleaned_data['point'].id
            bundles = Bundle.objects.filter(bundle_entry__quality_id=quality_id, bundle_entry__point_id=point_id)
            customers = Customer.objects.all()  # Get all customers
            company_names = [customer.company_name for customer in customers]  # Extract company names
            return render(request, 'entry/sform.html', {'bundles': bundles, 'customers': customers,'company_names': company_names})
    else:
        form = SPageForm()
        
    qualities = Quality.objects.all()
    points = Point.objects.all()
    
    return render(request, 'entry/selected.html', {'form': form, 'qualities': qualities, 'points': points})

def dispatch(request):
    if request.method == 'POST':
        selected_bundles = request.POST.getlist('selected_bundles')
        name_id = request.POST.get('name')  # This will be the selected customer's ID
        bill_no = request.POST.get('bill_no')
        date = request.POST.get('date')

        for bundle_id in selected_bundles:
            bundle = Bundle.objects.get(id=int(bundle_id))
            bundle.status = True
            bundle.bill_no = bill_no 
            bundle.save()

            # Fetch the customer's company name from the ID
            customer = Customer.objects.get(id=name_id)
            customer_name = customer.company_name

            # Save the Selected record with the customer's company name
            Selected.objects.create(
                packing=bundle.bundle_entry,
                name=customer_name,
                bill_no=bill_no,
                date=date
            )

        return redirect('index')
    
    customers = Customer.objects.all()
    packings = Packing.objects.all()
    context = {
        'customers': customers,
        'packings': packings,
    }

    return render(request, 'entry/sform.html', context)


def lot(request):
    if request.method == 'POST':
        form = LottForm(request.POST)
        if form.is_valid():
            lot_no = form.cleaned_data['lot_no']
            bundles = Bundle.objects.filter(bundle_entry__lot_no=lot_no)
            customers = Customer.objects.all()  # Get all customers
            company_names = [customer.company_name for customer in customers]  # Extract company names
            return render(request, 'entry/sform.html', {'bundles': bundles, 'lot_no': lot_no, 'customers': customers,'company_names': company_names})
    else:
        form = LottForm()
        bundles = []

    lot_nos = Packing.objects.values_list('lot_no', flat=True).distinct()
    return render(request, 'entry/lot.html', {'form': form, 'bundles': bundles, 'lot_nos': lot_nos})

