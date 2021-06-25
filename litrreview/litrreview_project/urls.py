from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path  # new

urlpatterns = [
    path('admin/', admin.site.urls),
    path('users/', include('users.urls')),  # new
    path('users/', include('django.contrib.auth.urls')),  # new
    # path('', TemplateView.as_view(template_name='home.html'),
    #      name='home'),  # new
    path('tickets/', include('tickets.urls')),
    path('', include('pages.urls')),  # new

]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL,
                          document_root=settings.MEDIA_ROOT)
