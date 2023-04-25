# Самостоятельная работа(сдавать не обязательно) Доработать тест
# на питоне из предыдущего задания таким образом, чтобы вывод сохранялся построчно в список
# и в тесте проверялось, что в этом списке есть строки VERSION = "22.04.1 LTS (Jammy Jellyfish)" и
# VERSION_CODENAME = jammy.Проверка должна выполняться только если код возврата равен 0.

import subprocess

if __name__ == '__main__':

    result = subprocess.run("cat /etc/os-release", shell=True, stdout=subprocess.PIPE, encoding="utf-8")
    out = result.stdout
    print(out)
    out_list = out.split("\n")
    print(out_list)

    if result.returncode == 0:
        if 'VERSION="22.04.1 LTS (Jammy Jellyfish)"' in out_list and 'VERSION_CODENAME=jammy' in out_list:
            print("SUCCESS")
        else:
            print("FAIL")
    else:
        print("FAIL")


    # Задание 1.
    #
    # Условие:
    # Написать функцию на Python, которой передаются в качестве
    # параметров команда и текст.Функция должна возвращать True,\если
    # команда успешно выполнена и текст найден в её выводе
    # и False в противном случае.Передаваться должна только одна строка, разбиение
    # вывода использовать не нужно.


    def func(command, text):
        result1 = subprocess.run(command, shell=True, stdout=subprocess.PIPE, encoding="utf-8")
        out1 = result1.stdout

        if result1.returncode == 0:
            if "apt" in out1:
                return True
            else:
                return False
        else:
            return False
    print(func("ls /etc", "apt"))
