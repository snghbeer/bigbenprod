from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.views.generic import DetailView, CreateView
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import Post, Appointment
from users.models import User
from .forms import CreatePostForm, ApointmentForm, ApointmentModelForm, AppointmentUpdateForm
from django.views.decorators.csrf import csrf_protect
from selenium import webdriver
from time import sleep
from .secrets import pw
import os

from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options as ChromeOptions

chrome_bin = os.environ.get('GOOGLE_CHROME_SHIM', None)
opts = ChromeOptions()
opts.add_argument('--disable-gpu')
opts.add_argument('--no-sandbox')
#opts.add_argument('--headless')
opts.binary_location = chrome_bin
url = "https://www.instagram.com/"


class Instabot():
    def __init__(self, username, pw, appointment):
        self.driver = webdriver.Chrome(executable_path="chromedriver", chrome_options=opts)
        self.username = username
        self.url = "https://www.instagram.com/"

        self.driver.get(self.url)
        sleep(1)
        self.driver.find_element_by_xpath('//input[@name= "username"]')\
            .send_keys('snghbeer')
        self.driver.find_element_by_xpath('//input[@name= "password"]')\
            .send_keys(pw)
        self.driver.find_element_by_xpath('//button[@type="submit"]')\
            .click()
        sleep(2)
        self.driver.find_element_by_xpath('//button[contains(text(), "Plus tard")]')\
            .click()
        sleep(1)
        self.driver.find_element_by_xpath('//button[contains(text(), "Plus tard")]')\
            .click()
        sleep(1)
        self.driver.get(url+ appointment.blaze)
        self.driver.find_element_by_xpath('//button[contains(text(), "Contacter")]')\
            .click()
        sleep(1)
        self.driver.find_element_by_xpath('//textarea[@placeholder="Votre message…"]')\
            .send_keys('Ton rendez-vous pour le: ' + appointment.date.strftime("%H:%M:%S") + ' est confirmé, on va pull up saaaale!')
        sleep(2)
        self.driver.find_element_by_xpath('//button[contains(text(), "Envoyer")]')\
            .click()
        self.driver.close()

class DetailPostView(DetailView):
    model = Post
    template_name = 'bigbenapp/post_url.html'
    context_object_name = 'post-detail'

class CreatePostView(LoginRequiredMixin, CreateView):
    model = Post
    fields = ['title', 'content', 'image']
    template_name = 'bigbenapp/createpost_url.html'
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
    return render(request, 'bigbenapp/about.html',  context)


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

        return render(request, 'bigbenapp/create_post.html', context)


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
        template = 'bigbenapp/index.html'
        return render(request, template, context)

@csrf_protect
def create_appointmentt(request):
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
        template = 'bigbenapp/about.html'
        return render(request, template, context)

@csrf_protect
def rdv(request):
    if request.method == 'POST': #confirm an appointment
        appointments = request.POST.getlist('choices')
        for app_id in appointments:
            obj = Appointment.objects.get(id=app_id)
            obj.confirmed = True
            obj.save()
            Instabot('snghbeer', pw, obj)
        return redirect('rdv')

    context = {
        'appointments': Appointment.objects.all()
    }
    return render(request, 'bigbenapp/rdv.html',  context)