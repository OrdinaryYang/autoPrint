from . import views
from django.conf.urls import url
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    url(r'^index$', views.home, name='home'),
    url(r'login$', views.login, name='login'),
    url(r'logout$', views.logout, name='logout'),
    url(r'^$', views.upload_file, name='upload_file'),
    url(r'^helper', views.helper, name='helper'),
    url(r'^upload/$', views.upload_file, name='upload_file'),

    # 此url当前无用
    url(r'check_info/$', views.check_info, name='check_info'),

    url(r'details/$', views.post_details, name='post_details'),
    url(r'download/$', views.download, name='download'),
    url(r'printer/$', views.download_printer, name='download_printer'),

    # 此url当前无用
    url(r'^cn-(?P<order>[0-9]+)-(?P<comp_name>[\u4e00-\u9fa5]+)/$', views.get_details, name='get_details'),
]