from django.conf.urls import url
from django.urls import path, include
from django.contrib import admin
from django.views.generic import TemplateView
from django.conf import settings
from django.conf.urls.static import static
from rest_framework import permissions
from rest_framework import routers
from rest_framework.documentation import include_docs_urls
from rest_framework_jwt.views import obtain_jwt_token, refresh_jwt_token
from allauth.account.views import ConfirmEmailView
from drf_yasg.views import get_schema_view
from drf_yasg import openapi

from api.users.views import (
    AdminUserViewSet,
    UserViewSet,
    null_view,
    VerifyEmailView,
    CollectorViewSet,
    AdminCollectorViewSet,
    NationalIdTypeViewSet,
    AdminNationalIdTypeViewSet
)

from api.tolls.views import (
    TollLocationViewSet, AdminTollLocationViewSet,
    TollViewSet, AdminTollViewSet,
)
from api.vehicles.views import (
    VehicleCategoryViewSet, 
    AdminVehicleCategoryViewSet,
    VehicleViewSet,
    AdminVehicleViewSet,
    )
from api.wallet.views import (
    WalletViewSet, AdminDepositViewSet,
    DepositViewSet, TransactionViewSet,
    AdminTransactionViewSet
)

# user and collector endpoints
router = routers.DefaultRouter()
router.register('users', UserViewSet, base_name='users')
router.register('collectors', CollectorViewSet, basename='collector')
router.register('id-types', NationalIdTypeViewSet, basename='id_types')
router.register('toll-locations', TollLocationViewSet, basename='toll_locations')
router.register('tolls', TollViewSet, basename='tolls')
router.register('vehicle-categories', VehicleCategoryViewSet, basename='vehicle_categories')
router.register('vehicles', VehicleViewSet, basename='vehicles')
router.register('wallet', WalletViewSet, basename='wallet')
router.register('deposits', DepositViewSet, basename='deposits')
router.register('transactions', TransactionViewSet, basename='transactions')

#admin endpoints
admin_router = routers.DefaultRouter()
admin_router.register('users', AdminUserViewSet, base_name='admin_users')
admin_router.register('collectors', AdminCollectorViewSet, basename='admin_collector')
admin_router.register('id-types', AdminNationalIdTypeViewSet, basename='admin_id_types')
admin_router.register('toll-locations', AdminTollLocationViewSet, basename='admin_toll_locations')
admin_router.register('tolls', AdminTollViewSet, 'admin_tolls')
admin_router.register('vehicle-categories', VehicleCategoryViewSet, basename='admin_vehicle_categories')
admin_router.register('vehicles', AdminVehicleViewSet, basename='admin_vehicles')
admin_router.register('deposits', AdminDepositViewSet, basename='admin_deposits')
admin_router.register('transactions', AdminTransactionViewSet, basename='admin_transactions')

admin.site.site_header = "E-REVENUE ADMIN"
admin.site.site_title = "E-REVENUE ADMIN"
admin.site.index_title = "E-REVENUE ADMIN"

schema_view = get_schema_view(
   openapi.Info(
      title="Snippets API",
      default_version='v1',
      description="Test description",
      terms_of_service="https://www.google.com/policies/terms/",
      contact=openapi.Contact(email="contact@snippets.local"),
      license=openapi.License(name="BSD License"),
   ),
   public=True,
   permission_classes=(permissions.AllowAny,),
)


urlpatterns = [
    path('', TemplateView.as_view(template_name='index.html'), name='home'),
    # path('docs/', include_docs_urls('Kwik Chow API Documentation')),
    url(r'^swagger(?P<format>\.json|\.yaml)$', schema_view.without_ui(cache_timeout=0), name='schema-json'),
    url(r'^swagger/$', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    url(r'^redoc/$', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
    path('docs/', TemplateView.as_view(
        template_name='redoc.html',
        extra_context={'schema_url':'openapi-schema'}
    ), name='redoc'),

    # App Specific url & namespaces
    path('api/v1/', include(router.urls)),
    path('api/v1/admin/', include(admin_router.urls)),

    # Authentication Setup urls
    path('api/v1/auth/', include('rest_auth.urls')),
    path('api/v1/auth/register/', include('rest_auth.registration.urls')),
    path('api/v1/auth/token-auth/', obtain_jwt_token),
    path('api/v1/auth/refresh-token/', refresh_jwt_token),

    # custom auth urls
    path('api/v1/auth/account-email-verification-sent/', null_view, name='account_email_verification_sent'),
    url(r'^verify-email/(?P<key>\d+)/$', VerifyEmailView.as_view(), name='account_confirm_email'),
    url(r'^api/v1/auth/password/reset/confirm/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$', null_view, name='password_reset_confirm'),
    path('super-site/', admin.site.urls),
]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
