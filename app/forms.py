from django import forms
from .models import *
from django.forms import modelformset_factory
from django.contrib.auth.models import User


class CustomerForm(forms.ModelForm):
    class Meta:
        model = Customer
        fields = '__all__'

class client_ForgotPassword_Form(forms.ModelForm):
    email = forms.EmailField(required=True, widget=forms.EmailInput(
        attrs={'class': 'form-control',}))
    class Meta:
        model = User
        fields = ['email']

class client_OtpVerify_Form(forms.Form):
     otp = forms.CharField(required=True, error_messages={'required':'Please enter OTP'} ,max_length=6, widget=forms.TextInput(
        attrs={'class': 'form-control'}))
     
class QualityForm(forms.ModelForm):
    class Meta:
        model = Quality
        fields = '__all__'


        
class pointForm(forms.ModelForm):
    class Meta:
        model = Point
        fields = '__all__'

class BrandForm(forms.ModelForm):
    class Meta:
        model = Brand
        fields = '__all__'

       
class PackingForm(forms.ModelForm):
    class Meta:
        model = Packing
        fields = ['date_packing','name', 'lot_no', 'quality', 'point', 'brand', 'lot_kgs']

class BundleForm(forms.ModelForm):
    class Meta:
        model = Bundle
        fields = ['bundle', 'grade', 'sizes', 'sheet', 'weight', 'remarks']

class SelectedForm(forms.ModelForm):
    class Meta:
        model = Selected
        fields = ['name', 'bill_no', 'date']

        


class SPageForm(forms.ModelForm):
    quality = forms.ModelChoiceField(queryset=Quality.objects.all())
    point = forms.ModelChoiceField(queryset=Point.objects.all())

    class Meta:
        model = SPage
        fields = '__all__'

class LottForm(forms.Form):
    lot_no = forms.ChoiceField(choices=[])
    
    def __init__(self, *args, **kwargs):
        super(LottForm, self).__init__(*args, **kwargs)
        self.fields['lot_no'].choices = [(lot_no, lot_no) for lot_no in Packing.objects.values_list('lot_no', flat=True).distinct()]


class Packing_slip_new(forms.ModelForm):
    class Meta:
        model = packing_slip_new
        fields = ['bill_no', 'vehicle_no']