from django.shortcuts import render, redirect
from django.contrib import messages
from django.shortcuts import render, get_object_or_404
from .forms import *
from .master import *
from .models import *
from .entry import *
from .modify import *


from django.contrib import messages


def modify_packing(request):
    packings = Packing.objects.all()  # Fetch all records from Packing model
    return render(request, 'modify/modify_packing.html', {'packings': packings})


def edit_packing(request, pk):
    packing = Packing.objects.get(pk=pk)

    if request.method == 'POST':
        packing_form = PackingForm(request.POST, instance=packing)
        bundle_forms = [BundleForm(request.POST, instance=bundle) for bundle in packing.bundles.all()]
        
        if packing_form.is_valid() and all(bundle_form.is_valid() for bundle_form in bundle_forms):
            packing_form.save()
            for bundle_form in bundle_forms:
                bundle_form.save()
            return redirect('modify_packing')  # Redirect back to modify_packing URL

    else:
        packing_form = PackingForm(instance=packing)
        bundle_forms = [BundleForm(instance=bundle) for bundle in packing.bundles.all()]

    return render(request, 'modify/edit_packing.html', {'packing_form': packing_form, 'bundle_forms': bundle_forms})


def delete_packing(request, pk):
    packing = get_object_or_404(Packing, pk=pk)
    if request.method == 'POST':
        packing.delete()
        return redirect('modify_packing')  # Adjust the redirect to your needs
    return render(request, 'modify/delete_packing.html', {'packing': packing})







def modify_dispatch(request):
    # Filter packings based on whether they have a related Selected entry
    packings = Packing.objects.filter(selected__isnull=False)
    return render(request, 'modify/modify_dispatch.html', {'packings': packings})

def edit_dispatch(request, pk):
    packing = Packing.objects.get(pk=pk)
    selected_instance, created = Selected.objects.get_or_create(packing=packing)

    if request.method == 'POST':
        selected_form = SelectedForm(request.POST, instance=selected_instance)
        if selected_form.is_valid():
            selected_form.save()
            return redirect('modify_dispatch')  # Redirect back to modify_dispatch URL after saving
    else:
        selected_form = SelectedForm(instance=selected_instance)

    return render(request, 'modify/edit_dispatch.html', {'selected_form': selected_form})


def recall_dispatch(request, packing_id):
    if request.method == 'POST':
        try:
            packing = Packing.objects.get(pk=packing_id)
            for bundle in packing.bundles.all():
                bundle.status = False
                bundle.save()
            packing.selected_set.all().delete()
            messages.success(request, "Dispatch recalled successfully.")
            return redirect('modify_dispatch')
        except Packing.DoesNotExist:
            messages.error(request, "Packing record not found.")
            return redirect('index')
    else:
        messages.error(request, "Invalid request method.")
        return redirect('modify_dispatch')
