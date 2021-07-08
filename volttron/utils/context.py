
from configparser import ConfigParser
# used to make sure that volttron_home hasn't be modified
# since written to disk.
import hashlib
import logging
import os
from pathlib import Path
from posixpath import expanduser

from typing import Optional

_log = logging.getLogger(__name__)


class ClientContext:
    """
    The `ClientContext` class is the single source of truth within
    a process running this system.
    """
    __volttron_home__: Optional[Path] = None
    __config__: dict = {}

    # @classmethod
    # def __load_config__(klass):
    #     if __config__ is None:
    #     __config__ = FrozenDict()
    #     volttron_home = get_home()
    #     config_file = os.path.join(volttron_home, "config")
    #     if os.path.exists(config_file):
    #         parser = ConfigParser()
    #         parser.read(config_file)
    #         options = parser.options("volttron")
    #         for option in options:
    #             __config__[option] = parser.get("volttron", option)
    #         __config__.freeze()
    # return __config__


    @classmethod
    def get_config_param(key: str):
        pass
    
    # def get_config_path() -> str:
    # """
    # Returns the platforms main configuration file.

    # :return:
    # """
    # return os.path.join(get_home(), "config")
    
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
        vhome = Path(os.environ.get("VOLTTRON_HOME", "~/.volttron")).expanduser().resolve()

        # klass variable is set the first time through this function
        # so we test to make sure nothing has changed from vhome and
        # the klass.__volttron_home__ variable.
        if klass.__volttron_home__:
            hashed = hashlib.md5(str(vhome).encode('utf-8')).hexdigest()
            if not klass.__volttron_home__.joinpath(hashed).exists():
                raise ValueError("VOLTTRON_HOME has been changed.  Possible nefarious act!")
        
        # Initialize class variable here and write a file inside the
        # volttron_home that we can check against.
        if klass.__volttron_home__ is None:
            klass.__volttron_home__ = vhome
            
            if not vhome.exists():
                # python 3.6 doesn't support pathlike object in mkdir
                os.makedirs(str(vhome), exist_ok=True)
            
            # Create a file with the hex of the path so that we know when 
            # it has been manipulated
            hexhash = hashlib.md5(str(vhome).encode('utf-8')).hexdigest()
            with open(vhome.joinpath(hexhash), "wt") as fp:
                fp.write(hexhash)

        return str(vhome)
