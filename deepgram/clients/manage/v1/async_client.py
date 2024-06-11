# Copyright 2023-2024 Deepgram SDK contributors. All Rights Reserved.
# Use of this source code is governed by a MIT license that can be found in the LICENSE file.
# SPDX-License-Identifier: MIT

import logging
from typing import Dict, Union, Optional

import httpx

from deepgram.utils import verboselogs
from ....options import DeepgramClientOptions
from ...abstract_async_client import AbstractAsyncRestClient

from .response import (
    Message,
    Project,
    ProjectsResponse,
    MembersResponse,
    Key,
    KeyResponse,
    KeysResponse,
    ScopesResponse,
    InvitesResponse,
    UsageRequest,
    UsageRequestsResponse,
    UsageSummaryResponse,
    UsageFieldsResponse,
    Balance,
    BalancesResponse,
)
from .options import (
    ProjectOptions,
    KeyOptions,
    ScopeOptions,
    InviteOptions,
    UsageRequestOptions,
    UsageSummaryOptions,
    UsageFieldsOptions,
)


class AsyncManageClient(
    AbstractAsyncRestClient
):  # pylint: disable=too-many-public-methods
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
    """

    _logger: verboselogs.VerboseLogger
    _config: DeepgramClientOptions
    _endpoint: str

    def __init__(self, config: DeepgramClientOptions):
        self._logger = verboselogs.VerboseLogger(__name__)
        self._logger.addHandler(logging.StreamHandler())
        self._logger.setLevel(config.verbose)
        self._config = config
        self._endpoint = "v1/projects"
        super().__init__(config)

    # projects
    async def list_projects(
        self,
        timeout: Optional[httpx.Timeout] = None,
        addons: Optional[Dict] = None,
        headers: Optional[Dict] = None,
        **kwargs,
    ) -> ProjectsResponse:
        """
        Please see get_projects for more information.
        """
        return await self.get_projects(
            timeout=timeout, addons=addons, headers=headers, **kwargs
        )

    async def get_projects(
        self,
        timeout: Optional[httpx.Timeout] = None,
        addons: Optional[Dict] = None,
        headers: Optional[Dict] = None,
        **kwargs,
    ) -> ProjectsResponse:
        """
        Gets a list of projects for the authenticated user.

        Reference:
        https://developers.deepgram.com/reference/get-projects
        """
        self._logger.debug("ManageClient.get_projects ENTER")
        url = f"{self._config.url}/{self._endpoint}"
        self._logger.info("url: %s", url)
        self._logger.info("addons: %s", addons)
        self._logger.info("headers: %s", headers)
        result = await self.get(
            url, timeout=timeout, addons=addons, headers=headers, **kwargs
        )
        self._logger.info("result: %s", result)
        res = ProjectsResponse.from_json(result)
        self._logger.verbose("result: %s", res)
        self._logger.notice("get_projects succeeded")
        self._logger.debug("ManageClient.get_projects LEAVE")
        return res

    async def get_project(
        self,
        project_id: str,
        timeout: Optional[httpx.Timeout] = None,
        addons: Optional[Dict] = None,
        headers: Optional[Dict] = None,
        **kwargs,
    ) -> Project:
        """
        Gets details for a specific project.

        Reference:
        https://developers.deepgram.com/reference/get-project
        """
        self._logger.debug("ManageClient.get_project ENTER")
        url = f"{self._config.url}/{self._endpoint}/{project_id}"
        self._logger.info("url: %s", url)
        self._logger.info("project_id: %s", project_id)
        self._logger.info("addons: %s", addons)
        self._logger.info("headers: %s", headers)
        result = await self.get(
            url, timeout=timeout, addons=addons, headers=headers, **kwargs
        )
        self._logger.info("result: %s", result)
        res = Project.from_json(result)
        self._logger.verbose("result: %s", res)
        self._logger.notice("get_project succeeded")
        self._logger.debug("ManageClient.get_project LEAVE")
        return res

    async def update_project_option(
        self,
        project_id: str,
        options: Union[Dict, ProjectOptions],
        timeout: Optional[httpx.Timeout] = None,
        addons: Optional[Dict] = None,
        headers: Optional[Dict] = None,
        **kwargs,
    ) -> Message:
        """
        Updates a project's settings.

        Reference:
        https://developers.deepgram.com/reference/update-project
        """
        self._logger.debug("ManageClient.update_project_option ENTER")
        url = f"{self._config.url}/{self._endpoint}/{project_id}"
        self._logger.info("url: %s", url)
        self._logger.info("project_id: %s", project_id)
        if isinstance(options, ProjectOptions):
            self._logger.info("ProjectOptions switching class -> dict")
            options = options.to_dict()
        self._logger.info("options: %s", options)
        self._logger.info("addons: %s", addons)
        self._logger.info("headers: %s", headers)
        result = await self.patch(
            url, json=options, timeout=timeout, addons=addons, headers=headers, **kwargs
        )
        self._logger.info("result: %s", result)
        res = Message.from_json(result)
        self._logger.verbose("result: %s", res)
        self._logger.notice("update_project_option succeeded")
        self._logger.debug("ManageClient.update_project_option LEAVE")
        return res

    async def update_project(
        self,
        project_id: str,
        name="",
        timeout: Optional[httpx.Timeout] = None,
        addons: Optional[Dict] = None,
        headers: Optional[Dict] = None,
        **kwargs,
    ) -> Message:
        """
        Updates a project's settings.

        Reference:
        https://developers.deepgram.com/reference/update-project
        """
        self._logger.debug("ManageClient.update_project ENTER")
        url = f"{self._config.url}/{self._endpoint}/{project_id}"
        options = {
            "name": name,
        }
        self._logger.info("url: %s", url)
        self._logger.info("project_id: %s", project_id)
        self._logger.info("options: %s", options)
        self._logger.info("addons: %s", addons)
        self._logger.info("headers: %s", headers)
        result = await self.patch(
            url, json=options, timeout=timeout, addons=addons, headers=headers, **kwargs
        )
        self._logger.info("result: %s", result)
        res = Message.from_json(result)
        self._logger.verbose("result: %s", res)
        self._logger.notice("update_project succeeded")
        self._logger.debug("ManageClient.update_project LEAVE")
        return res

    async def delete_project(
        self,
        project_id: str,
        timeout: Optional[httpx.Timeout] = None,
        addons: Optional[Dict] = None,
        headers: Optional[Dict] = None,
        **kwargs,
    ) -> Message:
        """
        Deletes a project.

        Reference:
        https://developers.deepgram.com/reference/delete-project
        """
        self._logger.debug("ManageClient.delete_project ENTER")
        url = f"{self._config.url}/{self._endpoint}/{project_id}"
        self._logger.info("addons: %s", addons)
        self._logger.info("headers: %s", headers)
        result = await self.delete(
            url, timeout=timeout, addons=addons, headers=headers, **kwargs
        )
        self._logger.info("result: %s", result)
        res = Message.from_json(result)
        self._logger.verbose("result: %s", res)
        self._logger.notice("delete_project succeeded")
        self._logger.debug("ManageClient.delete_project LEAVE")
        return res

    # keys
    async def list_keys(
        self,
        project_id: str,
        timeout: Optional[httpx.Timeout] = None,
        addons: Optional[Dict] = None,
        headers: Optional[Dict] = None,
        **kwargs,
    ) -> KeysResponse:
        """
        Please see get_keys for more information.
        """
        return await self.get_keys(
            project_id, timeout=timeout, addons=addons, headers=headers, **kwargs
        )

    async def get_keys(
        self,
        project_id: str,
        timeout: Optional[httpx.Timeout] = None,
        addons: Optional[Dict] = None,
        headers: Optional[Dict] = None,
        **kwargs,
    ) -> KeysResponse:
        """
        Gets a list of keys for a project.

        Reference:
        https://developers.deepgram.com/reference/list-keys
        """
        self._logger.debug("ManageClient.get_keys ENTER")
        url = f"{self._config.url}/{self._endpoint}/{project_id}/keys"
        self._logger.info("url: %s", url)
        self._logger.info("project_id: %s", project_id)
        self._logger.info("addons: %s", addons)
        self._logger.info("headers: %s", headers)
        result = await self.get(
            url, timeout=timeout, addons=addons, headers=headers, **kwargs
        )
        self._logger.info("result: %s", result)
        res = KeysResponse.from_json(result)
        self._logger.verbose("result: %s", res)
        self._logger.notice("get_keys succeeded")
        self._logger.debug("ManageClient.get_keys LEAVE")
        return res

    async def get_key(
        self,
        project_id: str,
        key_id: str,
        timeout: Optional[httpx.Timeout] = None,
        addons: Optional[Dict] = None,
        headers: Optional[Dict] = None,
        **kwargs,
    ) -> KeyResponse:
        """
        Gets details for a specific key.

        Reference:
        https://developers.deepgram.com/reference/get-key
        """
        self._logger.debug("ManageClient.get_key ENTER")
        url = f"{self._config.url}/{self._endpoint}/{project_id}/keys/{key_id}"
        self._logger.info("url: %s", url)
        self._logger.info("project_id: %s", project_id)
        self._logger.info("key_id: %s", key_id)
        self._logger.info("addons: %s", addons)
        self._logger.info("headers: %s", headers)
        result = await self.get(
            url, timeout=timeout, addons=addons, headers=headers, **kwargs
        )
        self._logger.info("result: %s", result)
        res = KeyResponse.from_json(result)
        self._logger.verbose("result: %s", res)
        self._logger.notice("get_key succeeded")
        self._logger.debug("ManageClient.get_key LEAVE")
        return res

    async def create_key(
        self,
        project_id: str,
        options: Union[Dict, KeyOptions],
        timeout: Optional[httpx.Timeout] = None,
        addons: Optional[Dict] = None,
        headers: Optional[Dict] = None,
        **kwargs,
    ) -> Key:
        """
        Creates a new key.

        Reference:
        https://developers.deepgram.com/reference/create-key
        """
        self._logger.debug("ManageClient.create_key ENTER")
        url = f"{self._config.url}/{self._endpoint}/{project_id}/keys"
        self._logger.info("url: %s", url)
        self._logger.info("project_id: %s", project_id)
        if isinstance(options, KeyOptions):
            self._logger.info("KeyOptions switching class -> dict")
            options = options.to_dict()
        self._logger.info("options: %s", options)
        self._logger.info("addons: %s", addons)
        self._logger.info("headers: %s", headers)
        result = await self.post(
            url, json=options, timeout=timeout, addons=addons, headers=headers, **kwargs
        )
        self._logger.info("result: %s", result)
        res = Key.from_json(result)
        self._logger.verbose("result: %s", res)
        self._logger.notice("create_key succeeded")
        self._logger.debug("ManageClient.create_key LEAVE")
        return res

    async def delete_key(
        self,
        project_id: str,
        key_id: str,
        timeout: Optional[httpx.Timeout] = None,
        addons: Optional[Dict] = None,
        headers: Optional[Dict] = None,
        **kwargs,
    ) -> Message:
        """
        Deletes a key.

        Reference:
        https://developers.deepgram.com/reference/delete-key
        """
        self._logger.debug("ManageClient.delete_key ENTER")
        url = f"{self._config.url}/{self._endpoint}/{project_id}/keys/{key_id}"
        self._logger.info("url: %s", url)
        self._logger.info("project_id: %s", project_id)
        self._logger.info("key_id: %s", key_id)
        self._logger.info("addons: %s", addons)
        self._logger.info("headers: %s", headers)
        result = await self.delete(
            url, timeout=timeout, addons=addons, headers=headers, **kwargs
        )
        self._logger.info("result: %s", result)
        res = Message.from_json(result)
        self._logger.verbose("result: %s", res)
        self._logger.notice("delete_key succeeded")
        self._logger.debug("ManageClient.delete_key LEAVE")
        return res

    # members
    async def list_members(
        self,
        project_id: str,
        timeout: Optional[httpx.Timeout] = None,
        addons: Optional[Dict] = None,
        headers: Optional[Dict] = None,
        **kwargs,
    ) -> MembersResponse:
        """
        Please see get_members for more information.
        """
        return await self.get_members(
            project_id, timeout=timeout, addons=addons, headers=headers, **kwargs
        )

    async def get_members(
        self,
        project_id: str,
        timeout: Optional[httpx.Timeout] = None,
        addons: Optional[Dict] = None,
        headers: Optional[Dict] = None,
        **kwargs,
    ) -> MembersResponse:
        """
        Gets a list of members for a project.

        Reference:
        https://developers.deepgram.com/reference/get-members
        """
        self._logger.debug("ManageClient.get_members ENTER")
        url = f"{self._config.url}/{self._endpoint}/{project_id}/members"
        self._logger.info("url: %s", url)
        self._logger.info("project_id: %s", project_id)
        self._logger.info("addons: %s", addons)
        self._logger.info("headers: %s", headers)
        result = await self.get(
            url, timeout=timeout, addons=addons, headers=headers, **kwargs
        )
        self._logger.info("result: %s", result)
        res = MembersResponse.from_json(result)
        self._logger.verbose("result: %s", res)
        self._logger.notice("get_members succeeded")
        self._logger.debug("ManageClient.get_members LEAVE")
        return res

    async def remove_member(
        self,
        project_id: str,
        member_id: str,
        timeout: Optional[httpx.Timeout] = None,
        addons: Optional[Dict] = None,
        headers: Optional[Dict] = None,
        **kwargs,
    ) -> Message:
        """
        Removes a member from a project.

        Reference:
        https://developers.deepgram.com/reference/remove-member
        """
        self._logger.debug("ManageClient.remove_member ENTER")
        url = f"{self._config.url}/{self._endpoint}/{project_id}/members/{member_id}"
        self._logger.info("url: %s", url)
        self._logger.info("project_id: %s", project_id)
        self._logger.info("member_id: %s", member_id)
        self._logger.info("addons: %s", addons)
        self._logger.info("headers: %s", headers)
        result = await self.delete(
            url, timeout=timeout, addons=addons, headers=headers, **kwargs
        )
        self._logger.info("result: %s", result)
        res = Message.from_json(result)
        self._logger.verbose("result: %s", res)
        self._logger.notice("remove_member succeeded")
        self._logger.debug("ManageClient.remove_member LEAVE")
        return res

    # scopes
    async def get_member_scopes(
        self,
        project_id: str,
        member_id: str,
        timeout: Optional[httpx.Timeout] = None,
        addons: Optional[Dict] = None,
        headers: Optional[Dict] = None,
        **kwargs,
    ) -> ScopesResponse:
        """
        Gets a list of scopes for a member.

        Reference:
        https://developers.deepgram.com/reference/get-member-scopes
        """
        self._logger.debug("ManageClient.get_member_scopes ENTER")
        url = f"{self._config.url}/{self._endpoint}/{project_id}/members/{member_id}/scopes"
        self._logger.info("url: %s", url)
        self._logger.info("project_id: %s", project_id)
        self._logger.info("member_id: %s", member_id)
        self._logger.info("addons: %s", addons)
        self._logger.info("headers: %s", headers)
        result = await self.get(
            url, timeout=timeout, addons=addons, headers=headers, **kwargs
        )
        self._logger.info("result: %s", result)
        res = ScopesResponse.from_json(result)
        self._logger.verbose("result: %s", res)
        self._logger.notice("get_member_scopes succeeded")
        self._logger.debug("ManageClient.get_member_scopes LEAVE")
        return res

    async def update_member_scope(
        self,
        project_id: str,
        member_id: str,
        options: Union[Dict, ScopeOptions],
        timeout: Optional[httpx.Timeout] = None,
        addons: Optional[Dict] = None,
        headers: Optional[Dict] = None,
        **kwargs,
    ) -> Message:
        """
        Updates a member's scopes.

        Reference:
        https://developers.deepgram.com/reference/update-scope
        """
        self._logger.debug("ManageClient.update_member_scope ENTER")
        url = f"{self._config.url}/{self._endpoint}/{project_id}/members/{member_id}/scopes"
        self._logger.info("url: %s", url)
        self._logger.info("project_id: %s", project_id)
        if isinstance(options, ScopeOptions):
            self._logger.info("ScopeOptions switching class -> dict")
            options = options.to_dict()
        self._logger.info("options: %s", options)
        self._logger.info("addons: %s", addons)
        self._logger.info("headers: %s", headers)
        result = await self.put(
            url, json=options, timeout=timeout, addons=addons, headers=headers, **kwargs
        )
        self._logger.info("result: %s", result)
        res = Message.from_json(result)
        self._logger.verbose("result: %s", res)
        self._logger.notice("update_member_scope succeeded")
        self._logger.debug("ManageClient.update_member_scope LEAVE")
        return res

    # invites
    async def list_invites(
        self,
        project_id: str,
        timeout: Optional[httpx.Timeout] = None,
        addons: Optional[Dict] = None,
        headers: Optional[Dict] = None,
        **kwargs,
    ) -> InvitesResponse:
        """
        Please see get_invites for more information.
        """
        return await self.get_invites(
            project_id, timeout=timeout, addons=addons, headers=headers, **kwargs
        )

    async def get_invites(
        self,
        project_id: str,
        timeout: Optional[httpx.Timeout] = None,
        addons: Optional[Dict] = None,
        headers: Optional[Dict] = None,
        **kwargs,
    ) -> InvitesResponse:
        """
        Gets a list of invites for a project.

        Reference:
        https://developers.deepgram.com/reference/list-invites
        """
        self._logger.debug("ManageClient.get_invites ENTER")
        url = f"{self._config.url}/{self._endpoint}/{project_id}/invites"
        self._logger.info("url: %s", url)
        self._logger.info("project_id: %s", project_id)
        self._logger.info("addons: %s", addons)
        self._logger.info("headers: %s", headers)
        result = await self.get(
            url, timeout=timeout, addons=addons, headers=headers, **kwargs
        )
        self._logger.info("result: %s", result)
        res = InvitesResponse.from_json(result)
        self._logger.verbose("result: %s", res)
        self._logger.notice("get_invites succeeded")
        self._logger.debug("ManageClient.get_invites LEAVE")
        return res

    async def send_invite_options(
        self,
        project_id: str,
        options: Union[Dict, InviteOptions],
        timeout: Optional[httpx.Timeout] = None,
        addons: Optional[Dict] = None,
        headers: Optional[Dict] = None,
        **kwargs,
    ) -> Message:
        """
        Sends an invite to a project.

        Reference:
        https://developers.deepgram.com/reference/send-invite
        """
        self._logger.debug("ManageClient.send_invite_options ENTER")
        url = f"{self._config.url}/{self._endpoint}/{project_id}/invites"
        self._logger.info("url: %s", url)
        self._logger.info("project_id: %s", project_id)
        if isinstance(options, InviteOptions):
            self._logger.info("InviteOptions switching class -> dict")
            options = options.to_dict()
        self._logger.info("options: %s", options)
        self._logger.info("addons: %s", addons)
        self._logger.info("headers: %s", headers)
        result = await self.post(
            url, json=options, timeout=timeout, addons=addons, headers=headers, **kwargs
        )
        self._logger.info("result: %s", result)
        res = Message.from_json(result)
        self._logger.verbose("result: %s", res)
        self._logger.notice("send_invite_options succeeded")
        self._logger.debug("ManageClient.send_invite_options LEAVE")
        return res

    async def send_invite(
        self,
        project_id: str,
        email: str,
        scope="member",
        timeout: Optional[httpx.Timeout] = None,
        addons: Optional[Dict] = None,
        headers: Optional[Dict] = None,
        **kwargs,
    ) -> Message:
        """
        Sends an invite to a project.

        Reference:
        https://developers.deepgram.com/reference/send-invite
        """
        self._logger.debug("ManageClient.send_invite ENTER")
        url = f"{self._config.url}/{self._endpoint}/{project_id}/invites"
        options = {
            "email": email,
            "scope": scope,
        }
        self._logger.info("url: %s", url)
        self._logger.info("project_id: %s", project_id)
        self._logger.info("options: %s", options)
        self._logger.info("addons: %s", addons)
        self._logger.info("headers: %s", headers)
        result = await self.post(
            url, json=options, timeout=timeout, addons=addons, headers=headers, **kwargs
        )
        self._logger.info("result: %s", result)
        res = Message.from_json(result)
        self._logger.verbose("result: %s", res)
        self._logger.notice("send_invite succeeded")
        self._logger.debug("ManageClient.send_invite LEAVE")
        return res

    async def delete_invite(
        self,
        project_id: str,
        email: str,
        timeout: Optional[httpx.Timeout] = None,
        addons: Optional[Dict] = None,
        headers: Optional[Dict] = None,
        **kwargs,
    ) -> Message:
        """
        Deletes an invite from a project.

        Reference:
        https://developers.deepgram.com/reference/delete-invite
        """
        self._logger.debug("ManageClient.delete_invite ENTER")
        url = f"{self._config.url}/{self._endpoint}/{project_id}/invites/{email}"
        self._logger.info("url: %s", url)
        self._logger.info("project_id: %s", project_id)
        self._logger.info("email: %s", email)
        self._logger.info("addons: %s", addons)
        self._logger.info("headers: %s", headers)
        result = await self.delete(
            url, timeout=timeout, addons=addons, headers=headers, **kwargs
        )
        self._logger.info("result: %s", result)
        res = Message.from_json(result)
        self._logger.verbose("result: %s", res)
        self._logger.notice("delete_invite succeeded")
        self._logger.debug("ManageClient.delete_invite LEAVE")
        return res

    async def leave_project(
        self,
        project_id: str,
        timeout: Optional[httpx.Timeout] = None,
        addons: Optional[Dict] = None,
        headers: Optional[Dict] = None,
        **kwargs,
    ) -> Message:
        """
        Leaves a project.

        Reference:
        https://developers.deepgram.com/reference/leave-project
        """
        self._logger.debug("ManageClient.leave_project ENTER")
        url = f"{self._config.url}/{self._endpoint}/{project_id}/leave"
        self._logger.info("url: %s", url)
        self._logger.info("project_id: %s", project_id)
        self._logger.info("addons: %s", addons)
        self._logger.info("headers: %s", headers)
        result = await self.delete(
            url, timeout=timeout, addons=addons, headers=headers, **kwargs
        )
        self._logger.info("result: %s", result)
        res = Message.from_json(result)
        self._logger.verbose("result: %s", res)
        self._logger.notice("leave_project succeeded")
        self._logger.debug("ManageClient.leave_project LEAVE")
        return res

    # usage
    async def get_usage_requests(
        self,
        project_id: str,
        options: Union[Dict, UsageRequestOptions],
        timeout: Optional[httpx.Timeout] = None,
        addons: Optional[Dict] = None,
        headers: Optional[Dict] = None,
        **kwargs,
    ) -> UsageRequestsResponse:
        """
        Gets a list of usage requests for a project.

        Reference:
        https://developers.deepgram.com/reference/get-all-requests
        """
        self._logger.debug("ManageClient.get_usage_requests ENTER")
        url = f"{self._config.url}/{self._endpoint}/{project_id}/requests"
        self._logger.info("url: %s", url)
        self._logger.info("project_id: %s", project_id)
        if isinstance(options, UsageRequestOptions):
            self._logger.info("UsageRequestOptions switching class -> dict")
            options = options.to_dict()
        self._logger.info("options: %s", options)
        self._logger.info("addons: %s", addons)
        self._logger.info("headers: %s", headers)
        result = await self.get(
            url,
            options=options,
            timeout=timeout,
            addons=addons,
            headers=headers,
            **kwargs,
        )
        self._logger.info("result: %s", result)
        res = UsageRequestsResponse.from_json(result)
        self._logger.verbose("result: %s", res)
        self._logger.notice("get_usage_requests succeeded")
        self._logger.debug("ManageClient.get_usage_requests LEAVE")
        return res

    async def get_usage_request(
        self,
        project_id: str,
        request_id: str,
        timeout: Optional[httpx.Timeout] = None,
        addons: Optional[Dict] = None,
        headers: Optional[Dict] = None,
        **kwargs,
    ) -> UsageRequest:
        """
        Gets details for a specific usage request.

        Reference:
        https://developers.deepgram.com/reference/get-request
        """
        self._logger.debug("ManageClient.get_usage_request ENTER")
        url = f"{self._config.url}/{self._endpoint}/{project_id}/requests/{request_id}"
        self._logger.info("url: %s", url)
        self._logger.info("project_id: %s", project_id)
        self._logger.info("request_id: %s", request_id)
        self._logger.info("addons: %s", addons)
        self._logger.info("headers: %s", headers)
        result = await self.get(
            url, timeout=timeout, addons=addons, headers=headers, **kwargs
        )
        self._logger.info("result: %s", result)
        res = UsageRequest.from_json(result)
        self._logger.verbose("result: %s", res)
        self._logger.notice("get_usage_request succeeded")
        self._logger.debug("ManageClient.get_usage_request LEAVE")
        return res

    async def get_usage_summary(
        self,
        project_id: str,
        options: Union[Dict, UsageSummaryOptions],
        timeout: Optional[httpx.Timeout] = None,
        addons: Optional[Dict] = None,
        headers: Optional[Dict] = None,
        **kwargs,
    ) -> UsageSummaryResponse:
        """
        Gets a summary of usage for a project.

        Reference:
        https://developers.deepgram.com/reference/summarize-usage
        """
        self._logger.debug("ManageClient.get_usage_summary ENTER")
        url = f"{self._config.url}/{self._endpoint}/{project_id}/usage"
        self._logger.info("url: %s", url)
        self._logger.info("project_id: %s", project_id)
        if isinstance(options, UsageSummaryOptions):
            self._logger.info("UsageSummaryOptions switching class -> dict")
            options = options.to_dict()
        self._logger.info("options: %s", options)
        self._logger.info("addons: %s", addons)
        self._logger.info("headers: %s", headers)
        result = await self.get(
            url,
            options=options,
            timeout=timeout,
            addons=addons,
            headers=headers,
            **kwargs,
        )
        self._logger.info("result: %s", result)
        res = UsageSummaryResponse.from_json(result)
        self._logger.verbose("result: %s", res)
        self._logger.notice("get_usage_summary succeeded")
        self._logger.debug("ManageClient.get_usage_summary LEAVE")
        return res

    async def get_usage_fields(
        self,
        project_id: str,
        options: Union[Dict, UsageFieldsOptions],
        timeout: Optional[httpx.Timeout] = None,
        addons: Optional[Dict] = None,
        headers: Optional[Dict] = None,
        **kwargs,
    ) -> UsageFieldsResponse:
        """
        Gets a list of usage fields for a project.

        Reference:
        https://developers.deepgram.com/reference/get-fields
        """
        self._logger.debug("ManageClient.get_usage_fields ENTER")
        url = f"{self._config.url}/{self._endpoint}/{project_id}/usage/fields"
        self._logger.info("url: %s", url)
        self._logger.info("project_id: %s", project_id)
        if isinstance(options, UsageFieldsOptions):
            self._logger.info("UsageFieldsOptions switching class -> dict")
            options = options.to_dict()
        self._logger.info("options: %s", options)
        self._logger.info("addons: %s", addons)
        self._logger.info("headers: %s", headers)
        result = await self.get(
            url,
            options=options,
            timeout=timeout,
            addons=addons,
            headers=headers,
            **kwargs,
        )
        self._logger.info("result: %s", result)
        res = UsageFieldsResponse.from_json(result)
        self._logger.verbose("result: %s", res)
        self._logger.notice("get_usage_fields succeeded")
        self._logger.debug("ManageClient.get_usage_fields LEAVE")
        return res

    # balances
    async def list_balances(
        self,
        project_id: str,
        timeout: Optional[httpx.Timeout] = None,
        addons: Optional[Dict] = None,
        headers: Optional[Dict] = None,
        **kwargs,
    ) -> BalancesResponse:
        """
        Please see get_balances for more information.
        """
        return await self.get_balances(
            project_id, timeout=timeout, addons=addons, headers=headers, **kwargs
        )

    async def get_balances(
        self,
        project_id: str,
        timeout: Optional[httpx.Timeout] = None,
        addons: Optional[Dict] = None,
        headers: Optional[Dict] = None,
        **kwargs,
    ) -> BalancesResponse:
        """
        Gets a list of balances for a project.

        Reference:
        https://developers.deepgram.com/reference/get-all-balances
        """
        self._logger.debug("ManageClient.get_balances ENTER")
        url = f"{self._config.url}/{self._endpoint}/{project_id}/balances"
        self._logger.info("url: %s", url)
        self._logger.info("project_id: %s", project_id)
        self._logger.info("addons: %s", addons)
        self._logger.info("headers: %s", headers)
        result = await self.get(
            url, timeout=timeout, addons=addons, headers=headers, **kwargs
        )
        self._logger.info("result: %s", result)
        res = BalancesResponse.from_json(result)
        self._logger.verbose("result: %s", res)
        self._logger.notice("get_balances succeeded")
        self._logger.debug("ManageClient.get_balances LEAVE")
        return res

    async def get_balance(
        self,
        project_id: str,
        balance_id: str,
        timeout: Optional[httpx.Timeout] = None,
        addons: Optional[Dict] = None,
        headers: Optional[Dict] = None,
        **kwargs,
    ) -> Balance:
        """
        Gets details for a specific balance.

        Reference:
        https://developers.deepgram.com/reference/get-balance
        """
        self._logger.debug("ManageClient.get_balance ENTER")
        url = f"{self._config.url}/{self._endpoint}/{project_id}/balances/{balance_id}"
        self._logger.info("url: %s", url)
        self._logger.info("project_id: %s", project_id)
        self._logger.info("balance_id: %s", balance_id)
        self._logger.info("addons: %s", addons)
        self._logger.info("headers: %s", headers)
        result = await self.get(
            url, timeout=timeout, addons=addons, headers=headers, **kwargs
        )
        self._logger.info("result: %s", result)
        res = Balance.from_json(result)
        self._logger.verbose("result: %s", res)
        self._logger.notice("get_balance succeeded")
        self._logger.debug("ManageClient.get_balance LEAVE")
        return res
