from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect, HttpResponsePermanentRedirect

def products(request, productid):
    category = request.GET.get("ctg", "None")
    output = "<h2>Product № {0}  Category: {1}</h2>".format(productid, category)
    return HttpResponse(output)
 
def users(request):
    id = request.GET.get("id", 1)
    name = request.GET.get("name", "Tom")
    output = "<h2>User</h2><h3>id: {0}  name: {1}</h3>".format(id, name)
    return HttpResponse(output)

def home(request):
    header = "Personal Data"                    # обычная переменная
    langs = ["English", "German", "Spanish"]    # массив
    user ={"name" : "Tom", "age" : 23}          # словарь
    addr = ("Абрикосовая", 23, 45)              # кортеж
 
    data = {"header": header, "langs": langs, "user": user, "address": addr}
    return render(request, "main_window/home.html", context=data)