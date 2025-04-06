from django.shortcuts import render

# Create your views here.


from .models import *
from .forms import *
from django.contrib.auth.decorators import login_required

from django.shortcuts import render, redirect
from django.urls import reverse
from django.http.response import HttpResponseRedirect
from doctor.models import *



from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger





@login_required(login_url='login')
def add_doctor(request):

    if request.method == 'POST':

        forms = doctor_Form(request.POST, request.FILES)

        if forms.is_valid():
            forms.save()
            return redirect('list_doctor')
        else:
            print(forms.errors)
            context = {
                'form': forms
            }
            return render(request, 'add_doctor.html', context)
    
    else:

        forms = doctor_Form()

        context = {
            'form': forms
        }
        return render(request, 'add_doctor.html', context)


from django.views.decorators.csrf import csrf_exempt

@login_required(login_url='login')
@csrf_exempt 
def add_doctor_json(request):

    if request.method == 'POST':
        form = doctor_Form(request.POST, request.FILES)
        
        if form.is_valid():
            form.save()
            return JsonResponse({'status': 'success', 'message': 'Doctor added successfully'}, status=201)
        else:
            return JsonResponse({'status': 'error', 'errors': form.errors}, status=400)
    
    return JsonResponse({'status': 'error', 'message': 'Invalid request method'}, status=405)

        

@login_required(login_url='login')
def update_doctor(request, doctor_id):

    if request.method == 'POST':

        instance = doctor.objects.get(id=doctor_id)

        print('-------------------')
        print('-------------------')
        print('-------------------')
        print(instance.user)

        updated_request = request.POST.copy()
        updated_request.update({'user': instance.user})

        forms = doctor_Form(updated_request, request.FILES, instance=instance)

        print(forms.instance.user)

        if forms.is_valid():
            forms.save()
            return redirect('list_doctor')
        else:
            print(forms.errors)
    
    else:

        instance = doctor.objects.get(id=doctor_id)
        forms = doctor_Form(instance=instance)

        context = {
            'form': forms
        }
        return render(request, 'add_doctor.html', context)

        

@login_required(login_url='login')
def delete_doctor(request, doctor_id):

    doctor.objects.get(id=doctor_id).delete()

    return HttpResponseRedirect(reverse('list_doctor'))


@login_required(login_url='login')
def list_doctor(request):

    data = doctor.objects.all()
    context = {
        'data': data
    }
    return render(request, 'list_doctor.html', context)


from django.http import JsonResponse

def get_doctor(request):

    data = list(doctor.objects.values())  # ✅ Converts QuerySet to a list of dictionaries
    return JsonResponse({'data': data})



@login_required(login_url='login')
def list_doctor(request):

    data = doctor.objects.all()
    context = {
        'data': data
    }
    return render(request, 'list_doctor.html', context)


@login_required(login_url='login')
def add_coupon(request):

    if request.method == 'POST':

        forms = coupon_Form(request.POST, request.FILES)

        if forms.is_valid():
            forms.save()
            return redirect('list_coupon')
        else:
            print(forms.errors)
            context = {
                'form': forms
            }
            return render(request, 'add_coupon.html', context)
    
    else:

        forms = coupon_Form()

        context = {
            'form': forms
        }
        return render(request, 'add_coupon.html', context)

        

@login_required(login_url='login')
def update_coupon(request, coupon_id):

    if request.method == 'POST':

        instance = coupon.objects.get(id=coupon_id)

        forms = coupon_Form(request.POST, request.FILES, instance=instance)

        if forms.is_valid():
            forms.save()
            return redirect('list_coupon')
        else:
            print(forms.errors)
    
    else:

        instance = coupon.objects.get(id=coupon_id)
        forms = coupon_Form(instance=instance)

        context = {
            'form': forms
        }
        return render(request, 'add_coupon.html', context)

        

@login_required(login_url='login')
def delete_coupon(request, coupon_id):

    coupon.objects.get(id=coupon_id).delete()

    return HttpResponseRedirect(reverse('list_coupon'))


@login_required(login_url='login')
def list_coupon(request):

    data = coupon.objects.all()
    context = {
        'data': data
    }
    return render(request, 'list_coupon.html', context)


from django.http import JsonResponse

def get_coupon(request):

    data = list(coupon.objects.values())  # ✅ Converts QuerySet to a list of dictionaries
    return JsonResponse({'data': data})





def add_testimonials(request):
    
    if request.method == "POST":

        description = request.POST.get('description')
        name = request.POST.get('name')

        print(description)
        print(name)

        instance = testimonials.objects.create(description = description, name = name)
        instance.save()

        return redirect('list_testimonials')
    
    else:

        # create first row using admin then editing only

        

        return render(request, 'add_testimonials.html', { 'form' : testimonials_Form()})

def update_testimonials(request, testimonials_id):
    
    instance = testimonials.objects.get(id = testimonials_id)

    if request.method == "POST":

        description = request.POST.get('description')
        name = request.POST.get('name')

        print(description)
        print(name)

        instance.description = description
        instance.name = name
        instance.save()

        return redirect('list_testimonials')
    
    else:

        # create first row using admin then editing only

        

        return render(request, 'add_testimonials.html', {'data' : instance})


def list_testimonials(request):

    data = testimonials.objects.all()

    return render(request, 'list_testimonials.html', {'data' : data})


def delete_testimonials(request, testimonials_id):

    data = testimonials.objects.get(id = testimonials_id).delete()

    return redirect('list_testimonials')


from django.views import View


def get_testimonials(request):
  
    data = testimonials.objects.all()  # Assuming Testimonials is the model name

    if not data.exists():
        return JsonResponse({"error": "No data found"}, status=404)

    response_data = []
    for testimonial in data:
        temp = {
            "id": testimonial.id,
            "name": testimonial.name,
            "rating": testimonial.rating,
            "created_at": testimonial.created_at,
            "description": testimonial.description,
        }
        response_data.append(temp)

    return JsonResponse({"data": response_data}, status=200)

def get_amenity (request):
  
    data = amenity.objects.all()  # Assuming amenity  is the model name

    if not data.exists():
        return JsonResponse({"error": "No data found"}, status=404)

    response_data = []
    for i in data:
        temp = {
            "id": i.id,
            "name": i.name,
        }
        response_data.append(temp)

    return JsonResponse({"data": response_data}, status=200)

def get_symptom  (request):
  
    data = symptom.objects.all()  # Assuming symptom   is the model name

    if not data.exists():
        return JsonResponse({"error": "No data found"}, status=404)

    response_data = []
    for i in data:
        temp = {
            "id": i.id,
            "name": i.name,
            "image": i.image.url,
        }
        response_data.append(temp)

    return JsonResponse({"data": response_data}, status=200)

def get_service_category(request):
  
    data = service_category.objects.all()  # Assuming services_category   is the model name

    if not data.exists():
        return JsonResponse({"error": "No data found"}, status=404)

    response_data = []
    for i in data:
        temp = {
            "id": i.id,
            "name": i.name,
            "description": i.description,
        }
        response_data.append(temp)

    return JsonResponse({"data": response_data}, status=200)

def get_service_subcategory(request):
  
    data = service_subcategory.objects.all()  # Assuming service_subcategory   is the model name

    if not data.exists():
        return JsonResponse({"error": "No data found"}, status=404)

    response_data = []
    for i in data:
        temp = {
            "id": i.id,
            "name": i.name,
            "description": i.description,

        }
        response_data.append(temp)

    return JsonResponse({"data": response_data}, status=200)
