from django.contrib import admin
from django.urls import include, path

admin.site.site_header = "Адміністрування сайту ФПрН НаУКМА"
admin.site.site_title = "ФПрН НаУКМА"

urlpatterns = [
    path("admin/", admin.site.urls),
    path("exchange/", include("exchange.urls")),
    path("", include("faculty.urls")),
]
