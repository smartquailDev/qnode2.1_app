
#from django.contrib import admin
from django.urls import path,re_path,include
from django.conf import settings
from baton.autodiscover import admin
from courses.views import CourseListView
from django.contrib.auth import views as auth_views

from wagtail.admin import urls as wagtailadmin_urls
from wagtail.core import urls as wagtail_urls
from wagtail.documents import urls as wagtaildocs_urls

from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('baton/', include('baton.urls')),
    #E-commerce-configs
    #path('coupons/', include('coupons.urls', namespace='coupons')),
    #path('cart/', include('cart.urls', namespace='cart')),
    #path('orders/', include('orders.urls', namespace='orders')),
    #path('payment/', include('payment.urls', namespace='payment')),
    #path('shop/', include('shop.urls', namespace='shop')),
    #Eduaction Platform
    path('account/', include('account.urls')),
    #path('account/login/', auth_views.LoginView.as_view(), name='login'),
    #path('account/logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('course/', include('courses.urls')),
    path('course_list', CourseListView.as_view(), name='course_list'),
    path('students/', include('students.urls')),
    path('api/', include('courses.api.urls', namespace='api')),
    path('social-auth/', include('social_django.urls', namespace='social')),
    
     
    re_path(r'^smartbusinessmedia/', include(wagtailadmin_urls),name='wagtail'),
    re_path(r'^documents/', include(wagtaildocs_urls)),
    re_path(r'', include(wagtail_urls)),

 ] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT) 

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL,
                          document_root=settings.MEDIA_ROOT)

