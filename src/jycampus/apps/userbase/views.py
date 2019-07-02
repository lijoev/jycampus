from __future__ import unicode_literals

from django.contrib.auth import get_user_model
from django.http import HttpResponse, JsonResponse

from django.core.exceptions import ValidationError
try:
    from django.utils import simplejson as json
except ImportError:
    import json
import logging
from braces.views import AnonymousRequiredMixin
from django.contrib.auth import login, authenticate
from django.shortcuts import redirect, get_object_or_404
from django.shortcuts import render
from django.views.generic import TemplateView
from .forms import LoginForm, ProfileForm, \
    AddParticipantsForm
from .models import Profile, Participants
from django.contrib import messages
from django.utils.http import urlsafe_base64_decode
from django.core.paginator import Paginator
from django.shortcuts import render_to_response

User = get_user_model()

LOG = logging.getLogger('myStock.%s' % __name__)

# Create your views here.


class LoginView(AnonymousRequiredMixin, TemplateView):
    """
    Login view class. Users are logged in
    using either email or nick name.
    """

    login_form = LoginForm
    initial = {'key': 'value'}
    template_name = 'registration/login.html'

    def get(self, request, *args, **kwargs):
        """
        function which return the template with login and signup form
        :param request:
        :param args:
        :param kwargs:
        :return:
        """
        login_form = self.login_form(initial=self.initial)

        context = {
            'login_form': login_form,

        }
        return render(request, self.template_name, context)

    def post(self, request):
        """
        function which handles post request from login and signup form
        to login and create user
        :param request:
        :param args:
        :param kwargs:
        :return:
        """

        login_form = self.login_form(request.POST)
        context = {
            'login_form': login_form,

        }
        if login_form.is_valid():
            email = login_form.cleaned_data.get('email')
            raw_password = login_form.cleaned_data.get('password')
            try:
                print("user")
                user = authenticate(email=email, password=raw_password)
                login(request, user)
                return redirect('/participants')
            except:
                messages.warning(request, 'Email And Password Does Not Match.')
                return redirect('/login')
        return render(request, self.template_name, context)

        # elif request.POST.get('submit') == 'sign_up':
        #     sign_up_form = self.sign_up_form(request.POST)
        #     login_form = self.login_form()
        #     i_agree_form = self.i_agree_form(request.POST)
        #     forgot_password_form = self.forgot_password_form()
        #     context = {
        #         'login_form': login_form,
        #         'signup_form': sign_up_form,
        #         'i_agree_form': i_agree_form,
        #         'forgot_password_form': forgot_password_form,
        #     }
        #     if sign_up_form.is_valid() and i_agree_form.is_valid():
        #         subscription_flag = sign_up_form.cleaned_data.get('is_subscribed')
        #         subscription_email = sign_up_form.cleaned_data.get('email')
        #         user = sign_up_form.save(commit=False)
        #         user.is_active = False
        #         user.is_subscribed = subscription_flag
        #         user.save()
        #         if subscription_flag == True:
        #             # call the services to add to subscription list.
        #             services.add_to_subscription_list(subscription_email)
        #
        #         # context['line1'] = "Welcome to Spattern.net."
        #         # context['line2'] = "We have sent the registration confirmation link to your email address."
        #         # context['line3'] = "If you have not received the password link, please check your junk email folder."
        #         # context['line4'] = "Team SPatterns.net"
        #
        #         context['message'] = "Welcome to Spattern.net. We have sent the registration " \
        #                              "confirmation link to your email address. " \
        #                              "If you have not received the password link, " \
        #                              "please check your junk email folder. Team SPatterns.net"
        #         return render(request, self.template_name, context)
        #     return render(request, self.template_name, context)


class ParticipantsView(TemplateView):
    participants_form = AddParticipantsForm
    # sign_up_form = SignUpForm
    initial = {'key': 'value'}
    template_name = 'registration/participants.html'

    def get(self, request, *args, **kwargs):
        """
        function which return the template with login and signup form
        :param request:
        :param args:
        :param kwargs:
        :return:
        """
        participants_form = self.participants_form(initial=self.initial)

        context = {
            'participants_form': participants_form,

        }
        return render(request, self.template_name, context)

    def post(self, request):
        """

        :param request:
        :return:
        """
        participants_form = self.participants_form(request.POST)
        if participants_form.is_valid():
            try:
                participants_form.save()
            except ValidationError as e:
                print(e)
                pass
        context = {
            'participants_form': participants_form,

        }
        return render(request, self.template_name, context)


class ParticipantList(TemplateView):
    """

    """
    template_name = 'registration/participants_list.html'

    def get(self, request, *args, **kwargs):
        """

        :param request:
        :param args:
        :param kwargs:
        :return:
        """
        participants = Participants.objects.all()
        context = {
            'participants': participants
        }
        return render(request, self.template_name, context)

class AboutUs(TemplateView):
    """

    """
    template_name = 'registration/about.html'

    def get(self, request, *args, **kwargs):
        """

        :param request:
        :param args:
        :param kwargs:
        :return:
        """
        return render(request, self.template_name)


class Mission(TemplateView):
    """

    """
    template_name = 'registration/mission.html'

    def get(self, request, *args, **kwargs):
        """

        :param request:
        :param args:
        :param kwargs:
        :return:
        """
        return render(request, self.template_name)


class HomeView(TemplateView):
    """

    """
    template_name = 'registration/participants_list.html'

    def get(self, request, *args, **kwargs):
        """

        :param request:
        :param args:
        :param kwargs:
        :return:
        """
        participants = Participants.objects.all()
        context = {
            'participants': participants
        }
        return render(request, self.template_name, context)