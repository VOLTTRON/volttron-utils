from configparser import ConfigParser

# used to make sure that volttron_home hasn't be modified
# since written to disk.
import hashlib
import logging
import os
from pathlib import Path
from posixpath import expanduser
from typing import Optional

from .frozendict import FrozenDict

_log = logging.getLogger(__name__)


class ClientContext:
    """
    The `ClientContext` class is the single source of truth within
    a process running this system.
    """

    __volttron_home__: Optional[Path] = None
    __config__: dict = {}
    __config_keys__ = (
        "vip-address",
        "bind-web-address",
        "instance-name",
        "message-bus",
        "web-ssl-cert",
        "web-ssl-key",
        "web-secret-key",
        "secure-agent-users",
    )

    @classmethod
    def __load_config__(klass: "ClientContext"):
        if klass.__config__ is None:
            klass.__config__ = FrozenDict()

            volttron_home = ClientContext.get_volttron_home()
            config_file = os.path.join(volttron_home, "config")
            if os.path.exists(config_file):
                parser = ConfigParser()
                parser.read(config_file)
                options = parser.options("volttron")
                for option in options:
                    klass.__config__[option] = parser.get("volttron", option)
                klass.__config__.freeze()
        return klass.__config__

    @classmethod
    def get_config_param(
        klass, key: str, default: Optional[str] = None
    ) -> Optional[str]:

        ClientContext.__load_config__()
        return klass.__config__.get(key, default)

    @classmethod
    def is_rabbitmq_available(klass):
        rabbitmq_available = True
        try:
            import pika

            rabbitmq_available = True
        except ImportError:
            os.environ["RABBITMQ_NOT_AVAILABLE"] = "True"
            rabbitmq_available = False
        return rabbitmq_available

    @classmethod
    def get_volttron_home(klass) -> str:
        """
        Return the VOLTTRON_HOME directory specified or default directory.

        If the VOLTTRON_HOME environment variable is set, it used.
        Otherwise, the default value of '~/.volttron' is used.

        If the volttron_home does not exist then this function will create
        it if possible.  This function also creates a check file for the
        VOLTTRON_HOME such that if the VOLTTRON_HOME is modified during
        runtime it will be detected and cause an error.

        @return:str:
            The absolute path to the volttron_home.
        """

        # vhome to test against for modification.
        vhome = (
            Path(os.environ.get("VOLTTRON_HOME", "~/.volttron")).expanduser().resolve()
        )

        # klass variable is set the first time through this function
        # so we test to make sure nothing has changed from vhome and
        # the klass.__volttron_home__ variable.
        if klass.__volttron_home__:
            if vhome != klass.__volttron_home__:
                raise ValueError(
                    "VOLTTRON_HOME has been changed.  Possible nefarious act!"
                )

        # Initialize class variable here and write a file inside the
        # volttron_home that we can check against.
        if klass.__volttron_home__ is None:
            klass.__volttron_home__ = vhome

            if not vhome.exists():
                # python 3.6 doesn't support pathlike object in mkdir
                os.makedirs(str(vhome), exist_ok=True)

        return str(vhome)

    @classmethod
    def get_fq_identity(klass, identity, platform_instance_name=None):
        """
        Return the fully qualified identity for the passed core identity.

        Fully qualified identities are instance_name.identity

        :param identity:
        :param platform_instance_name: str The name of the platform.
        :return:
        """
        if not platform_instance_name:
            platform_instance_name = klass.get_config_param("instance-name")
        return "{platform_instance_name}.{identity}"

    @classmethod
    def get_messagebus(klass):
        """Get type of message bus - zeromq or rabbbitmq."""
        return klass.get_config_param("message-bus")

    @classmethod
    def get_instance_name(klass):
        """Get type of message bus - zeromq or rabbbitmq."""
        return klass.get_config_param("instance-name")

    @classmethod
    def is_web_enabled(klass):
        """Returns True if web enabled, False otherwise"""
        if klass.get_config_param("bind-web-address"):
            return True
        return False

    @classmethod
    def is_secure_mode(klass):
        """Returns True if running in secure mode, False otherwise"""
        secure_mode = klass.get_config_param("secure-agent-users", False)
        if secure_mode:
            secure_mode = secure_mode.upper() == "TRUE"
        return secure_mode
