
# Create your views here.
from django.shortcuts import render
from django.http import HttpRequest, HttpResponse
import random

quotes_list =["My library is an archive of longings",
         "Attention is vitality. It connects you with others. It makes you eager. Stay eager", 
         "To paraphrase several sages: Nobody can think and hit someone at the same time",
         ]

images = ['https://cs-webapps.bu.edu/meeram/static/image1.jpg', 'https://cs-webapps.bu.edu/meeram/static/image2.webp', 'https://cs-webapps.bu.edu/meeram/static/image3.webp']

def quote(request):
  template_name = 'quotes/quote.html'
  rand_index = random.randint(0,2)
  display_quote = quotes_list[rand_index]
  diplay_image= images[rand_index]

  context = {
        'quote': display_quote,
        'image' : diplay_image,
    }

  return render(request, template_name, context)

def show_all(request):
  template_name = 'quotes/show_all.html'

  context = {
    'images': images,
    'quotes_list': quotes_list,
  }

  print(context)
  return render(request, template_name, context)

def base(request):
  template_name = 'quotes/base.html'

  return render(request, template_name)

def about(request):
  template_name = 'quotes/about.html'
  context = {
    'welcome': "Welcome",
    'string_one': "This application displays the quotes of the author Susan Sontag.",
    'string_two': "Susan Lee Sontag was a writer, essayist, critic, and public intellectual. She is known for her essays like On Photagraphy and Notes On Camp."
  }
  return render(request, template_name, context)
