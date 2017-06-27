from . import views
from django.conf.urls import url
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    url(r'^$', views.home, name='home'),
    url(r'^upload/$', views.upload_file, name='upload_file'),
    url(r'checkInfo/$', views.check_info, name='check_info'),
]