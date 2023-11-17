# Copyright 2023 Deepgram SDK contributors. All Rights Reserved.
# Use of this source code is governed by a MIT license that can be found in the LICENSE file.
# SPDX-License-Identifier: MIT

from .v1_response import Project, ProjectsResponse, Message, ProjectOptionsV1, KeysResponse, KeyResponse, KeyOptionsV1, Key, MembersResponse, ScopesResponse, ScopeOptionsV1, InvitesResponse, InviteOptionsV1, UsageRequestsResponse, UsageRequestOptionsV1, UsageRequest, UsageSummaryOptionsV1, UsageSummaryResponse, UsageFieldsResponse, UsageFieldsOptionsV1, BalancesResponse, Balance

from ...options import DeepgramClientOptions
from ..abstract_client import AbstractRestfulClient

class ManageClientV1(AbstractRestfulClient):
    """
    A client for managing Deepgram projects and associated resources via the Deepgram API.

    This class provides methods for performing various operations on Deepgram projects, including:
    - Retrieving project details
    - Updating project settings
    - Managing project members and scopes
    - Handling project invitations
    - Monitoring project usage and balances

    Args:
        config (DeepgramClientOptions): all the options for the client.

    Attributes:
        url (str): The base URL of the Deepgram API.
        headers (dict): Optional HTTP headers to include in requests.
        endpoint (str): The API endpoint for managing projects.

    Raises:
        DeepgramApiError: Raised for known API errors.
        DeepgramUnknownApiError: Raised for unknown API errors.
        Exception: For any other unexpected exceptions.
    """
    def __init__(self, config : DeepgramClientOptions):
      self.config = config
      self.endpoint = "v1/projects"
      super().__init__(config)
    
    # projects
    async def list_projects(self):
        return self.get_projects()
    async def get_projects(self):
        url = f"{self.config.url}/{self.endpoint}"
        return ProjectsResponse.from_json(await self.get(url))

    async def get_project(self, project_id: str):
        url = f"{self.config.url}/{self.endpoint}/{project_id}"
        return Project.from_json(await self.get(url))

    async def update_project_option(self, project_id: str, options: ProjectOptionsV1):
        url = f"{self.config.url}/{self.endpoint}/{project_id}"
        return Message.from_json(await self.patch(url, json=options))
    async def update_project(self, project_id: str, name=""):
        url = f"{self.config.url}/{self.endpoint}/{project_id}"
        options: ProjectOptionsV1 = {
            "name": name,
        }
        return Message.from_json(await self.patch(url, json=options))

    async def delete_project(self, project_id: str) -> None:
        url = f"{self.config.url}/{self.endpoint}/{project_id}"
        return Message.from_json(await self.delete(url))

    # keys
    async def list_keys(self, project_id: str):
        return self.get_keys(project_id)
    async def get_keys(self, project_id: str):
        url = f"{self.config.url}/{self.endpoint}/{project_id}/keys"
        result = await self.get(url)
        return KeysResponse.from_json(result)

    async def get_key(self, project_id: str, key_id: str):
        url = f"{self.config.url}/{self.endpoint}/{project_id}/keys/{key_id}"
        return KeyResponse.from_json(await self.get(url))

    async def create_key(self, project_id: str, options: KeyOptionsV1):
        url = f"{self.config.url}/{self.endpoint}/{project_id}/keys"
        return Key.from_json(await self.post(url, json=options))

    async def delete_key(self, project_id: str, key_id: str) -> None:
        url = f"{self.config.url}/{self.endpoint}/{project_id}/keys/{key_id}"
        return Message.from_json(await self.delete(url))

    # members
    async def get_members(self, project_id: str):
        url = f"{self.config.url}/{self.endpoint}/{project_id}/members"
        return MembersResponse.from_json(await self.get(url))

    async def remove_member(self, project_id: str, member_id: str) -> None:
        url = f"{self.config.url}/{self.endpoint}/{project_id}/members/{member_id}"
        return Message.from_json(await self.delete(url))

    # scopes
    async def get_member_scopes(self, project_id: str, member_id: str):
        url = f"{self.config.url}/{self.endpoint}/{project_id}/members/{member_id}/scopes"
        return ScopesResponse.from_json(await self.get(url))

    async def update_member_scope(self, project_id: str, member_id: str, options: ScopeOptionsV1):
        url = f"{self.config.url}/{self.endpoint}/{project_id}/members/{member_id}/scopes"
        return Message.from_json(await self.put(url, json=options))

    # invites
    async def list_invites(self, project_id: str):
        return self.get_invites(project_id)
    async def get_invites(self, project_id: str):
        url = f"{self.config.url}/{self.endpoint}/{project_id}/invites"
        return InvitesResponse.from_json(await self.get(url))

    async def send_invite_options(self, project_id: str, options: InviteOptionsV1):
        url = f"{self.config.url}/{self.endpoint}/{project_id}/invites"
        return Message.from_json(await self.post(url, json=options))
    async def send_invite(self, project_id: str, email: str, scope="member"):
        url = f"{self.config.url}/{self.endpoint}/{project_id}/invites"
        options: InviteOptionsV1 = {
            "email": email,
            "scope": scope,
        }
        return Message.from_json(await self.post(url, json=options))

    async def delete_invite(self, project_id: str, email: str):
        url = f"{self.config.url}/{self.endpoint}/{project_id}/invites/{email}"
        return Message.from_json(await self.delete(url))

    async def leave_project(self, project_id: str):
        url = f"{self.config.url}/{self.endpoint}/{project_id}/leave"
        return Message.from_json(await self.delete(url))

    # usage
    async def get_usage_requests(self, project_id: str, options: UsageRequestOptionsV1):
        url = f"{self.config.url}/{self.endpoint}/{project_id}/requests"
        return UsageRequestsResponse.from_json(await self.get(url, options))

    async def get_usage_request(self, project_id: str, request_id: str):
        url = f"{self.config.url}/{self.endpoint}/{project_id}/requests/{request_id}"
        return UsageRequest.from_json(await self.get(url))

    async def get_usage_summary(self, project_id: str, options: UsageSummaryOptionsV1):
        url = f"{self.config.url}/{self.endpoint}/{project_id}/usage"
        return UsageSummaryResponse.from_json(await self.get(url, options))

    async def get_usage_fields(self, project_id: str, options: UsageFieldsOptionsV1):
        url = f"{self.config.url}/{self.endpoint}/{project_id}/usage/fields"
        return UsageFieldsResponse.from_json(await self.get(url, options))

    # balances
    async def list_balances(self, project_id: str):
        return self.get_balances(project_id)
    async def get_balances(self, project_id: str):
        url = f"{self.config.url}/{self.endpoint}/{project_id}/balances"
        return BalancesResponse.from_json(await self.get(url))

    async def get_balance(self, project_id: str, balance_id: str):
        url = f"{self.config.url}/{self.endpoint}/{project_id}/balances/{balance_id}"
        return Balance.from_json(await self.get(url))
