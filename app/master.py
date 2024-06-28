from django.shortcuts import render, redirect
from .forms import *

  # Replace with your actual form import

def customer(request):
    if request.method == 'POST':
        form = CustomerForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('index')  # Replace 'index' with your actual success URL
    else:
        form = CustomerForm()

    # Define the list of states
    states = [
        'Andhra Pradesh', 'Arunachal Pradesh', 'Assam', 'Bihar', 'Chhattisgarh', 'Goa', 'Gujarat', 
        'Haryana', 'Himachal Pradesh', 'Jharkhand', 'Karnataka', 'Kerala', 'Madhya Pradesh', 'Maharashtra', 
        'Manipur', 'Meghalaya', 'Mizoram', 'Nagaland', 'Odisha (Orissa)', 'Punjab', 'Rajasthan', 'Sikkim', 
        'Tamil Nadu', 'Telangana', 'Tripura', 'Uttar Pradesh', 'Uttarakhand', 'West Bengal',
        'Andaman and Nicobar Islands', 'Chandigarh', 'Dadra and Nagar Haveli and Daman and Diu',
        'Lakshadweep', 'Delhi (National Capital Territory of Delhi)', 'Puducherry', 'Ladakh'
    ]

    # Define cities for each state
    cities_by_state = {
        'Andhra Pradesh': ['Visakhapatnam', 'Vijayawada', 'Guntur', 'Nellore', 'Kurnool'],
        'Arunachal Pradesh': ['Itanagar', 'Naharlagun'],
        'Assam': ['Guwahati', 'Silchar', 'Dibrugarh', 'Jorhat', 'Nagaon'],
        'Bihar': ['Patna', 'Gaya', 'Bhagalpur', 'Muzaffarpur', 'Purnia'],
        'Chhattisgarh': ['Raipur', 'Bhilai', 'Bilaspur', 'Korba', 'Raigarh'],
        'Goa': ['Panaji', 'Margao', 'Vasco da Gama'],
        'Gujarat': ['Ahmedabad', 'Surat', 'Vadodara', 'Rajkot', 'Gandhinagar'],
        'Haryana': ['Faridabad', 'Gurgaon', 'Panipat', 'Ambala', 'Yamunanagar'],
        'Himachal Pradesh': ['Shimla', 'Mandi', 'Solan', 'Dharamshala', 'Kullu'],
        'Jharkhand': ['Ranchi', 'Jamshedpur', 'Dhanbad', 'Bokaro Steel City', 'Deoghar'],
        'Karnataka': ['Bangalore', 'Mysore', 'Hubli', 'Mangalore', 'Belgaum'],
        'Kerala': ['Thiruvananthapuram', 'Kochi', 'Kozhikode', 'Thrissur', 'Malappuram'],
        'Madhya Pradesh': ['Bhopal', 'Indore', 'Jabalpur', 'Gwalior', 'Ujjain'],
        'Maharashtra': ['Mumbai', 'Pune', 'Nagpur', 'Nashik', 'Aurangabad'],
        'Manipur': ['Imphal', 'Thoubal'],
        'Meghalaya': ['Shillong', 'Tura'],
        'Mizoram': ['Aizawl', 'Lunglei'],
        'Nagaland': ['Kohima', 'Dimapur'],
        'Odisha (Orissa)': ['Bhubaneswar', 'Cuttack', 'Rourkela', 'Berhampur', 'Sambalpur'],
        'Punjab': ['Ludhiana', 'Amritsar', 'Jalandhar', 'Patiala', 'Bathinda'],
        'Rajasthan': ['Jaipur', 'Jodhpur', 'Udaipur', 'Kota', 'Bikaner'],
        'Sikkim': ['Gangtok', 'Namchi'],
        'Tamil Nadu': ['Chennai', 'Coimbatore', 'Madurai', 'Tiruchirappalli', 'Salem'],
        'Telangana': ['Hyderabad', 'Warangal', 'Nizamabad', 'Karimnagar', 'Ramagundam'],
        'Tripura': ['Agartala', 'Udaipur'],
        'Uttar Pradesh': ['Lucknow', 'Kanpur', 'Agra', 'Varanasi', 'Meerut'],
        'Uttarakhand': ['Dehradun', 'Haridwar', 'Rishikesh', 'Nainital', 'Mussoorie'],
        'West Bengal': ['Kolkata', 'Howrah', 'Durgapur', 'Asansol', 'Siliguri'],
        'Andaman and Nicobar Islands': ['Port Blair'],
        'Chandigarh': ['Chandigarh'],
        'Dadra and Nagar Haveli and Daman and Diu': ['Daman', 'Diu', 'Silvassa'],
        'Lakshadweep': ['Kavaratti'],
        'Delhi (National Capital Territory of Delhi)': ['New Delhi', 'North Delhi', 'South Delhi', 'East Delhi', 'West Delhi'],
        'Puducherry': ['Pondicherry', 'Karaikal', 'Mahe', 'Yanam'],
        'Ladakh': ['Leh', 'Kargil'],
    }

    return render(request, 'master/customer.html', {'form': CustomerForm(), 'states': states, 'cities_by_state': cities_by_state})


def quality(request):
    if request.method == 'POST':
        form = QualityForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('index')  # Replace 'index' with your actual success URL
    else:
        form = QualityForm()

    return render(request, 'master/quality.html', {'form': form})

def point(request):
    if request.method == 'POST':
        form = pointForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('index')  # Replace 'index' with your actual success URL
    else:
        form = pointForm()

    return render(request, 'master/point.html', {'form': form})




def brand(request):
    if request.method == 'POST':
        form = BrandForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('index')  # Replace 'index' with your actual success URL
    else:
        form = BrandForm()

    return render(request, 'master/brand.html', {'form': form})