import sys
import platform
import socket
import os

from ...exceptions import ContextParsingException
from .Block import Block


class Environment(Block):
    id = "environment"
    name = "System Environment"
    icon = "TerminalIcon"

    def build(self):
        python_version = (
            f"{sys.version_info.major}.{sys.version_info.minor}.{sys.version_info.micro}"
        )
        default_encoding = sys.getdefaultencoding()
        file_system_encoding = sys.getfilesystemencoding()
        os_name = platform.system()
        if os_name == "Darwin":
            os_name = "macOS"

        # when VPN is enabled it can fails for some VPN clients on macOS
        try:
            ip = socket.gethostbyname(socket.gethostname())
        except socket.gaierror:
            raise ContextParsingException(
                "Exceptionite did not manage to fetch the IP address"
                + "Disable you VPN or '127.0.0.1 YOUR_HOSTNAME' entry in /etc/hosts file."
            )

        return {
            "Python Version": python_version,
            "Python Interpreter": sys.executable,
            "Virtual env": os.getenv("VIRTUAL_ENV"),
            "Python argv": sys.argv,
            "Working Dir": os.getcwd(),
            "OS": os_name,
            "Arch": platform.architecture()[0],
            "Hostname": socket.gethostname(),
            "IP": ip,
            "File System Encoding": file_system_encoding,
            "Default Encoding": default_encoding,
        }

    def has_content(self):
        return True
