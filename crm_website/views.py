from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, authenticate
from django.contrib import messages
from .forms import SignUpForm, AddRecordForm
from .models import CustomerDeletedRecords, CustomerRecords


from django.http import FileResponse
import io
from reportlab.pdfgen import canvas
from reportlab.lib.units import inch
from reportlab.lib.pagesizes import letter

# Create your views here.

def generate_pdf(request):
    buf = io.BytesIO()
    lines = []
    c = canvas.Canvas(buf, pagesize=letter, bottomup=0)
    textobj = c.beginText()
    textobj.setTextOrigin(inch, inch)
    records = CustomerRecords.objects.all()
    for record in records:
        lines.append(record.first_name + ' ' + record.last_name + '  Details')
        lines.append(record.email)
        lines.append(record.phone)
        lines.append(record.address)
        lines.append(record.city)
        lines.append(record.state)
        lines.append(record.postcode)
        #lines.append(record.created_at)
        #lines.append(record.id)
        lines.append('===========================================\n')
        lines.append(" ")
    for line in lines:
        textobj.textLine(line)

    c.drawText(textobj)
    c.showPage()
    c.save()
    buf.seek(0)
    return FileResponse(buf, as_attachment=True, filename='customer_records.pdf')


def home_page(request):
    customer_records = CustomerRecords.objects.all()
    print('customer_records-----------------', customer_records)
    #print('customer_records-----------------', customer_records.first_name)
    print('METHOD-------', request.method)
    if request.method == "POST":
        print('inside the POST METHOD---------------------------')
        #Get the user details from Form
        username = request.POST.get('username')
        password = request.POST.get('password')
        #authenticate the user
        user = authenticate(request, username=username, password=password)
        print('user---------------', user)
        if user:
            login(request, user)
            messages.success(request, 'You have been logged in successfully...')
            return render(request, 'home_page.html', {'records':customer_records})
            #return redirect('home')
        else:
            messages.error(request, 'Please enter the correct username and ' \
                           'password to login application. Note that both fields may be case-sensitive.')
            return redirect('home')
    else:
        print('inside the GET method-------------------------------')
        return render(request, 'home_page.html', {'records':customer_records})
    
def logout_user(request):
    logout(request)
    messages.success(request, 'you have been logged out successfully...')
    return redirect('home')

def register_user(request):
	if request.method == 'POST':
		form = SignUpForm(request.POST)
		if form.is_valid():
			form.save()
			# Authenticate and login
			#username = form.cleaned_data['username']
			#password = form.cleaned_data['password1']
			#user = authenticate(username=username, password=password)
			#login(request, user)
			messages.success(request, "You Have Successfully Registered! Welcome!")
			return redirect('home')
	else:
		form = SignUpForm()
		return render(request, 'register_page.html', {'form':form})

	return render(request, 'register_page.html', {'form':form})


def update_record(request, record_id):
    print('UPDATE  record_id--->>>>', record_id)
    print('UPDATE record_id TYPE ------->>', type(record_id))
    #print(MM)
    record = CustomerRecords.objects.get(id=record_id)
    form = AddRecordForm(request.POST or None, instance=record)
    if form.is_valid():
        form.save()
        return redirect('home')
    return render(request, 'update_record.html', {'form':form, 'record': record} )


def delete_record(request, record_id):
    record = CustomerRecords.objects.get(id=record_id)
    #form = DeletedRecordForm(request.POST)
    
    CustomerDeletedRecords.objects.update_or_create(
                first_name = record.first_name,
                last_name = record.last_name,
                email = record.email,
                phone = record.phone,
                address = record.address,
                city = record.city,
                state = record.state,
                postcode = record.postcode,)
    #if form.is_valid():
    #    print('INSIDE THE VALID FUNCTION-----------')
    #    form.save()
    #    print('FORM HAS BEEN SAVED SUCCESSFULLY--------------------------------------')
    
    record.delete()
    return redirect('home')

def add_record(request):
    form = AddRecordForm(request.POST or None)
    if request.method == 'POST':
        if form.is_valid:
            form.save()
            messages.success(request, 'Customer record added successfully...')
            return redirect('home')
        
        return render(request, 'add_record.html', {'form':form})
    else:
        return render(request, 'add_record.html', {'form':form})
    
def display_deleted_records(request):
    records = CustomerDeletedRecords.objects.all()
    return render(request, 'display_deleted_records.html', {'records':records})