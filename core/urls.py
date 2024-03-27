
# myproject/urls.py
from django.contrib import admin
from django.urls import path, include

# myproject/urls.py
from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static
from web import views as views

urlpatterns = [
    path('', views.index, name='index'),
    path('admin/', admin.site.urls),
    path('', include(('web.urls', 'web'), namespace='web')),
    path('chat/', include('chat.urls')),
    path('hotel/', include(('hotel.urls', 'hotel'), namespace='hotel')),
    path('shop/', include(('shop.urls', 'shop'), namespace='shop')),
    path('blog/', include(('blog.urls', 'blog'), namespace='blog')),
    path('sass/', include(('sass.urls', 'sass'), namespace='sass')),


]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
