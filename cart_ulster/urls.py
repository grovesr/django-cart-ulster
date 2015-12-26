from django.conf.urls import include, url
from django.conf.urls.static import static
from django.conf import settings
from django.contrib import admin
from django.contrib.auth.views import login, logout
from . import views

handler400 = 'cart_ulster.views.handler400'
handler404 = 'cart_ulster.views.handler404'
handler500 = 'cart_ulster.views.handler500'

urlpatterns = [
    # Examples:
    # url(r'^$', 'redcross.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^ims/',include('ims.urls',namespace='ims')),
    url(r'^accounts/login$', login, name='login'),
    url(r'^accounts/logout$', logout, name='logout'),
    url(r'^$', views.home,name='home'),
    url(r'^cart_help$',views.cart_help, name='cart_help')
]

# serve uploaded media in development only
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
