from django.views.generic import ListView, CreateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin

class OwnerListView(LoginRequiredMixin, ListView):

    def get_queryset(self):
        "Allows only on the tasks of the logged in user to listed"
        qs =  super(OwnerListView, self).get_queryset()
        return qs.filter(owner=self.request.user)

    def get_context_data(self, **kwargs):
        '''This overides the default get_context_data passed into the template and adds the number of tasks of the logged in user.'''
        context = super().get_context_data(**kwargs)
        task_count = self.get_queryset().filter(state=False).count() #This counts only tasks that have not been completed
        context['task_count'] = task_count
        return context

    

class OwnerCreateView(LoginRequiredMixin, CreateView):
    
    def form_valid(self, form):
        '''Allows the logged in user to create tasks'''
        object = form.save(commit=False)
        object.owner = self.request.user
        object.save()
        return super(OwnerCreateView, self).form_valid(form)

    def get_queryset(self):
        "Allows only on the tasks of the logged in user to listed"
        qs =  super(OwnerCreateView, self).get_queryset()
        return qs.filter(owner=self.request.user)

    def get_context_data(self, **kwargs):
        '''This overides the default get_context_data passed into the template and adds the number of tasks of the logged in user.'''
        context = super().get_context_data(**kwargs)
        task_count = self.get_queryset().filter(state=False).count() #This counts only tasks that have not been completed
        context['task_count'] = task_count
        return context


class OwnerDeleteView(LoginRequiredMixin, DeleteView):
    """"
    Sub-class the DeleteView to restrict a User from deleting other user's data.
    """

    def get_queryset(self):
        qs = super(OwnerDeleteView, self).get_queryset()
        return qs.filter(owner=self.request.user)


