# stdlib
import logging

# thirdparty
from fastapi import Request
from fastapi.responses import RedirectResponse
from onelogin.saml2.auth import OneLogin_Saml2_Auth

# project
from src.common.utils import SingletonWithArgs
from src.monetization_service.schemas.api.v1.auth_saml import UserSchema
from src.monetization_service.services.auth.base import BaseAuth
from src.monetization_service.settings.development import settings

logger = logging.getLogger(__name__)


class SamlAuth(BaseAuth, metaclass=SingletonWithArgs):
    def __init__(
        self,
        saml_settings: dict | None = None,
    ):
        """Initialize SAML auth service"""
        super().__init__()
        self.saml_settings = saml_settings
        self.auth = None

        if not self.saml_settings:
            self.saml_settings = {
                "strict": False,
                "debug": False,
                "idp": {
                    "entityId": settings.okta.entity_id,
                    "singleSignOnService": {
                        "url": settings.okta.sso_url,
                        "binding": "urn:oasis:names:tc:SAML:2.0"
                        ":bindings:HTTP-Redirect",
                    },
                    "x509cert": settings.okta.x509_cert,
                },
                "sp": {
                    "entityId": settings.okta.entity_id,
                    "assertionConsumerService": {
                        "url": settings.okta.callback_url,
                        "binding": "urn:oasis:names:tc:SAML:2.0"
                        ":bindings:HTTP-POST",
                    },
                    "x509cert": settings.okta.x509_cert,
                },
            }

    @staticmethod
    async def prepare_from_fastapi_request(request):
        """Prepare request data for SAML auth"""
        form_data = await request.form()
        rv = {
            "http_host": request.client.host,
            "server_port": request.url.port,
            "script_name": request.url.path,
            "post_data": {},
            "get_data": {},
        }
        if request.query_params:
            rv["get_data"] = (request.query_params,)
        if "SAMLResponse" in form_data:
            rv["post_data"]["SAMLResponse"] = form_data["SAMLResponse"]
        if "RelayState" in form_data:
            rv["post_data"]["RelayState"] = form_data["RelayState"]
        return rv

    async def refresh_auth_instance(self, request: Request):
        """Refresh auth instance with new request"""
        req = await self.prepare_from_fastapi_request(request)
        self.auth = OneLogin_Saml2_Auth(req, self.saml_settings)

    def prepare_redirect(self) -> RedirectResponse:
        """Prepare redirect to SAML IDP"""
        callback_url = self.auth.login()
        response = RedirectResponse(url=callback_url)
        return response

    def login(self) -> tuple[bool, UserSchema | str]:
        """Process SAML response and prepare user data"""
        self.auth.process_response()
        errors = self.auth.get_errors()

        if len(errors) == 0:
            if not self.auth.is_authenticated():
                return False, "User is not authenticated"
            else:
                user_data = self.auth.get_attributes()
                email = user_data["user.email"][0]
                first_name = None
                last_name = None

                if "user.first_name" in user_data:
                    if user_data["user.first_name"]:
                        first_name = user_data["user.first_name"][0]

                if "user.last_name" in user_data:
                    if user_data["user.last_name"]:
                        last_name = user_data["user.last_name"][0]

                return True, UserSchema(
                    email=email, first_name=first_name, last_name=last_name
                )
        else:
            return False, "Error when processing SAML Response: %s %s" % (
                ", ".join(errors),
                self.auth.get_last_error_reason(),
            )
