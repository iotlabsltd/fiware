from django.utils.importlib import import_module
from django.conf import settings
from django.apps import apps

from rest_framework import views
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework import status

from oauth2_provider.ext.rest_framework import OAuth2Authentication

# from django_recycle.utils.loading import import_class

from ops import QueryContext, UpdateContext, ContextResponses
from element import ContextElement

EXPORTED_MODELS = getattr(settings, "FIWARE_EXPORTED_MODELS", set())


def import_class(class_string):
    module, classname = class_string.rsplit(".", 1)
    m = import_module(module)
    return getattr(m, classname)


class NGSI10QueryContext(views.APIView):
    permission_classes = [IsAuthenticated, ]
    authentication_classes = [OAuth2Authentication, ]

    def post(self, request):
        query = QueryContext.from_dict(request.data)
        elements = []  # (ContextElement, status_code, reason)
        for e in query.entities:
            t = e.get("type")
            if not t:
                elements.append((ContextElement(None, None),
                                status.HTTP_400_BAD_REQUEST,
                                "missing element type"))
                continue
            if t not in EXPORTED_MODELS:
                elements.append((ContextElement(None, None),
                                status.HTTP_403_FORBIDDEN,
                                "Access denied"))
                continue
            mid = e.get("id")
            if not mid:
                elements.append((ContextElement(None, None),
                                status.HTTP_400_BAD_REQUEST,
                                "missing element id"))
                continue
            if not isinstance(mid, (str, unicode)):
                mid = int(mid)
            try:
                app_label, model_name = t.split(".", 2)
                model = apps.get_model(app_label=app_label,
                                       model_name=model_name)
                m = model.objects.get(id=mid)
                serializer = import_class(EXPORTED_MODELS[t])
                ce = ContextElement.from_model(m, serializer)
                elements.append((ce, status.HTTP_200_OK, ""))
            except Exception, e:
                elements.append((ContextElement(None, None),
                                status.HTTP_400_BAD_REQUEST,
                                str(e)))
                continue
        cr = ContextResponses(elements)
        return Response(data=cr.to_dict())


class NGSI10UpdateContext(views.APIView):
    permission_classes = [IsAuthenticated, ]
    authentication_classes = [OAuth2Authentication, ]

    def post(self, request):
        query = UpdateContext.from_dict(request.data)
        elements = []
        for e in query.elements:
            if e.type is None:
                elements.append((ContextElement(None, None),
                                status.HTTP_400_BAD_REQUEST,
                                "missing element type"))
                continue
            if e.type not in EXPORTED_MODELS:
                elements.append((ContextElement(None, None),
                                status.HTTP_403_FORBIDDEN,
                                "Access denied"))
                continue
            try:
                app_label, model_name = e.type.split(".", 2)
                model = apps.get_model(app_label=app_label,
                                       model_name=model_name)
                m = model()
                params = e.attrs
                serializer = import_class(EXPORTED_MODELS[e.type])
                s = serializer(data=params)
                if e.id is not None:
                    m = model.objects.get(id=e.id)
                    params["id"] = e.id
                    s = serializer(m, data=params)
                if not s.is_valid():
                    elements.append((ContextElement(None, None),
                                    status.HTTP_400_BAD_REQUEST,
                                    "Invalid attributes"))
                    continue
                s.save()
            except Exception, e:
                elements.append((ContextElement(None, None),
                                status.HTTP_400_BAD_REQUEST,
                                str(e)))
                continue
        # XXX notify subscribes in the background
        cr = ContextResponses(elements)
        return Response(data=cr.to_dict())
