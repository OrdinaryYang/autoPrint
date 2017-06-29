from . import views
from django.conf.urls import url
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    url(r'^$', views.home, name='home'),
    url(r'^upload/$', views.upload_file, name='upload_file'),
    url(r'checkInfo/$', views.check_info, name='check_info'),
    url(r'details/$', views.post_details, name='post_details'),
    url(r'^cn-(?P<order>[0-9]+)-(?P<comp_name>[\u4e00-\u9fa5]+)/$', views.get_details, name='get_details'),
]