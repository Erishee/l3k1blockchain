from django.shortcuts import render
from .models import Contact
#from .forms import ContactForm
# Create your views here.
def contact(request):
	if request.method =="POST":
		first_name=request.POST.get('first_name','')
		last_name=request.POST.get('last_name','')
		email=request.POST.get('email','')
		message=request.POST.get('message','')
		print(first_name,last_name,email,message)
		contact = Contact(first_name=first_name,last_name=last_name,email=email,message=message)
		contact.save()
	return render(request,'contact/contact.html')

def about(request):
	return render(request, 'contact/aboutus.html')

def api_instruction(request):
	return render(request, 'contact/api_instruction.html')