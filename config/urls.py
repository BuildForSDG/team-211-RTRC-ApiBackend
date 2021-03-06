from django.conf.urls import url
from django.urls import path, include
from django.contrib import admin
from django.views.generic import TemplateView
from django.conf import settings
from django.conf.urls.static import static

from rest_framework import routers
from rest_framework.documentation import include_docs_urls
from rest_framework_jwt.views import obtain_jwt_token, refresh_jwt_token
from allauth.account.views import ConfirmEmailView

from api.users.views import (
    AdminUserViewSet,
    UserViewSet,
    null_view,
    VerifyEmailView,
    CollectorViewSet,
    AdminCollectorViewSet
)


router = routers.DefaultRouter()
router.register('users', UserViewSet, base_name='users')
router.register('collectors', CollectorViewSet, basename='collector')

#admin endpoints
admin_router = routers.DefaultRouter()
admin_router.register('users', AdminUserViewSet, base_name='admin_users')
admin_router.register('collectors', AdminCollectorViewSet, basename='admin_collector')

admin.site.site_header = "I-COLLECTOR ADMIN"
admin.site.site_title = "I-COLLECTOR ADMIN"
admin.site.index_title = "I-COLLECTOR ADMIN"

urlpatterns = [
    path('', TemplateView.as_view(template_name='index.html'), name='home'),
    # path('docs/', include_docs_urls('Kwik Chow API Documentation')),

    # App Specific url & namespaces
    path('api/v1/', include(router.urls)),
    path('api/v1/admin/', include(admin_router.urls)),

    # Authentication Setup urls
    path('api/v1/rest-auth/', include('rest_auth.urls')),
    path('api/v1/rest-auth/registration/', include('rest_auth.registration.urls')),
    path('api/v1/rest-auth/registration/token-auth/', obtain_jwt_token),
    path('api/v1/rest-auth/registration/refresh-token/', refresh_jwt_token),

    # custom auth urls
    path('api/v1/rest-auth/registration/account-email-verification-sent/', null_view, name='account_email_verification_sent'),
    url(r'^verify-email/(?P<key>\d+)/$', VerifyEmailView.as_view(), name='account_confirm_email'),
    url(r'^api/v1/rest-auth/password/reset/confirm/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$', null_view, name='password_reset_confirm'),
    path('super-site/', admin.site.urls),
]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
