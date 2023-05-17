from checkout import checkout_negative, ssh_checkout_negative
import yaml


with open('config.yaml') as f:
    data = yaml.safe_load(f)


def test_step8(make_bad_arx):
    # test8
    assert ssh_checkout_negative(data["host"], data["user"], data["password"],
                                 "cd {}; 7z e badarx.7z -o{} -y".format(data["folder_out_negative_u2"],
                                                                        data["folder_ext_u2"]),
                                 "ERROR"), "Test8 Fail"


def test_step9(make_bad_arx):
    # test9
    assert ssh_checkout_negative(data["host"], data["user"], data["password"],
                                 "cd {}; 7z t badarx.7z".format(data["folder_out_negative_u2"]), "ERROR"), "Test9 Fail"

def test_step8(make_bad_arx):
    # test8
    assert checkout_negative("cd {}; 7z e badarx.7z -o{} -y".format(folder_out_negative, folder_ext), "ERROR"),
    "Test8 Fail"


def test_step9(make_bad_arx):
    # test9
    assert checkout_negative("cd {}; 7z t badarx.7z".format(folder_out_negative), "ERROR"), "Test9 Fail"