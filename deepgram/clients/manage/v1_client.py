# Copyright 2023 Deepgram SDK contributors. All Rights Reserved.
# Use of this source code is governed by a MIT license that can be found in the LICENSE file.
# SPDX-License-Identifier: MIT

from .v1_response import Project, ProjectsResponse, Message, ProjectOptionsV1, KeysResponse, Key, KeyOptionsV1, CreateKeyResponse, MembersResponse, ScopesResponse, ScopeOptionsV1, InvitesResponse, InviteOptionsV1, UsageRequestsResponse, UsageRequestOptionsV1, UsageRequest, UsageSummaryOptionsV1, UsageSummaryResponse, UsageFieldsResponse, UsageFieldsOptionsV1, BalancesResponse, Balance

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
        url (str): The base URL of the Deepgram API.
        headers (dict): Optional HTTP headers to include in requests.

    Attributes:
        url (str): The base URL of the Deepgram API.
        headers (dict): Optional HTTP headers to include in requests.
        endpoint (str): The API endpoint for managing projects.

    Raises:
        DeepgramApiError: Raised for known API errors.
        DeepgramUnknownApiError: Raised for unknown API errors.
        DeepgramUnknownError: Raised for unexpected errors not specific to the API.
        Exception: For any other unexpected exceptions.
    """
    def __init__(self, url, headers):
      self.url = url
      self.headers = headers
      self.endpoint = "v1/projects"
      super().__init__(url, headers)

    async def get_projects(self) -> ProjectsResponse:
        url = f"{self.url}/{self.endpoint}"
        return await self.get(url)

    async def get_project(self, project_id: str) -> Project:
        url = f"{self.url}/{self.endpoint}/{project_id}"
        return await self.get(url)

    async def update_project(self, project_id: str, options: ProjectOptionsV1) -> Message:
        url = f"{self.url}/{self.endpoint}/{project_id}"
        return await self.patch(url, json=options)

    async def delete_project(self, project_id: str) -> None:
        url = f"{self.url}/{self.endpoint}/{project_id}"
        return await self.delete(url)

    async def get_project_keys(self, project_id: str) -> KeysResponse:
        url = f"{self.url}/{self.endpoint}/{project_id}/keys"
        return await self.get(url)

    async def get_project_key(self, project_id: str, key_id: str) -> Key:
        url = f"{self.url}/{self.endpoint}/{project_id}/keys/{key_id}"
        return await self.get(url)

    async def create_project_key(self, project_id: str, options: KeyOptionsV1) -> CreateKeyResponse:
        url = f"{self.url}/{self.endpoint}/{project_id}/keys"
        return await self.post(url, json=options)

    async def delete_project_key(self, project_id: str, key_id: str) -> None:
        url = f"{self.url}/{self.endpoint}/{project_id}/keys/{key_id}"
        return await self.delete(url)

    async def get_project_members(self, project_id: str) -> MembersResponse:
        url = f"{self.url}/{self.endpoint}/{project_id}/members"
        return await self.get(url)

    async def remove_project_member(self, project_id: str, member_id: str) -> None:
        url = f"{self.url}/{self.endpoint}/{project_id}/members/{member_id}"
        return await self.delete(url)

    async def get_project_member_scopes(self, project_id: str, member_id: str) -> ScopesResponse:
        url = f"{self.url}/{self.endpoint}/{project_id}/members/{member_id}/scopes"
        return await self.get(url)

    async def update_project_member_scope(self, project_id: str, member_id: str, options: ScopeOptionsV1) -> Message:
        url = f"{self.url}/{self.endpoint}/{project_id}/members/{member_id}/scopes"
        return await self.put(url, json=options)

    async def get_project_invites(self, project_id: str) -> InvitesResponse:
        url = f"{self.url}/{self.endpoint}/{project_id}/invites"
        return await self.get(url)

    async def send_project_invite(self, project_id: str, options: InviteOptionsV1) -> Message:
        url = f"{self.url}/{self.endpoint}/{project_id}/invites"
        return await self.post(url, json=options)

    async def delete_project_invite(self, project_id: str, email: str) -> Message:
        url = f"{self.url}/{self.endpoint}/{project_id}/invites/{email}"
        return await self.delete(url)

    async def leave_project(self, project_id: str) -> Message:
        url = f"{self.url}/{self.endpoint}/{project_id}/leave"
        return await self.delete(url)

    async def get_project_usage_requests(self, project_id: str, options: UsageRequestOptionsV1) -> UsageRequestsResponse:
        url = f"{self.url}/{self.endpoint}/{project_id}/requests"
        return await self.get(url, options)

    async def get_project_usage_request(self, project_id: str, request_id: str) -> UsageRequest:
        url = f"{self.url}/{self.endpoint}/{project_id}/requests/{request_id}"
        return await self.get(url)

    async def get_project_usage_summary(self, project_id: str, options: UsageSummaryOptionsV1) -> UsageSummaryResponse:
        url = f"{self.url}/{self.endpoint}/{project_id}/usage"
        return await self.get(url, options)

    async def get_project_usage_fields(self, project_id: str, options: UsageFieldsOptionsV1) -> UsageFieldsResponse:
        url = f"{self.url}/{self.endpoint}/{project_id}/usage/fields"
        return await self.get(url, options)

    async def get_project_balances(self, project_id: str) -> BalancesResponse:
        url = f"{self.url}/{self.endpoint}/{project_id}/balances"
        return await self.get(url)

    async def get_project_balance(self, project_id: str, balance_id: str) -> Balance:
        url = f"{self.url}/{self.endpoint}/{project_id}/balances/{balance_id}"
        return await self.get(url)
