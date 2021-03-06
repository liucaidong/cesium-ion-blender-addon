import bpy
from bpy.types import Operator
from bpy.props import *
import requests

from ..globals import (APP_OPERATOR_PREFIX, API_ADDRESS, CLIENT_ID)
from ..cache import save_properties


class GetTokenOperator(Operator):
    bl_label = "Cesium Token Fetch"
    bl_idname = f"{APP_OPERATOR_PREFIX}.get_token"
    bl_options = {'INTERNAL'}

    api_address: StringProperty(default=API_ADDRESS)
    client_id: StringProperty(default=CLIENT_ID)
    redirect_uri: StringProperty()
    code_verifier: StringProperty()
    code: StringProperty()

    def execute(self, context):

        url = f"{self.api_address}/oauth/token/"
        data = {
            "grant_type": "authorization_code",
            "code": self.code,
            "client_id": self.client_id,
            "redirect_uri": self.redirect_uri,
            "code_verifier": self.code_verifier
        }
        req = requests.post(url, json=data)
        output = req.json()

        if req.status_code != 200:
            self.report({"ERROR"}, "Authorization failed")
            return {"CANCELLED"}
        if "access_token" not in output:
            self.report({"ERROR"}, "Invalid access token")
            return {"CANCELLED"}

        csm_user = context.window_manager.csm_user
        csm_user.token = output["access_token"]
        save_properties(csm_user)

        return {"FINISHED"}


class ClearTokenOperator(Operator):
    bl_label = "Cesium Clear Token"
    bl_idname = f"{APP_OPERATOR_PREFIX}.clear_token"
    bl_options = {'INTERNAL'}

    def execute(self, context):
        csm_user = context.window_manager.csm_user
        csm_user.token = ""
        save_properties(csm_user)

        return {"FINISHED"}
