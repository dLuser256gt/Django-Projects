from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import LoginView
from django.conf import settings
from .forms import NewUserForm
from django.contrib import messages

@login_required
def dashboard(request):
    return render(request, 'dashboard.html')

class CustomLoginView(LoginView):
    template_name = 'login.html'
    redirect_authenticated_user = True
    success_url = '/dashboard/'

    def form_valid(self, form):
        self.request.session['next'] = self.request.POST.get('next', self.success_url)
        return super().form_valid(form)
    
    def form_invalid(self, form):
        return render(self.request, 'login.html', {'form': form, 'invalid': True})

def login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            next_url = request.POST.get('next', '/dashboard/')
            return redirect(next_url)
        else:
            error_message = "Invalid login credentials"
            return render(request, 'login.html', {'error_message': error_message})
    else:
        return render(request, 'login.html')
    
def register_request(request):
	if request.method == "POST":
		form = NewUserForm(request.POST)
		if form.is_valid():
			user = form.save()
			login(request, user)
			messages.success(request, "Registration successful." )
			return redirect(request.POST.get('next', '/dashboard/'))
		messages.error(request, "Unsuccessful registration. Invalid information.")
	form = NewUserForm()
	return render (request=request, template_name="register.html", context={"register_form":form})