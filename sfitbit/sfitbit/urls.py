"""sfitbit URL Configuration

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
from django.conf.urls import url
from django.contrib import admin
import spotify
import fitbit

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^log/track/', spotify.log),
    url(r'^log/end', spotify.end_log),
    url(r'^user/new/', fitbit.permissions_request),
    url(r'^user/fitbit/register', fitbit.authorize),
    url(r'^user/spotify/register', spotify.authorize)
]
