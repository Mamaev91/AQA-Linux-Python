import subprocess


def checkout(cmd, text):
    result = subprocess.run(cmd, shell=True, stdout=subprocess.PIPE, encoding='utf-8')
    if result.returncode == 0 and text in result.stdout:
        return True
    else:
        return False


def checksum(cmdcrc, cmd7zh):
    result = subprocess.run(cmdcrc, shell=True, stdout=subprocess.PIPE, encoding='utf-8')
    if result.stdout.upper() in check7zh(cmd7zh):
        return True
    else:
        return False


def check7zh(cmd):
    result = subprocess.run(cmd, shell=True, stdout=subprocess.PIPE, encoding='utf-8')
    return result.stdout


