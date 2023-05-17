import yaml
from checkout import checkout_positive, ssh_checkout
from deploy_file import upload_files

with open('config.yaml') as f:
    data = yaml.safe_load(f)


def test_step0():
    res = []
    upload_files(data["host"], data["user"], data["password"], data["local_path"],
                 data["remote_path"])
    res.append(ssh_checkout(data["host"], data["user"], data["password"],
                            f"echo {data['password']} | sudo -S dpkg -i {data['remote_path']}",
                            "Настраивается пакет"))
    res.append(ssh_checkout(data["host"], data["user"], data["password"],
                            f"echo {data['password']} | sudo -S dpkg -s {data['pkgname']}",
                            "Status: install ok installed"))
    assert all(res), "Test0 Failed"


def test_step1(make_folders_u2, clear_folders_u2, make_files_u2):
    # test1
    res1 = ssh_checkout(data["host"], data["user"], data["password"],
                        "cd {}; 7z a -tzip {}/arx1.tar".format(data["folder_in_u2"], data["folder_out_u2"]),
                        "Everything is Ok"), "Test1 Fail"
    res2 = ssh_checkout(data["host"], data["user"], data["password"], "ls {}".format(data["folder_out_u2"]),
                        "arx1.zip"), "Test1 Fail"
    assert res1 and res2, "Test Fail"


def test_step2(clear_folders_u2, make_files_u2):
    # test2
    res = []
    res.append(ssh_checkout(data["host"], data["user"], data["password"],
                            "cd {}; 7z a {}/arx1.7z".format(data["folder_in_u2"], data["folder_out_u2"]),
                            "Everything is Ok"))
    res.append(ssh_checkout(data["host"], data["user"], data["password"],
                            "cd {}; 7z e arx1.7z -o{} -y".format(data["folder_out_u2"], data["folder_ext_u2"]),
                            "Everything is Ok"))
    for item in make_files_u2:
        res.append(ssh_checkout(data["host"], data["user"], data["password"], "ls {}".format(data["folder_ext_u2"]), ""))
    assert all(res)


def test_step3():
    # test3
    assert ssh_checkout(data["host"], data["user"], data["password"],
                        "cd {}; 7z t {}/arx1.7z".format(data["folder_in_u2"], data["folder_out_u2"]),
                        "Everything is Ok"), "Test3 Fail"


def test_step4(make_folders_u2, clear_folders_u2, make_files_u2):
    # test4
    assert ssh_checkout(data["host"], data["user"], data["password"],
                        "cd {}; 7z u {}/arx1.7z".format(data["folder_in_u2"], data["folder_out_u2"]),
                        "Everything is Ok"), "Test4 Fail"


def test_step5(clear_folders_u2, make_files_u2):
    # test5
    res = []
    res.append(ssh_checkout(data["host"], data["user"], data["password"],
                            "cd {}; 7z a {}/arx1.7z".format(data["folder_in_u2"], data["folder_out_u2"]),
                            "Everything is Ok"))
    for item in make_files_u2:
        res.append(
            ssh_checkout(data["host"], data["user"], data["password"], "cd {}; 7z l arx1.7z".format(data["folder_out_u2"]),
                         item))
    assert all(res)


def test_step6(make_folders_u2, clear_folders_u2, make_files_u2, make_subfolder_u2):
    res = []
    res.append(ssh_checkout(data["host"], data["user"], data["password"],
                            "cd {}; 7z a {}/arx1.7z".format(data["folder_in_u2"], data["folder_out_u2"]),
                            "Everything is Ok"))
    res.append(ssh_checkout(data["host"], data["user"], data["password"],
                            "cd {}; 7z x arx1.7z -o{} -y".format(data["folder_out_u2"], data["folder_ext2_u2"]),
                            "Everything is Ok"))
    for item in make_files_u2:
        res.append(
            ssh_checkout(data["host"], data["user"], data["password"], "ls {}".format(data["folder_ext2_u2"]), item))
        res.append(ssh_checkout(data["host"], data["user"], data["password"], "ls {}".format(data["folder_ext2_u2"]),
                                make_subfolder_u2[0]))
        res.append(ssh_checkout(data["host"], data["user"], data["password"],
                                "ls {}/{}".format(data["folder_ext2_u2"], make_subfolder_u2[0]),
                                make_subfolder_u2[1]))
    assert all(res)


def test_step7():
    assert ssh_checkout(data["host"], data["user"], data["password"], "7z d {}/arx1.7z".format(data["folder_out_u2"]),
                        "Everything is Ok"), "Test7 Fail"

def test_step1(make_folders, clear_folders, make_files):
    # test1
    res1 = checkout_positive("cd {}; 7z a -tzip {}/arx1.tar".format(data["folder_in"], data["folder_out"]),
                             "Everything is Ok"), "Test1 Fail"
    res2 = checkout_positive("ls {}".format(data["folder_out"]), "arx1.zip"), "Test1 Fail"
    assert res1 and res2, "Test Fail"


def test_step2(clear_folders, make_files):
    # test2
    res = []
    res.append(checkout_positive("cd {}; 7z a {}/arx1.7z".format(data["folder_in"], data["folder_out"]),
                                 "Everything is Ok"))
    res.append(checkout_positive("cd {}; 7z e arx1.7z -o{} -y".format(data["folder_out"], data["folder_ext"]),
                                 "Everything is Ok"))
    for item in make_files:
        res.append(checkout_positive("ls {}".format(data["folder_ext"]), ""))
    assert all(res)


def test_step3():
    # test3
    assert checkout_positive("cd {}; 7z t {}/arx1.7z".format(data["folder_in"], data["folder_out"]),
                             "Everything is Ok"), "Test3 Fail"


def test_step4(make_folders, clear_folders, make_files):
    # test4
    assert checkout_positive("cd {}; 7z u {}/arx1.7z".format(data["folder_in"], data["folder_out"]),
                             "Everything is Ok"), "Test4 Fail"


def test_step5(clear_folders, make_files):
    # test5
    res = []
    res.append(checkout_positive("cd {}; 7z a {}/arx1.7z".format(data["folder_in"], data["folder_out"]),
                                 "Everything is Ok"))
    for item in make_files:
        res.append(checkout_positive("cd {}; 7z l arx1.7z".format(data["folder_out"]), item))
    assert all(res)


def test_step6(make_folders, clear_folders, make_files, make_subfolder):
    res = []
    res.append(checkout_positive("cd {}; 7z a {}/arx1.7z".format(data["folder_in"], data["folder_out"]),
                                 "Everything is Ok"))
    res.append(checkout_positive("cd {}; 7z x arx1.7z -o{} -y".format(data["folder_out"], data["folder_ext2"]),
                                 "Everything is Ok"))
    for item in make_files:
        res.append(checkout_positive("ls {}".format(data["folder_ext2"]), item))
        res.append(checkout_positive("ls {}".format(data["folder_ext2"]), make_subfolder[0]))
        res.append(checkout_positive("ls {}/{}".format(data["folder_ext2"], make_subfolder[0]),
                                     make_subfolder[1]))
    assert all(res)


def test_step7():
    assert checkout_positive("7z d {}/arx1.7z".format(data["folder_out"]),
                             "Everything is Ok"), "Test7 Fail"