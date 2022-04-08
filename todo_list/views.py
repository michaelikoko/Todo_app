from django.core.mail import EmailMessage
from django.views import View
from django.shortcuts import redirect, render
from todo_list import forms
from django.views.generic import CreateView, UpdateView
from django.contrib.auth.views import PasswordChangeView, PasswordResetView, PasswordResetConfirmView
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib.auth.models import User
from django.urls import reverse
from django.contrib.auth.mixins import LoginRequiredMixin
from todo_list import owner
from todo_list.models import Task
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.contrib.auth.tokens import default_token_generator
from django.contrib.sites.shortcuts import get_current_site
from django.core.mail import send_mail, BadHeaderError
from django.utils.encoding import force_bytes
from django.template.loader import render_to_string
from django.http import HttpResponse
from django.contrib import messages


# Create your views here.


class Register_User_View(SuccessMessageMixin, CreateView):
    model = User
    form_class = forms.Register_Form
    template_name = 'todo_list/register.html'
    success_message = "Hey %(first_name)s, verify your email address by clicking on the activation link sent to your email address."


    def get_success_message(self, cleaned_data):
        return self.success_message % dict(
        cleaned_data,
        first_name=self.object.first_name,
        )
    
    def get_success_url(self):
        return reverse('todo_list:dashboard')

    def form_valid(self, form):
        print('form valid ran')
        email = form.cleaned_data['email']
        user = form.save(commit = False)
        user.is_active = False #disables the just registered user account pending confirmation
        user.save()
        print(user, email)
        current_site = get_current_site(self.request) #Gets the current site
        subject = "Verify your email address"
        email_template_name = "todo_list/verify_email.html"
        context = {
        'domain':current_site.domain,
        'site_name': 'Todo',
        "uid": urlsafe_base64_encode(force_bytes(user.pk)),
        "user": user,
        'token': default_token_generator.make_token(user),
        'protocol': 'http',
        }
        message = render_to_string(email_template_name, context)
        email = EmailMessage(subject, message, to=[email])
        email.send()
        return super().form_valid(form)


def verify_email(request, uidb64, token):
        try:
            uid = urlsafe_base64_decode(uidb64).decode()
            user = User.objects.get(pk=uid)
            print('I ran')
        except:
            user = None
        if user is not None:
            user.is_active = True
            user.save()
            print('user has been made active')

            messages.add_message(request, messages.INFO, f'Hey {user.first_name}, you have been registered successfully')
        else:
            messages.add_message(request, messages.INFO, 'Activation link is invalid.')
        dashboard_url = reverse('todo_list:dashboard')
        return redirect(dashboard_url)
            


class Edit_Details_View(LoginRequiredMixin, SuccessMessageMixin, UpdateView):
    model = User
    form_class = forms.Edit_Details_Form
    template_name = 'todo_list/edit.html'
    success_message = "Your details have been edited successfully."

    def get_context_data(self, **kwargs):
        '''This overides the default get_context_data passed into the template and adds the number of tasks of the logged in user.'''
        context = super().get_context_data(**kwargs)
        task_count = Task.objects.filter(owner=self.request.user, state=False).count() #This only counts tasks that have been completed
        context['task_count'] = task_count
        return context

    def get_success_url(self):
        return reverse('todo_list:dashboard')

class Change_Password_View(LoginRequiredMixin, SuccessMessageMixin, PasswordChangeView):
    form_class = forms.Change_Password_Form
    template_name = 'todo_list/change_password.html'
    success_message = 'Your password has been reset successfully.'

    def get_context_data(self, **kwargs):
        '''This overides the default get_context_data passed into the template and adds the number of tasks of the logged in user.'''
        context = super().get_context_data(**kwargs)
        task_count = Task.objects.filter(owner=self.request.user, state=False).count() #This only counts tasks that have been completed
        context['task_count'] = task_count
        return context

    def get_success_url(self):
        return reverse('todo_list:dashboard')

class Reset_Password_View(SuccessMessageMixin, PasswordResetView):
    form_class = forms.Reset_Password_Form
    template_name = 'todo_list/reset_password.html'
    email_template_name = 'todo_list/reset_password_email.html'
    subject_template_name = 'todo_list/reset_password_subject.txt'
    success_message = "We've emailed you instructions for setting your password, if an account exists with the email you entered. You should receive them shortly."

    def get_success_url(self):
        return reverse('todo_list:dashboard')

class Reset_Password_Confirm_View(SuccessMessageMixin, PasswordResetConfirmView):
    form_class = forms.Reset_Password_Confirm_Form
    template_name = 'todo_list/reset_password_confirm.html'
    success_message = 'Your password has been reset successfully.'

    def get_success_url(self):
        return reverse('todo_list:dashboard')

class Landing_Page(View):
    def get(self, request):
        return render(request, 'todo_list/landing_page.html')

class Dashboard(owner.OwnerListView):
    '''This lists all the tasks of the logged in user. It inherits from the class owner.ListView'''
    model = Task
    template_name = 'todo_list/dashboard.html'

    def post(self, request):
        id = request.POST['id']
        task = Task.objects.get(pk=id, owner=self.request.user)
        task.state = True
        task.save()
        dashboard_url = reverse('todo_list:dashboard')
        return redirect(dashboard_url)

class Add_Task_View(SuccessMessageMixin, owner.OwnerCreateView):
    model = Task
    form_class = forms.Add_Task_Form
    template_name = 'todo_list/add_task.html'
    success_message = 'Task successfully added'
    
    def get_success_url(self):
        return reverse('todo_list:dashboard')

class Delete_Task(SuccessMessageMixin ,owner.DeleteView):
    model = Task
    success_message = 'Task successfully deleted'
    
    def get_success_url(self):
        return reverse('todo_list:dashboard')

class Search(View):
    def get(self, request):
        search_term = request.GET['search'].lower()
        tasks = Task.objects.filter(owner=self.request.user).all()
        task_count = Task.objects.filter(owner=self.request.user, state=False).count()
        search_results = self.get_results(tasks, search_term)
        context = {'search_results':search_results, 'search_term':search_term, 'task_count': task_count}
        return render(request, 'todo_list/search.html', context)

    def post(self, request):
        id = request.POST['id']
        task = Task.objects.get(pk=id, owner=self.request.user)
        task.state = True
        task.save()
        dashboard_url = reverse('todo_list:dashboard')
        return redirect(dashboard_url)


    def get_results(self, tasks, search_term):
        search_results = list()
        for task in tasks:
            word_list = task.description.split()
            word_list = [ word.lower() for word in word_list]
            if search_term in word_list:
                search_results.append(task)
        return search_results

    