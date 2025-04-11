from django.shortcuts import render

from masters.filters import EventFilter

# Create your views here.


from .models import *
from .forms import *
from django.contrib.auth.decorators import login_required

from django.shortcuts import render, redirect
from django.urls import reverse
from django.http.response import HttpResponseRedirect
from doctor.models import *
from .serializers import *


from rest_framework.generics import ListAPIView
from django_filters.rest_framework import DjangoFilterBackend

from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger





# @login_required(login_url='login')
# def add_doctor(request):

#     if request.method == 'POST':

#         forms = doctor_Form(request.POST, request.FILES)

#         if forms.is_valid():
#             forms.save()
#             return redirect('list_doctor')
#         else:
#             print(forms.errors)
#             context = {
#                 'form': forms
#             }
#             return render(request, 'add_doctor.html', context)
    
#     else:

#         forms = doctor_Form()

#         context = {
#             'form': forms
#         }
#         return render(request, 'add_doctor.html', context)


# from django.views.decorators.csrf import csrf_exempt

# @login_required(login_url='login')
# @csrf_exempt 
# def add_doctor_json(request):

#     if request.method == 'POST':
#         form = doctor_Form(request.POST, request.FILES)
        
#         if form.is_valid():
#             form.save()
#             return JsonResponse({'status': 'success', 'message': 'Doctor added successfully'}, status=201)
#         else:
#             return JsonResponse({'status': 'error', 'errors': form.errors}, status=400)
    
#     return JsonResponse({'status': 'error', 'message': 'Invalid request method'}, status=405)

        

# @login_required(login_url='login')
# def update_doctor(request, doctor_id):

#     if request.method == 'POST':

#         instance = doctor.objects.get(id=doctor_id)

#         print('-------------------')
#         print('-------------------')
#         print('-------------------')
#         print(instance.user)

#         updated_request = request.POST.copy()
#         updated_request.update({'user': instance.user})

#         forms = doctor_Form(updated_request, request.FILES, instance=instance)

#         print(forms.instance.user)

#         if forms.is_valid():
#             forms.save()
#             return redirect('list_doctor')
#         else:
#             print(forms.errors)
    
#     else:

#         instance = doctor.objects.get(id=doctor_id)
#         forms = doctor_Form(instance=instance)

#         context = {
#             'form': forms
#         }
#         return render(request, 'add_doctor.html', context)

        

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
from .filters import *

class get_coupon(ListAPIView):
    queryset = coupon.objects.all()
    serializer_class = coupon_serializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = '__all__'  # enables filtering on all fields
    filterset_class = couponFilter  # enables filtering on all fields



@login_required(login_url='login')
def add_event(request):

    if request.method == 'POST':

        forms = event_Form(request.POST, request.FILES)

        if forms.is_valid():
            forms.save()
            return redirect('list_event')
        else:
            print(forms.errors)
            context = {
                'form': forms
            }
            return render(request, 'add_event.html', context)
    
    else:

        forms = event_Form()

        context = {
            'form': forms
        }
        return render(request, 'add_event.html', context)

        

@login_required(login_url='login')
def update_event(request, event_id):

    if request.method == 'POST':

        instance = event.objects.get(id=event_id)

        forms = event_Form(request.POST, request.FILES, instance=instance)

        if forms.is_valid():
            forms.save()
            return redirect('list_event')
        else:
            print(forms.errors)
    
    else:

        instance = event.objects.get(id=event_id)
        forms = event_Form(instance=instance)

        context = {
            'form': forms
        }
        return render(request, 'add_event.html', context)

        

@login_required(login_url='login')
def delete_event(request, event_id):

    event.objects.get(id=event_id).delete()

    return HttpResponseRedirect(reverse('list_event'))


@login_required(login_url='login')
def list_event(request):

    data = event.objects.all()
    context = {
        'data': data
    }
    return render(request, 'list_event.html', context)


from django.http import JsonResponse

class get_event(ListAPIView):
    queryset = event.objects.all()
    serializer_class = event_serializer
    filter_backends = [DjangoFilterBackend]
    filterset_class = EventFilter  # enables filtering on all fields


    def get_queryset(self):
        return event.objects.filter(start_date__gte=now()).order_by('start_date')


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


class get_testimonials(ListAPIView):
    queryset = testimonials.objects.all()
    serializer_class = testimonials_serializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = '__all__'  # enables filtering on all fields




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



class get_amenity(ListAPIView):
    queryset = amenity.objects.all()
    serializer_class = amenity_serializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = '__all__'  # enables filtering on all fields



from users.permissions import *
from rest_framework.response import Response


class add_customer_address(View):

    permission_classes = [IsCustomer]

    def get(self, request):
        serializer = customer_address_serializer()
        return render(request, 'add_customer_address.html', {'form': serializer})


    def post(self, request):
        # Detect if request is single object or list
        is_many = isinstance(request.data, list)

        serializer = customer_address_serializer(
            data=request.data,
            many=is_many,
            context={'request': request}
        )
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response({"message": "Address(es) added successfully!"})

        
        

def update_customer_address(request, customer_address_id):
    
    instance = customer_address.objects.get(id = customer_address_id)

    if request.method == "POST":

        forms = customer_address_Form(request.POST, request.FILES, instance=instance)

        if forms.is_valid():
            forms.save()
            return redirect('list_customer_address')
        else:
            print(forms.errors)
            context = {
                'form': forms
            }
            return render(request, 'add_customer_address.html', context)
    
    else:

        # create first row using admin then editing only

        

        return render(request, 'add_customer_address.html', {'data' : instance})


def list_customer_address(request):

    data = customer_address.objects.all()

    return render(request, 'list_customer_address.html', {'data' : data})


def delete_customer_address(request, customer_address_id):

    data = customer_address.objects.get(id = customer_address_id).delete()

    return redirect('list_customer_address')


from django.views import View



class get_customer_address(ListAPIView):
    queryset = customer_address.objects.all()
    serializer_class = customer_address_serializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = '__all__'  # enables filtering on all fields


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


class get_symptom(ListAPIView):
    queryset = symptom.objects.all()
    serializer_class = symptom_serializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = '__all__'  # enables filtering on all fields
    filterset_class = symptomFilter  # enables filtering on all fields




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


class get_service_category(ListAPIView):
    queryset = service_category.objects.all()
    serializer_class = service_category_serializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = '__all__'  # enables filtering on all fields



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



class get_service_subcategory(ListAPIView):
    queryset = service_subcategory.objects.all()
    serializer_class = service_subcategory_serializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = '__all__'  # enables filtering on all fields



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

        forms = service_Form(instance=instance)

        context = {
            'form': forms
        }
        return render(request, 'add_services.html', context)


def list_service(request):

    data = service.objects.all()

    return render(request, 'list_services.html', {'data' : data})


def delete_service(request, service_id):

    data = service.objects.get(id = service_id).delete()

    return redirect('list_service')


class get_service(ListAPIView):
  
    
    queryset = service.objects.all()
    serializer_class = service_serializer
    filter_backends = [DjangoFilterBackend]
    filterset_class = serviceFilter  # enables filtering on all fields


from django_filters.rest_framework import DjangoFilterBackend


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


class get_test(ListAPIView):
    queryset = test.objects.all()
    serializer_class = test_serializer
    filter_backends = [DjangoFilterBackend]
    filterset_class = testFilter  # enables filtering on all fields


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



class get_dog_breed(ListAPIView):
    queryset = dog_breed.objects.all()
    serializer_class = dog_breed_serializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = '__all__'  # enables filtering on all fields


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


class get_product(ListAPIView):
    queryset = product.objects.all()
    serializer_class = product_serializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = '__all__'  # enables filtering on all fields
    filterset_class = productFilter  # enables filtering on all fields


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


class get_vaccination(ListAPIView):
    queryset = vaccination.objects.all()
    serializer_class = vaccination_serializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = '__all__'  # enables filtering on all fields





def add_home_banner(request):
    
    if request.method == "POST":

        forms = home_banner_Form(request.POST, request.FILES)

        if forms.is_valid():
            forms.save()
            return redirect('list_home_banner')
        else:
            print(forms.errors)
            context = {
                'form': forms
            }

            return render(request, 'add_home_banner.html', context)
    
    else:

        # create first row using admin then editing only

        

        return render(request, 'add_home_banner.html', { 'form' : home_banner_Form()})

def update_home_banner(request, home_banner_id):
    
    instance = home_banner.objects.get(id = home_banner_id)

    if request.method == "POST":


        instance = home_banner.objects.get(id=home_banner_id)

        forms = home_banner_Form(request.POST, request.FILES, instance=instance)

        if forms.is_valid():
            forms.save()
            return redirect('list_home_banner')
        else:
            print(forms.errors)
            context = {
                'form': forms
            }

            return render(request, 'add_home_banner.html', context)

    
    else:

        # create first row using admin then editing only

        

        return render(request, 'add_home_banner.html', {'data' : instance})


def list_home_banner(request):

    data = home_banner.objects.all()

    return render(request, 'list_home_banner.html', {'data' : data})


def delete_home_banner(request, home_banner_id):

    data = home_banner.objects.get(id = home_banner_id).delete()

    return redirect('list_home_banner')


from django.views import View

def get_home_banner(request):
  
    data = home_banner.objects.all()  # Assuming home_banner is the model name


    serialized_data = HomeBannerSerializer(data, many=True).data  

    return JsonResponse({"data": serialized_data}, status=200, safe=False)  


