from django.shortcuts import render,redirect
from EauthApp.models import Product
from math import ceil
from django.contrib import messages
# from PayTm import Checksum
from Eapp.models import Orders,OrderUpdate
from django.views.decorators.csrf import csrf_exempt
import json
from django.http import HttpResponse



# Create your views here.
def home(request):
    return render(request,'index.html')

def tracker(request):
    if not request.user.is_authenticated:
        messages.warning(request,"Login & Try Again")
        return redirect('/EauthApp/login')
    if request.method=="POST":
        orderId = request.POST.get('orderId', '')
        email = request.POST.get('email', '')
        try:
            order = Orders.objects.filter(order_id=orderId, email=email)
            if len(order)>0:
                update = OrderUpdate.objects.filter(order_id=orderId)
                updates = []
                for item in update:
                    updates.append({'text': item.update_desc, 'time': item.timestamp})
                    response = json.dumps([updates, order[0].items_json], default=str)
                return HttpResponse(response)
            else:
                return HttpResponse('{no orders}')
        except Exception as e:
            return HttpResponse('{}')

    return render(request, 'tracker.html')


def purchase(request):
    allProds = []
    catprods = Product.objects.values('category','id')
    cats = {item['category'] for item in catprods}
    for cat in cats:
        prod= Product.objects.filter(category=cat)
        n=len(prod)
        nSlides = n // 4 + ceil((n / 4) - (n // 4))
        allProds.append([prod, range(1, nSlides), nSlides])

    params= {'allProds':allProds}
    return render(request,'purchase.html',params)

def checkout(request):
    if not request.user.is_authenticated:
        messages.warning(request, "Login & Try Again")
        return redirect('/EauthApp/login')
    
    if request.method == "POST":
        items_json = request.POST.get('itemsJson', '')
        name = request.POST.get('name', '')
        amount = request.POST.get('amt')
        email = request.POST.get('email', '')
        address1 = request.POST.get('address1', '')
        address2 = request.POST.get('address2', '')
        city = request.POST.get('city', '')
        state = request.POST.get('state', '')
        zip_code = request.POST.get('zip_code', '')
        phone = request.POST.get('phone', '')

        # Save the order in the database
        order = Orders.objects.create(
            items_json=items_json,
            name=name,
            amount=amount,
            email=email,
            address1=address1,
            address2=address2,
            city=city,
            state=state,
            zip_code=zip_code,
            phone=phone
        )

        # Optionally, you can save an order update
        OrderUpdate.objects.create(order_id=order.order_id, update_desc="the order has been placed")

        # Simulate a response dictionary for demonstration
        response = {
            "ORDERID": order.order_id,
            "RESPCODE": "01"  # Assuming the payment is successful
        }

        # Pass the response variable to the template
        return render(request, 'thank_you.html', {'response': response})
    
    return render(request, 'checkout.html')

def about(request):
    return render(request, 'about.html')

def services(request):
    return render(request, 'services.html')

def portfolio_details(request):
    return render(request, 'portfolio-details.html')

def Privacy_Policy(request):
    return render(request, 'Privacy_Policy.html')

def Termofuse(request):
    return render(request, 'Termofuse.html')

# views.py
from django.shortcuts import render
from .forms import ContactForm
from Eapp.models import ContactMessage

def receive_message(request):
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            name = form.cleaned_data['name']
            email = form.cleaned_data['email']
            message = form.cleaned_data['message']
            # Create an instance of ContactMessage model and save it
            contact_message = ContactMessage(name=name, email=email, message=message)
            contact_message.save()
            # Render the success page
            return render(request, 'success.html')
    else:
        form = ContactForm()
    return render(request, 'form.html', {'form': form})
