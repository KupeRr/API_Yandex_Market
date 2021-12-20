from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect, HttpResponsePermanentRedirect

from .forms import UserForm

def products(request, productid):
    category = request.GET.get("ctg", "None")
    output = "<h2>Product № {0}  Category: {1}</h2>".format(productid, category)
    return HttpResponse(output)
 
def users(request):
    id = request.GET.get("id", 1)
    name = request.GET.get("name", "Tom")
    output = "<h2>User</h2><h3>id: {0}  name: {1}</h2>".format(id, name)
    return HttpResponse(output)

def home(request):
    header = "Personal Data"                    # обычная переменная
    langs = ["English", "German", "Spanish"]    # массив
    user ={"name" : "Tom", "age" : 23}          # словарь
    addr = ("Абрикосовая", 23, 45)              # кортеж
 
    data = {"header": header, "langs": langs, "user": user, "address": addr}
    return render(request, "main_window/home.html", context=data)

def user_form(request):
    if request.method == "POST":
        user_form = UserForm(request.POST)
        if user_form.is_valid():
            name = user_form.cleaned_data["name"]
            age  = user_form.cleaned_data["age"]
            return HttpResponse(f"<h2>Ur input: {name} and {age}</h2>")
        else:
            return HttpResponse("Invalid data")
    else:
        user_form = UserForm()
        return render(request, "user_form.html", {"form":user_form})