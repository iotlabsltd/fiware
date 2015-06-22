import json
import base64
from django.core.urlresolvers import reverse

from rest_framework import status
from rest_framework.test import APITestCase

from ..ops import QueryContext, ContextResponses

from fiware.ngsi.tests.factories import AccountFactory, OAuth2ApplicationFactory, TestModelFactory


class NSGI10Tests(APITestCase):

    def get_access_token(self, username, password):
        url = reverse("oauth2_provider:token")
        q = {"grant_type": "password",
             "username": username,
             "password": password,
             "client_secret": self.oauth2_client.client_secret,
             "client_id": self.oauth2_client.client_id}
        response = self.client.post(url, q, format="multipart")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        r = json.loads(response.content)
        return r["access_token"]

    def setUp(self):
        self.user = AccountFactory.create()
        self.test_model = TestModelFactory.create()
        self.oauth2_client = OAuth2ApplicationFactory.create()
        un = getattr(self.user, "username", None) or getattr(self.user, "email", None)
        self.access_token = self.get_access_token(un, "123456")

    def test_queryContext_bad_request(self):
        url = reverse("ngsi:query-context")
        qc = QueryContext(entities=[{"foo": "bar"}])

        self.client.credentials(HTTP_AUTHORIZATION="Bearer %s"
                                % self.access_token)
        response = self.client.post(url, data=qc.to_dict())
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        r = json.loads(response.content)
        cr = ContextResponses.from_dict(r)
        self.assertEqual(len(cr.elements), 1)
        self.assertEqual(cr.elements[0][1], status.HTTP_400_BAD_REQUEST)

    def test_queryContext_access_deined_request(self):
        url = reverse("ngsi:query-context")
        qc = QueryContext(entities=[{
            "type": "foo.Bar",
            "isPattern": "false",
            "id": "1",
        }])
        self.client.credentials(HTTP_AUTHORIZATION="Bearer %s"
                                % self.access_token)
        response = self.client.post(url, data=qc.to_dict())
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        r = json.loads(response.content)
        cr = ContextResponses.from_dict(r)
        self.assertEqual(len(cr.elements), 1)
        self.assertEqual(cr.elements[0][1], status.HTTP_403_FORBIDDEN)

    def test_queryContext_single_request(self):
        url = reverse("ngsi:query-context")
        qc = QueryContext(entities=[{
            "type": "tests.testmodel",
            "isPattern": "false",
            "id": self.test_model.id,
        }])
        self.client.credentials(HTTP_AUTHORIZATION="Bearer %s"
                                % self.access_token)
        response = self.client.post(url, data=qc.to_dict())
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        r = json.loads(response.content)
        print r
        cr = ContextResponses.from_dict(r)
        self.assertEqual(len(cr.elements), 1)
        self.assertEqual(cr.elements[0][1], status.HTTP_200_OK)
        ce = cr.elements[0][0]
        self.assertEqual(ce.type, "tests.testmodel")
        self.assertEqual(ce.id, self.test_model.id)
