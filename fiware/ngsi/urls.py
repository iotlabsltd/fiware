from django.conf.urls import url
from rest_framework.urlpatterns import format_suffix_patterns
import views

urlpatterns = [
    url(r'^ngsi10/queryContext$', views.NGSI10QueryContext.as_view(),
        name="query-context"),
]

urlpatterns = format_suffix_patterns(urlpatterns)
