"""hades URL Configuration

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
from django.conf.urls import url
from django.contrib import admin
from django.conf.urls.static import static

from . import views, settings

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^$', views.page_index),
    url(r'^next/$', views.page_next),
    url(r'^image/(?P<uuid>[a-f0-9\-]+)/$', views.page_image),
    url(r'^image/background/$', views.page_image_background),

    url(r'^login/$', views.page_login),
    url(r'^logout/$', views.page_logout),
    url(r'^pages/$', views.page_pages),
    url(r'^pages/new/$', views.page_pages_new),
    url(r'^pages/config/$', views.page_pages_config),
    url(r'^pages/config/background/delete/$', views.page_pages_config_background_delete),

    url(r'^page/delete/(?P<uuid>[a-f0-9\-]+)/$', views.page_page_delete),
] + static(settings.STATIC_URL, document_root=settings.STATICFILES_DIRS[0])
