from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView

urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/schema/", SpectacularAPIView.as_view(), name="schema"),
    path("api/docs/", SpectacularSwaggerView.as_view(url_name="schema"), name="api-docs"),
    path("api/auth/", include("apps.accounts.api_urls")),
    path("api/children/", include("apps.children.api_urls")),
    path("api/groups/", include("apps.groups.api_urls")),
    path("api/attendance/", include("apps.attendance.api_urls")),
    path("api/meals/", include("apps.meals.api_urls")),
    path("api/activities/", include("apps.activities.api_urls")),
    path("api/reports/", include("apps.reports.api_urls")),
    path("api/dashboard/", include("apps.dashboard.api_urls")),
    path("accounts/", include("apps.accounts.urls")),
    path("", include("apps.dashboard.urls")),
    path("children/", include("apps.children.urls")),
    path("groups/", include("apps.groups.urls")),
    path("attendance/", include("apps.attendance.urls")),
    path("meals/", include("apps.meals.urls")),
    path("activities/", include("apps.activities.urls")),
    path("reports/", include("apps.reports.urls")),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

admin.site.site_header = "Kesh Vorislari ERP"
admin.site.site_title = "Kesh Vorislari"
admin.site.index_title = "Administration"
