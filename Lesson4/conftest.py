import os
import random
import string
import subprocess

import pytest
from checkout import checkout_positive, ssh_checkout
import yaml
from datetime import *

with open('config.yaml') as f:
    data = yaml.safe_load(f)


@pytest.fixture()
def make_folders_u2():
    return ssh_checkout(data["host"], data["user"], data["password"],
                        "mkdir {} {} {} {}".format(data["folder_in_u2"], data["folder_out_u2"], data["folder_ext_u2"],
                                                   data["folder_badarx_u2"]), "")


@pytest.fixture()
def clear_folders_u2():
    return ssh_checkout(data["host"], data["user"], data["password"],
                        "rm -rf {}/* {}/* {}/* {}/*".format(data["folder_in_u2"], data["folder_out_u2"],
                                                            data["folder_ext_u2"], data["folder_badarx_u2"]), "")


@pytest.fixture()
def make_files_u2():
    list_off_files = []
    for i in range(5):
        filename = ''.join(random.choices(string.ascii_uppercase + string.digits, k=5))
        if ssh_checkout(data["host"], data["user"], data["password"],
                        "cd {}; dd if=/dev/urandom of={} bs={} count=1 iflag=fullblock".format(data["folder_in_u2"],
                                                                                               filename, data["bs"]),
                        ""):
            list_off_files.append(filename)
    return list_off_files


@pytest.fixture()
def make_subfolder_u2():
    testfilename = ''.join(random.choices(string.ascii_uppercase + string.digits, k=5))
    subfoldername = ''.join(random.choices(string.ascii_uppercase + string.digits, k=5))
    if not ssh_checkout(data["host"], data["user"], data["password"],
                        "cd {}; mkdir {}".format(data["folder_in_u2"], subfoldername), ""):
        return None, None
    if not ssh_checkout(data["host"], data["user"], data["password"],
                        "cd {}/{}; dd if=/dev/urandom of={} bs=1M count=1 iflag=fullblock".format(data["folder_in_u2"],
                                                                                                  subfoldername,
                                                                                                  testfilename), ""):
        return subfoldername, None
    else:
        return subfoldername, testfilename


@pytest.fixture()
def make_bad_arx_u2(make_folders, clear_folders, make_files):
    ssh_checkout(data["host"], data["user"], data["password"],
                 "cd {}; 7z a {}/arx1.7z".format(data["folder_in_u2"], data["folder_out_u2"]),
                 "Everything is Ok"), "Test1 Fail"
    return ssh_checkout(data["host"], data["user"], data["password"], "truncate -s 1 {}/badarx.7z", ""), "Test1 Fail"


@pytest.fixture()
def make_folders():
    return checkout_positive("mkdir {} {} {} {}".format(data["folder_in"], data["folder_out"],
                                                        data["folder_ext"], data["folder_badarx"]), "")


@pytest.fixture()
def clear_folders():
    return checkout_positive("rm -rf {}/* {}/* {}/* {}/*".format(data["folder_in"], data["folder_out"],
                                                                 data["folder_ext"], data["folder_badarx"]), "")


@pytest.fixture()
def make_files():
    list_off_files = []
    for i in range(5):
        filename = ''.join(random.choices(string.ascii_uppercase + string.digits, k=5))
        if checkout_positive(
                "cd {}; dd if=/dev/urandom of={} bs={} count=1 iflag=fullblock".format(data["folder_in"],
                                                                                       filename, data["bs"]), ""):
            list_off_files.append(filename)
    return list_off_files


@pytest.fixture()
def make_subfolder():
    testfilename = ''.join(random.choices(string.ascii_uppercase + string.digits, k=5))
    subfoldername = ''.join(random.choices(string.ascii_uppercase + string.digits, k=5))
    if not checkout_positive("cd {}; mkdir {}".format(data["folder_in"], subfoldername), ""):
        return None, None
    if not checkout_positive(
            "cd {}/{}; dd if=/dev/urandom of={} bs=1M count=1 iflag=fullblock".format(data["folder_in"], subfoldername,
                                                                                      testfilename), ""):
        return subfoldername, None
    else:
        return subfoldername, testfilename


@pytest.fixture()
def make_bad_arx(make_folders, clear_folders, make_files):
    checkout_positive("cd {}; 7z a {}/arx1.7z".format(data["folder_in"], data["folder_out"]),
                      "Everything is Ok"), "Test1 Fail"
    return checkout_positive("truncate -s 1 {}/badarx.7z", ""), "Test1 Fail"


@pytest.fixture()
def res_time():
    time = f"Время: {datetime.now().strftime('%H:%M:%S')}"
    return time


@pytest.fixture()
def make_res_file():
    if checkout_positive(f"ls {data['folder_tst']}", data['filename']):
        return True
    else:
        file = checkout_positive(f"cd {data['folder_tst']}; touch {data['filename']}", "")
        return file


@pytest.fixture()
def stat_data():
    res = subprocess.run("tail /proc/loadavg", shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                         encoding="utf-8")
    return res.stdout


@pytest.fixture(autouse=True)
def res_file_write(res_time, make_res_file, stat_data):
    count_file = len(os.listdir(os.getcwd()))
    size_file = os.path.getsize(os.getcwd())
    if make_res_file:
        with open(f"{data['folder_tst']}/{data['filename']}", "a") as f:
            f.write(f"{res_time}, {stat_data}, {count_file}, {size_file} \n")