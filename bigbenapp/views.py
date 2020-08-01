from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.views.generic import DetailView, CreateView
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import Post, Appointment
from users.models import User
from .forms import CreatePostForm, ApointmentForm, ApointmentModelForm, AppointmentUpdateForm
from django.views.decorators.csrf import csrf_protect

class DetailPostView(DetailView):
    model = Post
    template_name = 'app_folder/post_url.html'
    context_object_name = 'post-detail'

class CreatePostView(LoginRequiredMixin, CreateView):
    model = Post
    fields = ['title', 'content', 'image']
    template_name = 'app_folder/createpost_url.html'
    context_object_name = 'createpost'

    def get_absolute_url(self):
        return redirect('index')

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

    def get_succes_url (self):
        return redirect('index')


def about(request):
    context = {
        'posts': Post.objects.all()
    }
    return render(request, 'app_folder/index.html',  context)


def create_post(request):
    context = {}
    user = request.user

    form = CreatePostForm(request.POST or None, request.FILES or None)
    if form.is_valid():
        obj = form.save(commit=False)
        author = User.objects.filter(email = user.email).first()
        obj.author = author
        obj.save()
        form = CreatePostForm()

        context['form'] = form

        return render(request, 'app_folder/create_post.html', context)


@csrf_protect
def create_appointment(request):
    if request.method == 'POST':
        form = ApointmentModelForm(request.POST or None)
        if form.is_valid():
            new= form.save()
            return redirect('index')
    else:
        form = ApointmentForm()

        context = {
            'form': form,
            }
        template = 'app_folder/about.html'
        return render(request, template, context)


def confirm_appointment(request):
    if request.method == 'POST':
        appointments = request.POST.getlist('choices')
        for app_id in appointments:
            obj = Appointment.objects.get(id=app_id)
            obj.confirmed = True
            obj.save()
        return redirect('rdv')

@csrf_protect
def rdv(request):
    if request.method == 'POST':
        appointments = request.POST.getlist('choices')
        for app_id in appointments:
            obj = Appointment.objects.get(id=app_id)
            obj.confirmed = True
            obj.save()
        return redirect('rdv')

    context = {
        'appointments': Appointment.objects.all()
    }
    return render(request, 'app_folder/rdv.html',  context)