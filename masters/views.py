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

        forms = testimonials_Form(request.POST, request.FILES)

        if forms.is_valid():
            forms.save()
            return redirect('list_testimonials')
        else:
            print(forms.errors)
            context = {
                'form': forms
            }
            return render(request, 'add_testimonials.html', context)
    
    else:

        # create first row using admin then editing only

        

        return render(request, 'add_testimonials.html', { 'form' : testimonials_Form()})

def update_testimonials(request, testimonials_id):
    
    instance = testimonials.objects.get(id = testimonials_id)

    if request.method == "POST":

        forms = testimonials_Form(request.POST, request.FILES, instance=instance)

        if forms.is_valid():
            forms.save()
            return redirect('list_testimonials')
        else:
            print(forms.errors)
            context = {
                'form': forms
            }
            return render(request, 'add_testimonials.html', context)

    
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




def add_amenity(request):
    
    if request.method == "POST":

        forms = amenity_Form(request.POST, request.FILES)

        if forms.is_valid():
            forms.save()
            return redirect('list_amenity')
        else:
            print(forms.errors)
            context = {
                'form': forms
            }
            return render(request, 'add_amenity.html', context)


    else:

        # create first row using admin then editing only

        

        return render(request, 'add_amenity.html', { 'form' : amenity_Form()})

def update_amenity(request, amenity_id):
    
    instance = amenity.objects.get(id = amenity_id)

    if request.method == "POST":

        forms = amenity_Form(request.POST, request.FILES, instance=instance)

        if forms.is_valid():
            forms.save()
            return redirect('list_amenity')
        else:
            print(forms.errors)
            context = {
                'form': forms
            }
            return render(request, 'add_amenity.html', context)
    
    else:

        # create first row using admin then editing only

        

        return render(request, 'add_amenity.html', {'data' : instance})


def list_amenity(request):

    data = amenity.objects.all()

    return render(request, 'list_amenity.html', {'data' : data})


def delete_amenity(request, amenity_id):

    data = amenity.objects.get(id = amenity_id).delete()

    return redirect('list_amenity')


from django.views import View


def get_amenity (request):
  
    data = list(amenity.objects.values())  # ✅ Converts QuerySet to a list of dictionaries
    return JsonResponse({'data': data})





def add_symptom(request):
    
    if request.method == "POST":

        forms = symptom_Form(request.POST, request.FILES)

        if forms.is_valid():
            forms.save()
            return redirect('list_symptom')
        else:
            print(forms.errors)
            context = {
                'form': forms
            }
            return render(request, 'add_symptom.html', context)


    else:

        # create first row using admin then editing only

        

        return render(request, 'add_symptom.html', { 'form' : symptom_Form()})

def update_symptom(request, symptom_id):
    
    instance = symptom.objects.get(id = symptom_id)

    if request.method == "POST":

        forms = symptom_Form(request.POST, request.FILES, instance=instance)

        if forms.is_valid():
            forms.save()
            return redirect('list_symptom')
        else:
            print(forms.errors)
            context = {
                'form': forms
            }
            return render(request, 'add_symptom.html', context)
    
    else:

        # create first row using admin then editing only

        

        return render(request, 'add_symptom.html', {'data' : instance})


def list_symptom(request):

    data = symptom.objects.all()

    return render(request, 'list_symptom.html', {'data' : data})


def delete_symptom(request, symptom_id):

    data = symptom.objects.get(id = symptom_id).delete()

    return redirect('list_symptom')


def get_symptom(request):
  
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




def add_service_category(request):
    
    if request.method == "POST":

        forms = service_category_Form(request.POST, request.FILES)

        if forms.is_valid():
            forms.save()
            return redirect('list_service_category')
        else:
            print(forms.errors)
            context = {
                'form': forms
            }
            return render(request, 'add_services_category.html', context)
    
    else:

        # create first row using admin then editing only

        

        return render(request, 'add_services_category.html', { 'form' : service_category_Form()})

def update_service_category(request, service_category_id):
    
    instance = service_category.objects.get(id = service_category_id)

    if request.method == "POST":

        forms = service_category_Form(request.POST, request.FILES, instance=instance)

        if forms.is_valid():
            forms.save()
            return redirect('list_service_category')
        else:
            print(forms.errors)
            context = {
                'form': forms
            }
            return render(request, 'add_services_category.html', context)

    
    else:

        # create first row using admin then editing only

        

        return render(request, 'add_services_category.html', {'data' : instance})


def list_service_category(request):

    data = service_category.objects.all()

    return render(request, 'list_services_category.html', {'data' : data})


def delete_service_category(request, service_category_id):

    data = service_category.objects.get(id = service_category_id).delete()

    return redirect('list_service_category')


def get_service_category(request):
  
    data = list(service_category.objects.values())  # ✅ Converts QuerySet to a list of dictionaries
    return JsonResponse({'data': data})





def add_service_subcategory(request):
    
    if request.method == "POST":

        forms = service_subcategory_Form(request.POST, request.FILES)

        if forms.is_valid():
            forms.save()
            return redirect('list_service_subcategory')
        else:
            print(forms.errors)
            context = {
                'form': forms
            }
            return render(request, 'add_services_subcategory.html', context)
    
    else:

        # create first row using admin then editing only

        

        return render(request, 'add_services_subcategory.html', { 'form' : service_subcategory_Form()})

def update_service_subcategory(request, service_subcategory_id):
    
    instance = service_subcategory.objects.get(id = service_subcategory_id)

    if request.method == "POST":

        forms = service_subcategory_Form(request.POST, request.FILES, instance=instance)

        if forms.is_valid():
            forms.save()
            return redirect('list_services_subcategory')
        else:
            print(forms.errors)
            context = {
                'form': forms
            }
            return render(request, 'add_services_subcategory.html', context)

    
    else:

        # create first row using admin then editing only

        

        return render(request, 'add_services_subcategory.html', {'data' : instance})


def list_service_subcategory(request):

    data = service_subcategory.objects.all()

    return render(request, 'list_services_subcategory.html', {'data' : data})


def delete_service_subcategory(request, service_subcategory_id):

    data = service_subcategory.objects.get(id = service_subcategory_id).delete()

    return redirect('list_service_subcategory')


def get_service_subcategory(request):
  
    data = list(service_subcategory.objects.values())  # ✅ Converts QuerySet to a list of dictionaries
    return JsonResponse({'data': data})



def add_service(request):
    
    if request.method == "POST":

        forms = service_Form(request.POST, request.FILES)

        if forms.is_valid():
            forms.save()
            return redirect('list_service')
        else:
            print(forms.errors)
            context = {
                'form': forms
            }
            return render(request, 'add_services.html', context)
    
    else:

        # create first row using admin then editing only

        

        return render(request, 'add_services.html', { 'form' : service_Form()})

def update_service(request, service_id):
    
    instance = service.objects.get(id = service_id)

    if request.method == "POST":

        forms = service_Form(request.POST, request.FILES, instance=instance)

        if forms.is_valid():
            forms.save()
            return redirect('list_service')
        else:
            print(forms.errors)
            context = {
                'form': forms
            }
            return render(request, 'add_services.html', context)

    
    else:

        # create first row using admin then editing only

        

        return render(request, 'add_services.html', {'data' : instance})


def list_service(request):

    data = service.objects.all()

    return render(request, 'list_services.html', {'data' : data})


def delete_service(request, service_id):

    data = service.objects.get(id = service_id).delete()

    return redirect('list_service')


def get_service(request):
  
    data = list(service.objects.values())  # ✅ Converts QuerySet to a list of dictionaries
    return JsonResponse({'data': data})




@login_required(login_url='login')
def add_test(request):

    if request.method == 'POST':

        forms = test_Form(request.POST, request.FILES)

        if forms.is_valid():
            forms.save()
            return redirect('list_test')
        else:
            print(forms.errors)
            context = {
                'form': forms
            }
            return render(request, 'add_test.html', context)
    
    else:

        forms = test_Form()

        context = {
            'form': forms
        }
        return render(request, 'add_test.html', context)

        

@login_required(login_url='login')
def update_test(request, test_id):

    if request.method == 'POST':

        instance = test.objects.get(id=test_id)

        forms = test_Form(request.POST, request.FILES, instance=instance)

        if forms.is_valid():
            forms.save()
            return redirect('list_test')
        else:
            print(forms.errors)
    
    else:

        instance = test.objects.get(id=test_id)
        forms = test_Form(instance=instance)

        context = {
            'form': forms
        }
        return render(request, 'add_test.html', context)

        

@login_required(login_url='login')
def delete_test(request, test_id):

    test.objects.get(id=test_id).delete()

    return HttpResponseRedirect(reverse('list_test'))


@login_required(login_url='login')
def list_test(request):

    data = test.objects.all()
    context = {
        'data': data
    }
    return render(request, 'list_test.html', context)


from django.http import JsonResponse

def get_test(request):

    data = list(test.objects.values())  # ✅ Converts QuerySet to a list of dictionaries
    return JsonResponse({'data': data})


@login_required(login_url='login')
def add_dog_breed(request):

    if request.method == 'POST':

        forms = dog_breed_Form(request.POST, request.FILES)

        if forms.is_valid():
            forms.save()
            return redirect('list_dog_breed')
        else:
            print(forms.errors)
            context = {
                'form': forms
            }
            return render(request, 'add_dog_breed.html', context)
    
    else:

        forms = dog_breed_Form()

        context = {
            'form': forms
        }
        return render(request, 'add_dog_breed.html', context)

        

@login_required(login_url='login')
def update_dog_breed(request, dog_breed_id):

    if request.method == 'POST':

        instance = dog_breed.objects.get(id=dog_breed_id)

        forms = dog_breed_Form(request.POST, request.FILES, instance=instance)

        if forms.is_valid():
            forms.save()
            return redirect('list_dog_breed')
        else:
            print(forms.errors)
    
    else:

        instance = dog_breed.objects.get(id=dog_breed_id)
        forms = dog_breed_Form(instance=instance)

        context = {
            'form': forms
        }
        return render(request, 'add_dog_breed.html', context)

        

@login_required(login_url='login')
def delete_dog_breed(request, dog_breed_id):

    dog_breed.objects.get(id=dog_breed_id).delete()

    return HttpResponseRedirect(reverse('list_dog_breed'))


@login_required(login_url='login')
def list_dog_breed(request):

    data = dog_breed.objects.all()
    context = {
        'data': data
    }
    return render(request, 'list_dog_breed.html', context)


from django.http import JsonResponse

def get_dog_breed(request):

    data = list(dog_breed.objects.values())  # ✅ Converts QuerySet to a list of dictionaries
    return JsonResponse({'data': data})


@login_required(login_url='login')
def add_product(request):

    if request.method == 'POST':

        forms = product_Form(request.POST, request.FILES)

        if forms.is_valid():
            forms.save()
            return redirect('list_product')
        else:
            print(forms.errors)
            context = {
                'form': forms
            }
            return render(request, 'add_product.html', context)
    
    else:

        forms = product_Form()

        context = {
            'form': forms
        }
        return render(request, 'add_product.html', context)

        

@login_required(login_url='login')
def update_product(request, product_id):

    if request.method == 'POST':

        instance = product.objects.get(id=product_id)

        forms = product_Form(request.POST, request.FILES, instance=instance)

        if forms.is_valid():
            forms.save()
            return redirect('list_product')
        else:
            print(forms.errors)
    
    else:

        instance = product.objects.get(id=product_id)
        forms = product_Form(instance=instance)

        context = {
            'form': forms
        }
        return render(request, 'add_product.html', context)

        

@login_required(login_url='login')
def delete_product(request, product_id):

    product.objects.get(id=product_id).delete()

    return HttpResponseRedirect(reverse('list_product'))


@login_required(login_url='login')
def list_product(request):

    data = product.objects.all()
    context = {
        'data': data
    }
    return render(request, 'list_product.html', context)


from django.http import JsonResponse

def get_product(request):

    data = list(product.objects.values())  # ✅ Converts QuerySet to a list of dictionaries
    return JsonResponse({'data': data})


@login_required(login_url='login')
def add_vaccination(request):

    if request.method == 'POST':

        forms = vaccination_Form(request.POST, request.FILES)

        if forms.is_valid():
            forms.save()
            return redirect('list_vaccination')
        else:
            print(forms.errors)
            context = {
                'form': forms
            }
            return render(request, 'add_vaccination.html', context)
    
    else:

        forms = vaccination_Form()

        context = {
            'form': forms
        }
        return render(request, 'add_vaccination.html', context)

        

@login_required(login_url='login')
def update_vaccination(request, vaccination_id):

    if request.method == 'POST':

        instance = vaccination.objects.get(id=vaccination_id)

        forms = vaccination_Form(request.POST, request.FILES, instance=instance)

        if forms.is_valid():
            forms.save()
            return redirect('list_vaccination')
        else:
            print(forms.errors)
    
    else:

        instance = vaccination.objects.get(id=vaccination_id)
        forms = vaccination_Form(instance=instance)

        context = {
            'form': forms
        }
        return render(request, 'add_vaccination.html', context)

        

@login_required(login_url='login')
def delete_vaccination(request, vaccination_id):

    vaccination.objects.get(id=vaccination_id).delete()

    return HttpResponseRedirect(reverse('list_vaccination'))


@login_required(login_url='login')
def list_vaccination(request):

    data = vaccination.objects.all()

    print(data)

    
    context = {
        'data': data
    }
    return render(request, 'list_vaccination.html', context)


from django.http import JsonResponse

def get_vaccination(request):

    data = list(vaccination.objects.values())  # ✅ Converts QuerySet to a list of dictionaries
    return JsonResponse({'data': data})

