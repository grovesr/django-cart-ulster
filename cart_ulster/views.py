from django.shortcuts import render

def home(request):
    return render(request,'base/base.html',{'nav_home':1})

def cart_help(request):
    return render(request,'base/cart_help.html',{'nav_help':1})
