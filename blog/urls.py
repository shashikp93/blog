
from django.conf.urls import url
from django.contrib import admin
from vblog.views import *
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^$',index),
    url(r'^post_login/$',login),
    url(r'^accounts/auth/$',auth_view,name='check'),
    url(r'^search_query/$',search),
    url(r'^logout/$',logout_page),
    url(r'^success/$',success),
    url(r'^all_updates/$',updates,name='updates'),
    url(r'^post_insert/$',post_insert),
    url(r'^post_detail/(?P<id>\d+)/$',post_detail,name='detail'),
    url(r'^accounts/register/$',register_user,name='register'),
    url(r'^postcreate/$',post_create,name='post_create'),
    url(r'^postupdate/edit/(?P<id>\d+)/$',post_update,name='update'),
    url(r'^postdelete/(?P<id>\d+)/$',post_del,name='delete'),
    
]   + static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)






