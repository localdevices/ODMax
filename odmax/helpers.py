import shutil
from subprocess import Popen, PIPE

def assert_cli_exe(cmd):
    """
    Assert if a command-line OS command is available

    :param cmd: str, command to check
    :return: True if command exists, false if not
    """
    return shutil.which(cmd) is not None

def exiftool(*args):
    process = Popen(['exiftool'] + list(args), stdout=PIPE, stderr=PIPE)
    stdout, stderr = process.communicate()
    if stderr:
        print(f"WARNING: exceptions found during processing: {stderr.decode()}")
    return stdout.decode()
