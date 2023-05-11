from checkout import checkout, checksum, check7zh

path_dir = "cd /home/georgy/tst"
path_arx = "/home/georgy/arx1"
path_arx1 = "/home/georgy/tst/arx3.7z"


def test_step1():
    # test1
    assert checkout("cd {}; 7z a {}".format(path_dir, path_arx), "Everything is Ok"), "Test1 FAIL"


# def test_step2():
#     # test2
#     assert checkout("cd {}; 7z u {}".format(path_dir, path_arx), "Everything is Ok"), "Test1 FAIL"
#
#
# def test_step3():
#     # test3
#     assert checkout("cd {}; 7z d {}".format(path_dir, path_arx), "Everything is Ok"), "Test1 FAIL"


def test_step6():
    # test6
    assert checkout("cd {}; 7z l arx7.7z".format(path_dir, path_arx1), 'Physical Size = 452'), "Test1 FAIL"

def test_step7():
    # test7
    assert checkout('cd {}; 7z x {}'.format(path_dir, path_arx1), 'Everything is Ok'), 'Test7 Failed'

def test_step8():
    # test8
    assert checksum('cd {}; crc32 {}'.format(path_dir, path_arx1),
                    'cd {}; 7z h {}'.format(path_dir, path_arx1)), 'Test8 Failed'
