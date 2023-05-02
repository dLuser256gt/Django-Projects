from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import LoginView
from django.conf import settings
from .forms import NewUserForm
from django.contrib import messages
from django.http import HttpResponseRedirect
from .models import Income
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy

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
        password = request.POST['password1']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request)
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
            messages.success(request, "Registration successful.")
            return HttpResponseRedirect("/login/")
        else:
            password1 = form.data['password1']
            password2 = form.data['password2']
            email = form.data['email']
            for msg in form.errors.as_data():
                if msg == 'email':
                    messages.error(request, f"Declared {email} is not valid")
                if msg == 'password2' and password1 == password2:
                    messages.error(request, f"Selected password is not strong enough")
                elif msg == 'password2' and password1 != password2:
                    messages.error(request, f"Password and Confirmation Password do not match")
    form = NewUserForm()
    return render(request=request, template_name="register.html", context={"register_form": form})


""" Income Table """

# Displays a list of all the income objects belonging to the currently logged-in user.
class IncomeListView(LoginRequiredMixin, ListView):
    model = Income
    template_name = 'income_list.html'
    context_object_name = 'income_list'

    def get_queryset(self):
        return Income.objects.filter(user=self.request.user)

# Provides a form to create a new income object and saves it to the database.
class IncomeCreateView(LoginRequiredMixin, CreateView):
    model = Income
    fields = ['amount', 'date', 'category', 'description']
    success_url = reverse_lazy('income_list')

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)

#Provides a form to update an existing income object and updates it in the database.
class IncomeUpdateView(LoginRequiredMixin, UpdateView):
    model = Income
    fields = ['amount', 'date', 'category', 'description']
    success_url = reverse_lazy('income_list')

    def get_queryset(self):
        return Income.objects.filter(user=self.request.user)

# Deletes an existing income object from the database.
class IncomeDeleteView(LoginRequiredMixin, DeleteView):
    model = Income
    success_url = reverse_lazy('income_list')

    def get_queryset(self):
        return Income.objects.filter(user=self.request.user)