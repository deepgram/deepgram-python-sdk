# Copyright 2023 Deepgram SDK contributors. All Rights Reserved.
# Use of this source code is governed by a MIT license that can be found in the LICENSE file.
# SPDX-License-Identifier: MIT

import logging, verboselogs

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


class AsyncManageClient(AbstractAsyncRestClient):
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

    def __init__(self, config: DeepgramClientOptions):
        self.logger = logging.getLogger(__name__)
        self.logger.addHandler(logging.StreamHandler())
        self.logger.setLevel(config.verbose)
        self.config = config
        self.endpoint = "v1/projects"
        super().__init__(config)

    # projects
    async def list_projects(self, addons: dict = None, **kwargs) -> ProjectsResponse:
        """
        Please see get_projects for more information.
        """
        return self.get_projects(addons=addons, **kwargs)

    async def get_projects(self, addons: dict = None, **kwargs) -> ProjectsResponse:
        """
        Gets a list of projects for the authenticated user.

        Reference:
        https://developers.deepgram.com/reference/get-projects
        """
        self.logger.debug("ManageClient.get_projects ENTER")
        url = f"{self.config.url}/{self.endpoint}"
        self.logger.info("url: %s", url)
        self.logger.info("addons: %s", addons)
        result = await self.get(url, addons=addons, **kwargs)
        self.logger.info("result: %s", result)
        res = ProjectsResponse.from_json(result)
        self.logger.verbose("result: %s", res)
        self.logger.notice("get_projects succeeded")
        self.logger.debug("ManageClient.get_projects LEAVE")
        return res

    async def get_project(
        self, project_id: str, addons: dict = None, **kwargs
    ) -> Project:
        """
        Gets details for a specific project.

        Reference:
        https://developers.deepgram.com/reference/get-project
        """
        self.logger.debug("ManageClient.get_project ENTER")
        url = f"{self.config.url}/{self.endpoint}/{project_id}"
        self.logger.info("url: %s", url)
        self.logger.info("project_id: %s", project_id)
        self.logger.info("addons: %s", addons)
        result = await self.get(url, addons=addons, **kwargs)
        self.logger.info("result: %s", result)
        res = Project.from_json(result)
        self.logger.verbose("result: %s", res)
        self.logger.notice("get_project succeeded")
        self.logger.debug("ManageClient.get_project LEAVE")
        return res

    async def update_project_option(
        self, project_id: str, options: ProjectOptions, addons: dict = None, **kwargs
    ) -> Message:
        """
        Updates a project's settings.

        Reference:
        https://developers.deepgram.com/reference/update-project
        """
        self.logger.debug("ManageClient.update_project_option ENTER")
        url = f"{self.config.url}/{self.endpoint}/{project_id}"
        self.logger.info("url: %s", url)
        self.logger.info("project_id: %s", project_id)
        self.logger.info("options: %s", options)
        self.logger.info("addons: %s", addons)
        result = await self.patch(url, json=options, addons=addons, **kwargs)
        self.logger.info("result: %s", result)
        res = Message.from_json(result)
        self.logger.verbose("result: %s", res)
        self.logger.notice("update_project_option succeeded")
        self.logger.debug("ManageClient.update_project_option LEAVE")
        return res

    async def update_project(
        self, project_id: str, name="", addons: dict = None, **kwargs
    ) -> Message:
        """
        Updates a project's settings.

        Reference:
        https://developers.deepgram.com/reference/update-project
        """
        self.logger.debug("ManageClient.update_project ENTER")
        url = f"{self.config.url}/{self.endpoint}/{project_id}"
        options: ProjectOptions = {
            "name": name,
        }
        self.logger.info("url: %s", url)
        self.logger.info("project_id: %s", project_id)
        self.logger.info("options: %s", options)
        self.logger.info("addons: %s", addons)
        result = await self.patch(url, json=options, addons=addons, **kwargs)
        self.logger.info("result: %s", result)
        res = Message.from_json(result)
        self.logger.verbose("result: %s", res)
        self.logger.notice("update_project succeeded")
        self.logger.debug("ManageClient.update_project LEAVE")
        return res

    async def delete_project(
        self, project_id: str, addons: dict = None, **kwargs
    ) -> Message:
        """
        Deletes a project.

        Reference:
        https://developers.deepgram.com/reference/delete-project
        """
        self.logger.debug("ManageClient.delete_project ENTER")
        url = f"{self.config.url}/{self.endpoint}/{project_id}"
        self.logger.info("addons: %s", addons)
        result = await self.delete(url, addons=addons, **kwargs)
        self.logger.info("result: %s", result)
        res = Message.from_json(result)
        self.logger.verbose("result: %s", res)
        self.logger.notice("delete_project succeeded")
        self.logger.debug("ManageClient.delete_project LEAVE")
        return res

    # keys
    async def list_keys(
        self, project_id: str, addons: dict = None, **kwargs
    ) -> KeysResponse:
        """
        Please see get_keys for more information.
        """
        return self.get_keys(project_id, addons=addons, **kwargs)

    async def get_keys(
        self, project_id: str, addons: dict = None, **kwargs
    ) -> KeysResponse:
        """
        Gets a list of keys for a project.

        Reference:
        https://developers.deepgram.com/reference/list-keys
        """
        self.logger.debug("ManageClient.get_keys ENTER")
        url = f"{self.config.url}/{self.endpoint}/{project_id}/keys"
        self.logger.info("url: %s", url)
        self.logger.info("project_id: %s", project_id)
        self.logger.info("addons: %s", addons)
        result = await self.get(url, addons=addons, **kwargs)
        self.logger.info("result: %s", result)
        res = KeysResponse.from_json(result)
        self.logger.verbose("result: %s", res)
        self.logger.notice("get_keys succeeded")
        self.logger.debug("ManageClient.get_keys LEAVE")
        return res

    async def get_key(
        self, project_id: str, key_id: str, addons: dict = None, **kwargs
    ) -> KeyResponse:
        """
        Gets details for a specific key.

        Reference:
        https://developers.deepgram.com/reference/get-key
        """
        self.logger.debug("ManageClient.get_key ENTER")
        url = f"{self.config.url}/{self.endpoint}/{project_id}/keys/{key_id}"
        self.logger.info("url: %s", url)
        self.logger.info("project_id: %s", project_id)
        self.logger.info("key_id: %s", key_id)
        self.logger.info("addons: %s", addons)
        result = await self.get(url, addons=addons, **kwargs)
        self.logger.info("result: %s", result)
        res = KeyResponse.from_json(result)
        self.logger.verbose("result: %s", res)
        self.logger.notice("get_key succeeded")
        self.logger.debug("ManageClient.get_key LEAVE")
        return res

    async def create_key(
        self, project_id: str, options: KeyOptions, addons: dict = None, **kwargs
    ) -> Key:
        """
        Creates a new key.

        Reference:
        https://developers.deepgram.com/reference/create-key
        """
        self.logger.debug("ManageClient.create_key ENTER")
        url = f"{self.config.url}/{self.endpoint}/{project_id}/keys"
        self.logger.info("url: %s", url)
        self.logger.info("project_id: %s", project_id)
        self.logger.info("options: %s", options)
        self.logger.info("addons: %s", addons)
        result = await self.post(url, json=options, addons=addons, **kwargs)
        self.logger.info("result: %s", result)
        res = Key.from_json(result)
        self.logger.verbose("result: %s", res)
        self.logger.notice("create_key succeeded")
        self.logger.debug("ManageClient.create_key LEAVE")
        return res

    async def delete_key(
        self, project_id: str, key_id: str, addons: dict = None, **kwargs
    ) -> Message:
        """
        Deletes a key.

        Reference:
        https://developers.deepgram.com/reference/delete-key
        """
        self.logger.debug("ManageClient.delete_key ENTER")
        url = f"{self.config.url}/{self.endpoint}/{project_id}/keys/{key_id}"
        self.logger.info("url: %s", url)
        self.logger.info("project_id: %s", project_id)
        self.logger.info("key_id: %s", key_id)
        self.logger.info("addons: %s", addons)
        result = await self.delete(url, addons=addons, **kwargs)
        self.logger.info("result: %s", result)
        res = Message.from_json(result)
        self.logger.verbose("result: %s", res)
        self.logger.notice("delete_key succeeded")
        self.logger.debug("ManageClient.delete_key LEAVE")
        return res

    # members
    async def list_members(
        self, project_id: str, addons: dict = None, **kwargs
    ) -> MembersResponse:
        """
        Please see get_members for more information.
        """
        return self.get_members(project_id, addons=addons, **kwargs)

    async def get_members(
        self, project_id: str, addons: dict = None, **kwargs
    ) -> MembersResponse:
        """
        Gets a list of members for a project.

        Reference:
        https://developers.deepgram.com/reference/get-members
        """
        self.logger.debug("ManageClient.get_members ENTER")
        url = f"{self.config.url}/{self.endpoint}/{project_id}/members"
        self.logger.info("url: %s", url)
        self.logger.info("project_id: %s", project_id)
        self.logger.info("addons: %s", addons)
        result = await self.get(url, addons=addons, **kwargs)
        self.logger.info("result: %s", result)
        res = MembersResponse.from_json(result)
        self.logger.verbose("result: %s", res)
        self.logger.notice("get_members succeeded")
        self.logger.debug("ManageClient.get_members LEAVE")
        return res

    async def remove_member(
        self, project_id: str, member_id: str, addons: dict = None, **kwargs
    ) -> Message:
        """
        Removes a member from a project.

        Reference:
        https://developers.deepgram.com/reference/remove-member
        """
        self.logger.debug("ManageClient.remove_member ENTER")
        url = f"{self.config.url}/{self.endpoint}/{project_id}/members/{member_id}"
        self.logger.info("url: %s", url)
        self.logger.info("project_id: %s", project_id)
        self.logger.info("member_id: %s", member_id)
        self.logger.info("addons: %s", addons)
        result = await self.delete(url, addons=addons, **kwargs)
        self.logger.info("result: %s", result)
        res = Message.from_json(result)
        self.logger.verbose("result: %s", res)
        self.logger.notice("remove_member succeeded")
        self.logger.debug("ManageClient.remove_member LEAVE")
        return res

    # scopes
    async def get_member_scopes(
        self, project_id: str, member_id: str, addons: dict = None, **kwargs
    ) -> ScopesResponse:
        """
        Gets a list of scopes for a member.

        Reference:
        https://developers.deepgram.com/reference/get-member-scopes
        """
        self.logger.debug("ManageClient.get_member_scopes ENTER")
        url = (
            f"{self.config.url}/{self.endpoint}/{project_id}/members/{member_id}/scopes"
        )
        self.logger.info("url: %s", url)
        self.logger.info("project_id: %s", project_id)
        self.logger.info("member_id: %s", member_id)
        self.logger.info("addons: %s", addons)
        result = await self.get(url, addons=addons, **kwargs)
        self.logger.info("result: %s", result)
        res = ScopesResponse.from_json(result)
        self.logger.verbose("result: %s", res)
        self.logger.notice("get_member_scopes succeeded")
        self.logger.debug("ManageClient.get_member_scopes LEAVE")
        return res

    async def update_member_scope(
        self,
        project_id: str,
        member_id: str,
        options: ScopeOptions,
        addons: dict = None,
        **kwargs,
    ) -> Message:
        """
        Updates a member's scopes.

        Reference:
        https://developers.deepgram.com/reference/update-scope
        """
        self.logger.debug("ManageClient.update_member_scope ENTER")
        url = (
            f"{self.config.url}/{self.endpoint}/{project_id}/members/{member_id}/scopes"
        )
        self.logger.info("url: %s", url)
        self.logger.info("project_id: %s", project_id)
        self.logger.info("options: %s", options)
        self.logger.info("addons: %s", addons)
        result = await self.put(url, json=options, addons=addons, **kwargs)
        self.logger.info("result: %s", result)
        res = Message.from_json(result)
        self.logger.verbose("result: %s", res)
        self.logger.notice("update_member_scope succeeded")
        self.logger.debug("ManageClient.update_member_scope LEAVE")
        return res

    # invites
    async def list_invites(
        self, project_id: str, addons: dict = None, **kwargs
    ) -> InvitesResponse:
        """
        Please see get_invites for more information.
        """
        return self.get_invites(project_id, addons=addons, **kwargs)

    async def get_invites(
        self, project_id: str, addons: dict = None, **kwargs
    ) -> InvitesResponse:
        """
        Gets a list of invites for a project.

        Reference:
        https://developers.deepgram.com/reference/list-invites
        """
        self.logger.debug("ManageClient.get_invites ENTER")
        url = f"{self.config.url}/{self.endpoint}/{project_id}/invites"
        self.logger.info("url: %s", url)
        self.logger.info("project_id: %s", project_id)
        self.logger.info("addons: %s", addons)
        result = await self.get(url, addons=addons, **kwargs)
        self.logger.info("result: %s", result)
        res = InvitesResponse.from_json(result)
        self.logger.verbose("result: %s", res)
        self.logger.notice("get_invites succeeded")
        self.logger.debug("ManageClient.get_invites LEAVE")
        return res

    async def send_invite_options(
        self, project_id: str, options: InviteOptions, addons: dict = None, **kwargs
    ) -> Message:
        """
        Sends an invite to a project.

        Reference:
        https://developers.deepgram.com/reference/send-invite
        """
        self.logger.debug("ManageClient.send_invite_options ENTER")
        url = f"{self.config.url}/{self.endpoint}/{project_id}/invites"
        self.logger.info("url: %s", url)
        self.logger.info("project_id: %s", project_id)
        self.logger.info("options: %s", options)
        self.logger.info("addons: %s", addons)
        result = await self.post(url, json=options, addons=addons, **kwargs)
        self.logger.info("result: %s", result)
        res = Message.from_json(result)
        self.logger.verbose("result: %s", res)
        self.logger.notice("send_invite_options succeeded")
        self.logger.debug("ManageClient.send_invite_options LEAVE")
        return res

    async def send_invite(
        self, project_id: str, email: str, scope="member", addons: dict = None, **kwargs
    ) -> Message:
        """
        Sends an invite to a project.

        Reference:
        https://developers.deepgram.com/reference/send-invite
        """
        self.logger.debug("ManageClient.send_invite ENTER")
        url = f"{self.config.url}/{self.endpoint}/{project_id}/invites"
        options: InviteOptions = {
            "email": email,
            "scope": scope,
        }
        self.logger.info("url: %s", url)
        self.logger.info("project_id: %s", project_id)
        self.logger.info("options: %s", options)
        self.logger.info("addons: %s", addons)
        result = await self.post(url, json=options, addons=addons, **kwargs)
        self.logger.info("result: %s", result)
        res = Message.from_json(result)
        self.logger.verbose("result: %s", res)
        self.logger.notice("send_invite succeeded")
        self.logger.debug("ManageClient.send_invite LEAVE")
        return res

    async def delete_invite(
        self, project_id: str, email: str, addons: dict = None, **kwargs
    ) -> Message:
        """
        Deletes an invite from a project.

        Reference:
        https://developers.deepgram.com/reference/delete-invite
        """
        self.logger.debug("ManageClient.delete_invite ENTER")
        url = f"{self.config.url}/{self.endpoint}/{project_id}/invites/{email}"
        self.logger.info("url: %s", url)
        self.logger.info("project_id: %s", project_id)
        self.logger.info("email: %s", email)
        self.logger.info("addons: %s", addons)
        result = await self.delete(url, addons=addons, **kwargs)
        self.logger.info("result: %s", result)
        res = Message.from_json(result)
        self.logger.verbose("result: %s", res)
        self.logger.notice("delete_invite succeeded")
        self.logger.debug("ManageClient.delete_invite LEAVE")
        return res

    async def leave_project(
        self, project_id: str, addons: dict = None, **kwargs
    ) -> Message:
        """
        Leaves a project.

        Reference:
        https://developers.deepgram.com/reference/leave-project
        """
        self.logger.debug("ManageClient.leave_project ENTER")
        url = f"{self.config.url}/{self.endpoint}/{project_id}/leave"
        self.logger.info("url: %s", url)
        self.logger.info("project_id: %s", project_id)
        self.logger.info("addons: %s", addons)
        result = await self.delete(url, addons=addons, **kwargs)
        self.logger.info("result: %s", result)
        res = Message.from_json(result)
        self.logger.verbose("result: %s", res)
        self.logger.notice("leave_project succeeded")
        self.logger.debug("ManageClient.leave_project LEAVE")
        return res

    # usage
    async def get_usage_requests(
        self,
        project_id: str,
        options: UsageRequestOptions,
        addons: dict = None,
        **kwargs,
    ) -> UsageRequestsResponse:
        """
        Gets a list of usage requests for a project.

        Reference:
        https://developers.deepgram.com/reference/get-all-requests
        """
        self.logger.debug("ManageClient.get_usage_requests ENTER")
        url = f"{self.config.url}/{self.endpoint}/{project_id}/requests"
        self.logger.info("url: %s", url)
        self.logger.info("project_id: %s", project_id)
        self.logger.info("options: %s", options)
        self.logger.info("addons: %s", addons)
        result = await self.get(url, options=options, addons=addons, **kwargs)
        self.logger.info("result: %s", result)
        res = UsageRequestsResponse.from_json(result)
        self.logger.verbose("result: %s", res)
        self.logger.notice("get_usage_requests succeeded")
        self.logger.debug("ManageClient.get_usage_requests LEAVE")
        return res

    async def get_usage_request(
        self, project_id: str, request_id: str, addons: dict = None, **kwargs
    ) -> UsageRequest:
        """
        Gets details for a specific usage request.

        Reference:
        https://developers.deepgram.com/reference/get-request
        """
        self.logger.debug("ManageClient.get_usage_request ENTER")
        url = f"{self.config.url}/{self.endpoint}/{project_id}/requests/{request_id}"
        self.logger.info("url: %s", url)
        self.logger.info("project_id: %s", project_id)
        self.logger.info("request_id: %s", request_id)
        self.logger.info("addons: %s", addons)
        result = await self.get(url, addons=addons, **kwargs)
        self.logger.info("result: %s", result)
        res = UsageRequest.from_json(result)
        self.logger.verbose("result: %s", res)
        self.logger.notice("get_usage_request succeeded")
        self.logger.debug("ManageClient.get_usage_request LEAVE")
        return res

    async def get_usage_summary(
        self,
        project_id: str,
        options: UsageSummaryOptions,
        addons: dict = None,
        **kwargs,
    ) -> UsageSummaryResponse:
        """
        Gets a summary of usage for a project.

        Reference:
        https://developers.deepgram.com/reference/summarize-usage
        """
        self.logger.debug("ManageClient.get_usage_summary ENTER")
        url = f"{self.config.url}/{self.endpoint}/{project_id}/usage"
        self.logger.info("url: %s", url)
        self.logger.info("project_id: %s", project_id)
        self.logger.info("options: %s", options)
        self.logger.info("addons: %s", addons)
        result = await self.get(url, options=options, addons=addons, **kwargs)
        self.logger.info("result: %s", result)
        res = UsageSummaryResponse.from_json(result)
        self.logger.verbose("result: %s", res)
        self.logger.notice("get_usage_summary succeeded")
        self.logger.debug("ManageClient.get_usage_summary LEAVE")
        return res

    async def get_usage_fields(
        self,
        project_id: str,
        options: UsageFieldsOptions,
        addons: dict = None,
        **kwargs,
    ) -> UsageFieldsResponse:
        """
        Gets a list of usage fields for a project.

        Reference:
        https://developers.deepgram.com/reference/get-fields
        """
        self.logger.debug("ManageClient.get_usage_fields ENTER")
        url = f"{self.config.url}/{self.endpoint}/{project_id}/usage/fields"
        self.logger.info("url: %s", url)
        self.logger.info("project_id: %s", project_id)
        self.logger.info("options: %s", options)
        self.logger.info("addons: %s", addons)
        result = await self.get(url, options=options, addons=addons, **kwargs)
        self.logger.info("result: %s", result)
        res = UsageFieldsResponse.from_json(result)
        self.logger.verbose("result: %s", res)
        self.logger.notice("get_usage_fields succeeded")
        self.logger.debug("ManageClient.get_usage_fields LEAVE")
        return res

    # balances
    async def list_balances(
        self, project_id: str, addons: dict = None, **kwargs
    ) -> BalancesResponse:
        """
        Please see get_balances for more information.
        """
        return self.get_balances(project_id, addons=addons, **kwargs)

    async def get_balances(
        self, project_id: str, addons: dict = None, **kwargs
    ) -> BalancesResponse:
        """
        Gets a list of balances for a project.

        Reference:
        https://developers.deepgram.com/reference/get-all-balances
        """
        self.logger.debug("ManageClient.get_balances ENTER")
        url = f"{self.config.url}/{self.endpoint}/{project_id}/balances"
        self.logger.info("url: %s", url)
        self.logger.info("project_id: %s", project_id)
        self.logger.info("addons: %s", addons)
        result = await self.get(url, addons=addons, **kwargs)
        self.logger.info("result: %s", result)
        res = BalancesResponse.from_json(result)
        self.logger.verbose("result: %s", res)
        self.logger.notice("get_balances succeeded")
        self.logger.debug("ManageClient.get_balances LEAVE")
        return res

    async def get_balance(
        self, project_id: str, balance_id: str, addons: dict = None, **kwargs
    ) -> Balance:
        """
        Gets details for a specific balance.

        Reference:
        https://developers.deepgram.com/reference/get-balance
        """
        self.logger.debug("ManageClient.get_balance ENTER")
        url = f"{self.config.url}/{self.endpoint}/{project_id}/balances/{balance_id}"
        self.logger.info("url: %s", url)
        self.logger.info("project_id: %s", project_id)
        self.logger.info("balance_id: %s", balance_id)
        self.logger.info("addons: %s", addons)
        result = await self.get(url, addons=addons, **kwargs)
        self.logger.info("result: %s", result)
        res = Balance.from_json(result)
        self.logger.verbose("result: %s", res)
        self.logger.notice("get_balance succeeded")
        self.logger.debug("ManageClient.get_balance LEAVE")
        return res
