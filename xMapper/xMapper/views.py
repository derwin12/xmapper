from django.shortcuts import render
from django.http import HttpResponse

def process_data():
    """Stub function that simulates processing."""
    ret = read_source()
    return ret

def read_source():
    return "yes"

def home(request):
    if request.method == "POST":
        result = process_data()  # Call the stub function
        return render(request, "result.html", {"result": result})  # Pass result to template

    return render(request, "home.html")  # Show initial page
