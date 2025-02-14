# Create your views here.
from django.shortcuts import render
from django.http import HttpRequest, HttpResponse
import random
import time
from datetime import datetime


daily_specials = ["Olive Bread", "Pain aux Raisin", "Ginger Molasses Cookie", "Almond Macaroon", "Boston Cream Pie", 
                  "Guava-Filled Pan Dulce", "Mille-Feuille", "Red Velvet Cake"]


def confirmation(request: HttpRequest):
  sum = 0
  template_name = 'restaurant/confirmation.html'

  current = time.time()
  add_time = random.randint(30, 60)
  t = current + add_time

  time_at = datetime.fromtimestamp(t).strftime('%A, %Y-%m-%d %H:%M:%S')
  print(request.POST)


  chosen = []
  context =  {}
  cupcake = []

  #check if post data was sent with HTTP POST message
  if request.POST:
         #name is a required field
        if('name' in request.POST):
          name = request.POST['name']
          context.update({'name': name})
        if ('croissant' in request.POST):
              chosen.append("Croissant")
              sum += 2
        if ('cake' in request.POST):
              chosen.append("Black Forest Cake")
              sum += 15
        if ('bread' in request.POST):
              chosen.append("Baguette")
              sum +=3
        if ('special' in request.POST):
            special = request.POST['special']
            chosen.append(special)
        if ('cakeSelection' in request.POST):
            cakeSelection = request.POST.getlist('cakeSelection')
            cupcake = cakeSelection
            price = len(cupcake) * 3
            sum+=price
            context.update({'cupcake': cupcake})
        if ('special_instructions' in request.POST):
            special_instructions = request.POST["special_instructions"]
            context.update({'special_instructions': special_instructions})
        if ('email' in request.POST):
            email = request.POST['email']
            context.update({'email': email})
        if ('phone' in request.POST):
            phone = request.POST['phone']
            context.update({'phone': phone})

  context.update({'chosen': chosen})
  context.update({'time': time_at})
  context.update({'sum': sum})

  if request.GET:
    print("render something else")

  return render(request, template_name=template_name, context=context)




def order(request):
  template_name = 'restaurant/order.html'
  index = random.randint(0,7)
  day = daily_specials[index]

  context = {"special" : day}

  return render(request, template_name, context=context)




def main(request):
  template_name = 'restaurant/main.html'

  return render(request, template_name)