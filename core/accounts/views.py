from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.views import LoginView 
from django.contrib.auth import authenticate, login
from django.contrib.auth import get_user_model
from django.views.generic.edit import CreateView
from django.views import View

# Create your views here.
User = get_user_model()

class CustomLoginView(LoginView):
    redirect_authenticated_user = True
    template_name = "accounts/login.html"
    fields = ['email', 'password']
    success_url = '/todo/items/'
    def form_invalid(self, form):
        return self.render_to_response(self.get_context_data(form=form))

class RegisterPage(CreateView):
    model = User
    fields = ['email', 'password']
    template_name = 'accounts/register.html'
    success_url = '/todo/items/'

