"""teachadvisor URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.10/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""


from django.conf.urls import url, include
from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static
from home.views import HomeView, AboutUsView, PromotionView, ContactView, TermsAndConditionView, DisclaimerView, PrivacyPolicyView, RefundPolicyView, FAQTutorView, FAQStudentView, CSupportView, TutorialsView, CareersView, PressView, PartnershipsView, SiteMapView, Test#, SearchView
# from polls.views import FavPollSub
# from polls.views import PollSearchView

# test push


urlpatterns = [
    url(r'^admin/', admin.site.urls),

    # polling system
    # url('^', include('polls.urls')),

    url(r'^accounts/', include('allauth.urls')),
    url(r'^$', HomeView.as_view(), name='Home'),
    url(r'^contact/$', ContactView.as_view(), name='Contact'),
    url(r'^promotions/$', PromotionView.as_view(), name='Promotions'),






#    url(r'^test/$', SearchView.as_view(), name='SearchView'),



    # favoriting openings or teacher
    # url(r'^polls/(?P<pk>[0-9]+)/FavPollSub$', FavPollSub),


]


if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
