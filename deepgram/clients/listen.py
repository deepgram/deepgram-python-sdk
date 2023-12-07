# Copyright 2023 Deepgram SDK contributors. All Rights Reserved.
# Use of this source code is governed by a MIT license that can be found in the LICENSE file.
# SPDX-License-Identifier: MIT

from importlib import import_module
import logging, verboselogs

from ..options import DeepgramClientOptions

from .prerecorded.client import (
    PreRecordedClient,
    AsyncPreRecordedClient,
    PrerecordedOptions,
)
from .live.client import LiveClient, AsyncLiveClient, LiveOptions
from .errors import DeepgramModuleError


class ListenClient:
    def __init__(self, config: DeepgramClientOptions):
        self.logger = logging.getLogger(__name__)
        self.logger.addHandler(logging.StreamHandler())
        self.logger.setLevel(config.verbose)
        self.config = config

    @property
    def prerecorded(self):
        return self.Version(self.config, "prerecorded")

    @property
    def asyncprerecorded(self):
        return self.Version(self.config, "asyncprerecorded")

    @property
    def live(self):
        return self.Version(self.config, "live")

    @property
    def asynclive(self):
        return self.Version(self.config, "asynclive")

    # INTERNAL CLASSES
    class Version:
        def __init__(self, config, parent: str):
            self.logger = logging.getLogger(__name__)
            self.logger.addHandler(logging.StreamHandler())
            self.logger.setLevel(config.verbose)
            self.config = config
            self.parent = parent

        # FUTURE VERSIONING:
        # When v2 or v1.1beta1 or etc. This allows easy access to the latest version of the API.
        # @property
        # def latest(self):
        #     match self.parent:
        #         case "live":
        #             return LiveClient(self.config)
        #         case "prerecorded":
        #             return PreRecordedClient(self.config)
        #         case _:
        #             raise DeepgramModuleError("Invalid parent")

        def v(self, version: str = ""):
            self.logger.debug("Version.v ENTER")
            self.logger.info("version: %s", version)
            if len(version) == 0:
                self.logger.error("version is empty")
                self.logger.debug("Version.v LEAVE")
                raise DeepgramModuleError("Invalid module version")

            parent = ""
            fileName = ""
            className = ""
            match self.parent:
                case "live":
                    parent = "live"
                    fileName = "client"
                    className = "LiveClient"
                case "asynclive":
                    parent = "live"
                    fileName = "async_client"
                    className = "AsyncLiveClient"
                case "prerecorded":
                    parent = "prerecorded"
                    fileName = "client"
                    className = "PreRecordedClient"
                case "asyncprerecorded":
                    parent = "prerecorded"
                    fileName = "async_client"
                    className = "AsyncPreRecordedClient"
                case _:
                    self.logger.error("parent unknown: %s", self.parent)
                    self.logger.debug("Version.v LEAVE")
                    raise DeepgramModuleError("Invalid parent type")

            # create class path
            path = f"deepgram.clients.{parent}.v{version}.{fileName}"
            self.logger.info("path: %s", path)
            self.logger.info("className: %s", className)

            # import class
            mod = import_module(path)
            if mod is None:
                self.logger.error("module path is None")
                self.logger.debug("Version.v LEAVE")
                raise DeepgramModuleError("Unable to find package")

            my_class = getattr(mod, className)
            if my_class is None:
                self.logger.error("my_class is None")
                self.logger.debug("Version.v LEAVE")
                raise DeepgramModuleError("Unable to find class")

            # instantiate class
            myClass = my_class(self.config)
            self.logger.notice("Version.v succeeded")
            self.logger.debug("Version.v LEAVE")
            return myClass
