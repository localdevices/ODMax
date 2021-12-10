import shutil

def assert_cli_exe(cmd):
    """
    Assert if a command-line OS command is available

    :param cmd: str, command to check
    :return: True if command exists, false if not
    """
    return shutil.which(cmd) is not None
