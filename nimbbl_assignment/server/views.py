from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from .models import User

import requests

# Index view
def index(request):
    return render(request, "server/index.html")


# To create an order
def createOrder(request):

    if request.method == "POST":
        print('REQUEST: ', request)
        content = request.POST["heading"]
        print('CONTENT: ', content)
        return HttpResponseRedirect(reverse('index'))
    
    
    #url = "https://api.nimbbl.tech/api/v2/create-order"

    #payload="{\"amount_before_tax\": 4,\"currency\":\"INR\",\"invoice_id\":\"BrQv9nkxDEqWR3zg\",\"device_user_agent\": \"Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.128 Safari/537.36\",\"order_from_ip\": \"x.x.x.x\",\"tax\": 0,\"user\": {\"mobile_number\":\"9999999999\",\"email\":\"rakesh.kumar@example.com\",\"first_name\":\"Rakesh\",\"last_name\":\"Kumar\"    },\"shipping_address\": {\"address_1\":\"Some address\",\"street\":\"Your street\",\"landmark\":\"My landmark\",\"area\":\"My area\",\"city\":\"Mumbai\",\"state\":\"Maharashtra\",\"pincode\":\"400018\",\"address_type\":\"residential\"},\"total_amount\": 4,\"order_line_items\": [{\"referrer_platform_sku_id\":\"sku1\",\"title\":\"Designer Triangles\",\"description\":\"Wallpaper by  chenspec from Pixabay\",\"quantity\": 1,\"rate\": 4,\"amount\": 4,\"total_amount\": 4,\"image_url\":\"https:\/\/cdn.pixabay.com\/photo\/2021\/02\/15\/15\/25\/rhomboid-6018215_960_720.jpg\"}]}"
    #headers = {
    #    'Authorization': 'Bearer <token>',
    #    'Content-Type': 'application/json'
    #}

    #response = requests.request("POST", url, headers=headers, data=payload)

    #print(response.text)

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
