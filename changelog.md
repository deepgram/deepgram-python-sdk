## 7.0.0 - 2026-03-18
* The SDK now supports end-of-turn threshold configuration with new `eot_threshold` and `eager_eot_threshold` fields in V2 listen providers. Agent settings have been restructured with improved type organization and new think update capabilities.
* The agent API types have been restructured for better organization. Several type names have changed:
* `AgentV1SettingsAgentListen` → `AgentV1SettingsAgentContextListen`
* `AgentV1SettingsAgentSpeak` → `AgentV1SettingsAgentContextSpeak`
* `AgentV1SettingsAgentThink` → `AgentV1SettingsAgentContextThink`
* Context message types now include "Context" in their names (e.g., `AgentV1SettingsAgentContextMessagesItem` → `AgentV1SettingsAgentContextContextMessagesItem`)
* Update your imports to use the new type names. The functionality remains the same, only the naming structure has changed to better reflect the hierarchical organization.
* The SDK now includes enhanced agent configuration with restructured context settings and new think/speak update types. Listen websocket connections now use strongly-typed parameters instead of generic strings for better type safety and IDE support.
* The WebSocket APIs now use specific type classes (ListenV2Encoding, SpeakV1Model, etc.) instead of generic strings for better type safety and IDE support. New agent configuration capabilities have been added, including support for listen, speak, and think provider settings with dynamic configuration updates.
* New configuration message types for Listen v2 API enable dynamic adjustment of thresholds and keyterms during streaming sessions. Project member responses now include optional scopes, first_name, and last_name fields.

