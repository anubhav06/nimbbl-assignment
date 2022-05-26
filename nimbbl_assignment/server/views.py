from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from .models import User, Product

import requests
from decouple import config

import string
import random

# Index view
def index(request):

    products = Product.objects.all()

    return render(request, "server/index.html", {
        "products": products,
    })


# To create an order
def createOrder(request, id):

    if request.method == "POST":
        
        name = Product.objects.get(id = id).name
        price = Product.objects.get(id = id).price

        print ("name: ", name)
        print ("price: ", price)

        # To generate token
        url = "https://api.nimbbl.tech/api/v2/generate-token"

        access_key = config('ACCESS_KEY')
        access_secret = config('ACCESS_SECRET')

        payload="{\n    \"access_key\": \"" + access_key + "\",\n    \"access_secret\": \"" + access_secret + "\"\n}\n"

        headers = {
            'Content-Type': 'application/json'
        }

        response = requests.request("POST", url, headers=headers, data=payload)
        token = response.json()['token']
        
        # To create an order
        orderURL = "https://api.nimbbl.tech/api/v2/create-order"

        #payload= {
        #    "amount_before_tax": 4,
        #    "currency": "INR",
        #    "invoice_id": "hdaiasdha",
        #    "device_user_agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.128 Safari/537.36",
        #    "order_from_ip": "x.x.x.x",
        #    "tax": 0,
        #    "user": {
        #            "mobile_number": "9999999999",
        #            "email":"rakesh.kumar@example.com",
        #            "first_name":"Rakesh",
        #            "last_name":"Kumar"    
        #        },
        #    "shipping_address": {
        #        "address_1":"Some address",
        #        "street":"Your street",
        #        "landmark":"My landmark",
        #        "area":"My area",
        #        "city":"Mumbai",
        #        "state":"Maharashtra",
        #        "pincode":"400018",
        #        "address_type":"residential"},
        #        "total_amount": 4,
        #        "order_line_items": [{
        #            "referrer_platform_sku_id":"sku1",
        #            "title":"Designer Triangles",
        #            "description":"Wallpaper by  chenspec from Pixabay",
        #            "quantity": 1,
        #            "rate": 4,
        #            "amount": 4,
        #            "total_amount": 4,
        #            "image_url":"https://cdn.pixabay.com/photo/2021/02/15/15/25/rhomboid-6018215_960_720.jpg"
        #        }]
        #}
        
        invoiceID = ''.join(random.choice(string.ascii_uppercase + string.ascii_lowercase + string.digits) for _ in range(16))

        payload="{\"amount_before_tax\":" + str(price) + ",\"currency\":\"INR\",\"invoice_id\":\""+ invoiceID +"\",\"device_user_agent\": \"Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.128 Safari/537.36\",\"order_from_ip\": \"x.x.x.x\",\"tax\": 0,\"user\": {\"mobile_number\":\"9999999999\",\"email\":\"rakesh.kumar@example.com\",\"first_name\":\"Rakesh\",\"last_name\":\"Kumar\"    },\"shipping_address\": {\"address_1\":\"Some address\",\"street\":\"Your street\",\"landmark\":\"My landmark\",\"area\":\"My area\",\"city\":\"Mumbai\",\"state\":\"Maharashtra\",\"pincode\":\"400018\",\"address_type\":\"residential\"},\"total_amount\": 4,\"order_line_items\": [{\"referrer_platform_sku_id\":\"sku1\",\"title\":\"Designer Triangles\",\"description\":\"Wallpaper by  chenspec from Pixabay\",\"quantity\": 1,\"rate\": 4,\"amount\": 4,\"total_amount\": 4,\"image_url\":\"https:\/\/cdn.pixabay.com\/photo\/2021\/02\/15\/15\/25\/rhomboid-6018215_960_720.jpg\"}]}"
        
        headers = {
            'Authorization': 'Bearer ' + str(token),
            'Content-Type': 'application/json'
        }

        response = requests.request("POST", orderURL, headers=headers, data=payload)

        order_id = response.json()['order_id']

        return render(request, 'server/checkout.html', {
            "order_id": order_id,
            "access_key": access_key
        })

    return HttpResponse('GET method not allowed')



def login_view(request):
    if request.method == "POST":

        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "server/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "server/login.html")


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))


def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "server/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "server/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "server/register.html")
