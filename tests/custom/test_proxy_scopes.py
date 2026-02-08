"""Tests for proxy scope definitions and path matching."""


from deepgram.proxy.scopes import (
    Scope,
    get_target_base_url,
    path_matches_any_scope,
    path_matches_scope,
)


class TestPathMatchesScope:
    def test_listen_v1(self):
        assert path_matches_scope("/v1/listen", Scope.LISTEN)

    def test_listen_v2(self):
        assert path_matches_scope("/v2/listen", Scope.LISTEN)

    def test_listen_with_subpath(self):
        assert path_matches_scope("/v1/listen/stream", Scope.LISTEN)

    def test_speak(self):
        assert path_matches_scope("/v1/speak", Scope.SPEAK)

    def test_read(self):
        assert path_matches_scope("/v1/read", Scope.READ)

    def test_agent(self):
        assert path_matches_scope("/v1/agent", Scope.AGENT)

    def test_manage_projects(self):
        assert path_matches_scope("/v1/projects", Scope.MANAGE)

    def test_manage_usage(self):
        assert path_matches_scope("/v1/usage", Scope.MANAGE)

    def test_self_hosted(self):
        assert path_matches_scope("/v1/onprem", Scope.SELF_HOSTED)

    def test_no_match_wrong_scope(self):
        assert not path_matches_scope("/v1/listen", Scope.SPEAK)

    def test_no_match_unrecognised_path(self):
        assert not path_matches_scope("/v1/unknown", Scope.LISTEN)


class TestPathMatchesAnyScope:
    def test_matches_first(self):
        assert path_matches_any_scope("/v1/listen", [Scope.LISTEN, Scope.SPEAK])

    def test_matches_second(self):
        assert path_matches_any_scope("/v1/speak", [Scope.LISTEN, Scope.SPEAK])

    def test_no_match(self):
        assert not path_matches_any_scope("/v1/agent", [Scope.LISTEN, Scope.SPEAK])

    def test_empty_scopes(self):
        assert not path_matches_any_scope("/v1/listen", [])


class TestGetTargetBaseUrl:
    def test_default_api(self):
        assert get_target_base_url("/v1/listen") == "https://api.deepgram.com"

    def test_agent_path(self):
        assert get_target_base_url("/v1/agent") == "https://agent.deepgram.com"

    def test_agent_subpath(self):
        assert get_target_base_url("/v1/agent/sessions") == "https://agent.deepgram.com"

    def test_custom_production_url(self):
        assert get_target_base_url("/v1/listen", production_url="https://custom.api.com") == "https://custom.api.com"

    def test_custom_agent_url(self):
        assert get_target_base_url("/v1/agent", agent_url="https://custom.agent.com") == "https://custom.agent.com"

    def test_speak_goes_to_api(self):
        assert get_target_base_url("/v1/speak") == "https://api.deepgram.com"
