from django.shortcuts import render, HttpResponseRedirect, redirect, get_object_or_404, HttpResponse
from django.views.generic.edit import FormView
from django.views.generic import TemplateView, View
from home.forms import ContactForm
from django.db.models import Count
from django.conf import settings
from django.core.mail import send_mail
from django.contrib import messages
# from variables.models import Ptype
import datetime
from django.core.urlresolvers import reverse



# from django.conf import settings
# from django.contrib.auth.models import User
# from django.contrib.sites.models import Site
# from notifications.models import Notification
# # from datetime import datetime
# import datetime
# import pytz



class TermsAndConditionView(TemplateView):
    template_name = "sub/termsandconditions.html"


class DisclaimerView(TemplateView):
    template_name = "sub/disclaimer.html"


class PrivacyPolicyView(TemplateView):
    template_name = "sub/privacypolicy.html"


class RefundPolicyView(TemplateView):
    template_name = "sub/refundpolicy.html"


class PromotionView(TemplateView):
    template_name = "sub/promotions.html"


class FAQStudentView(TemplateView):
    template_name = "sub/faqstudents.html"


class FAQTutorView(TemplateView):
    template_name = "sub/faqtutors.html"


class CSupportView(TemplateView):
    template_name = "sub/customer_support.html"


class TutorialsView(TemplateView):
    template_name = "sub/tutorials.html"


class AboutUsView(TemplateView):
    template_name = "sub/about.html"


class CareersView(TemplateView):
    template_name = "sub/careers.html"


class PressView(TemplateView):
    template_name = "sub/press.html"


class PartnershipsView(TemplateView):
    template_name = "sub/partnerships.html"


class SiteMapView(TemplateView):
    template_name = "sitemap.xml"


# class PrelimsView(TemplateView):
#     template_name = "sub/prelims.html"

# class NavView(TemplateView):
#     template_name = "navbar.html"
#     def get_context_data(self, *args, **kwargs):
#         context = super(NavView, self).get_context_data(*args, **kwargs)
#         context["form"] = SearchForm()
#         return context

class HomeView(TemplateView):
    template_name = "home.html"
    title = 'Your Dashboard'
    # form_class = SearchForm

    # def dispatch(self, *args, **kwargs):
    #     dispatch = super(HomeView, self).dispatch(*args, **kwargs)
    #     #exit if no poll_id
    #     try: 
    #         print PUser.objects.get(user_id=self.request.user.id)
    #     except:
    #         return redirect('PUserCreate')

    #     return dispatch

    def get(self, request, *args, **kwargs):
        context = self.get_context_data(**kwargs)

        #redirecting users if user hasnt signed in
        if self.request.user.is_authenticated():
            try: 
                test = PUser.objects.get(user_id=self.request.user.id)
            except:
                return redirect('PUserCreate')

        return self.render_to_response(context)



    def get_context_data(self, *args, **kwargs):

        context = super(HomeView, self).get_context_data(*args, **kwargs)

        # context["form"] = SearchForm()

        if self.request.user.is_authenticated():
            fav_polls = PollFav.objects.filter(fav_user=self.request.user)

            #retrieving favourites of user
            pfav = PollFav.objects.filter(fav_user=self.request.user)

            #retrieving pollitems list
            pitem_lst = pfav.values_list('poll',flat=True)
            pitem_obj = PollItem.objects.filter(id__in=pitem_lst)

            #retrieving polltypes list
            ptype_lst = pitem_obj.values_list('polltype',flat=True).distinct()
            ptype_obj = Ptype.objects.filter(id__in=ptype_lst)

            context["submit_btn_value"] = "Send"
            context["title"] = self.title
            context["poll_types"] = ptype_obj
            todate = datetime.datetime.now().date()
            
            user = self.request.user

            context["pollsCreated"] = Ptype.objects.filter(c_user=user).count()
            context["pollsECreated"] = PollItem.objects.filter(user_submit=user).count()

            user_ptypes = Ptype.objects.filter(c_user=user)

            context["votes_polls"] = PollVote.objects.filter(posi=True, poll__polltype__in=user_ptypes).count()
            context["votes_poll_entries"] = PollVote.objects.filter(posi=True, poll__user_submit=user,
                                                                    poll__polltype__in=user_ptypes).count()


            # get user created ptypes
            created_polls = Ptype.objects.filter(c_user=user)
            # get list of views that belong to the pytypes created by user
            ptype_list = ViewPollTypeUnique.objects.filter(p_type__in=created_polls)
            # get user created polls
            context["votes_polls_views"] = ptype_list.values_list('userview',flat=True).distinct().count()


            # get user created pitems
            created_items = PollItem.objects.filter(user_submit=user)
            # get list of views that belong to the pytypes created by user
            pitem_list = ViewPollItemsUnique.objects.filter(p_item__in=created_items)
            # get user created polls
            context["votes_poll_entries_views"] = pitem_list.values_list('userview',flat=True).distinct().count()

            context["points"] = context["votes_polls_views"] + context["votes_poll_entries_views"]

            pt = context["points"]

            context["rank"] = Ranking.objects.get(low_score__lte=pt, high_score__gte=pt)

            try:
                context["user"] = PUser.objects.get(user_id=self.request.user.id)
            except:
                return redirect(reverse("PUserCreate"))

            return context

        return context


        


class ContactView(FormView):
    template_name = 'forms.html'
    form_class = ContactForm
    success_url = '/'
    title = 'Contact Us'

    def form_valid(self, form):

        form_email = form.cleaned_data.get("email")
        form_message = form.cleaned_data.get("message")
        form_full_name = form.cleaned_data.get("full_name")
        subject = "TeachAdvisor Contact Form"

        if settings.TYPE == "base":
            from_email = settings.EMAIL_HOST_USER
        else:
            from_email = settings.DEFAULT_FROM_EMAIL

        to_email = [from_email, form_email]  # [from_email, 'jumper23sierra@yahoo.com']
        contact_message = "<p>Message: %s.</p><br><p>From: %s</p><p>Email: %s</p>" % (
        form_message, form_full_name, form_email)

        send_mail(
            subject=subject,
            message="",
            html_message=contact_message,
            from_email=from_email,
            recipient_list=to_email,
            fail_silently=False
        )

        messages.info(self.request, "Thank you for your message, we will reply to you soon")
        return super(ContactView, self).form_valid(form)

    def get_context_data(self, *args, **kwargs):
        context = super(ContactView, self).get_context_data(*args, **kwargs)
        context["submit_btn_value"] = "Send"
        context["title"] = self.title
        return context





# #this works
# class SearchView(FormView):
#     template_name = 'base.html'
#     form_class = SearchForm
#     success_url = '/'

#     def form_valid(self, form):

#         print "test"

#         search = form.cleaned_data.get("search")

#         print search

#         messages.info(self.request, "Thank you for your message, we will reply to you soon")
#         return super(SearchView, self).form_valid(form)
 



# #this works
# class SearchView(FormView):
#     template_name = 'formtest.html'
#     form_class = SearchForm
#     success_url = '/'

#     def form_valid(self, form):

#         search = form.cleaned_data.get("search")

#         messages.info(self.request, "Thank you for your message, we will reply to you soon")
#         return super(SearchView, self).form_valid(form)
 



def Test(request):
    print "test"
    return redirect("Home")

# # We need to change this so that this will work with the latest registration
# class RegisterView(FormView):
# 	template_name = 'forms.html'
# 	form_class = RegisterForm
# 	success_url = '/'
# 	title = 'Register With Us'

# 	def get_context_data(self, *args, **kwargs):
# 		context = super(RegisterView, self).get_context_data(*args, **kwargs)
# 		context["title"] = title
# 		context["submit_btn_value"] = "Register"
# 		return context

# 	def form_valid(self, form):
# 		username = form.cleaned_data['username']
# 		email = form.cleaned_data['email']
# 		password = form.cleaned_data['password2']
# 		# MyUser.objects.create_user(username=username, email=email, password=password)
# 		new_user = MyUser()
# 		new_user.username = username
# 		new_user.email = email
# 		new_user.set_password(password)
# 		new_user.save()
# 		#email user
# 		#create user profile instance
# 		#add message for succcess
# 		return redirect('Home')
# 		# return super(RegisterView, self).form_valid(form)
