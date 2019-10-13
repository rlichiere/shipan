"""shipan URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
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
from django.contrib.auth import views as auth_views
from django.views.static import serve

from people.views import join
from people.forms import FrontAuthForm

from . import settings


urlpatterns = [
   url(r'^admin/doc/', include('django.contrib.admindocs.urls')),
   url(r'^admin/', admin.site.urls),
   url(r'^backoffice/', include('backoffice.urls')),

   url(r'^login/$', auth_views.login, {'template_name': 'people/login.html', 'authentication_form': FrontAuthForm},
       name='login'),
   url(r'^logout/$', auth_views.logout, {'next_page': '/'},
       name='logout'),
   url(r'^join/$', join,
       name='join'),
   url('^people/', include('people.urls')),

   url(r'^', include('frontoffice.urls')),

   url(r'^media/(?P<path>.*)$', serve, {'document_root': settings.MEDIA_ROOT}, name='media'),
   url(r'^doc/', include('doc.urls')),
]
