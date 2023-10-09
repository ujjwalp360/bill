from django.urls import path
from django.http import HttpResponse
from django.conf import settings
from django.conf.urls.static import static
from flask import Flask

# Define a Flask app within Django
flask_app = Flask(__name__)

@flask_app.route('/flask/')
def flask_view():
    return "This is a Flask view within Django."

urlpatterns = [
    path('admin/', admin.site.urls),
    path('django/', lambda request: HttpResponse("This is a Django view.")),
]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
