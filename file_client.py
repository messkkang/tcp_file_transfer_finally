#!/usr/bin/python3
# -*- coding: utf-8 -*-

import socket
import sys
import os
import hashlib
import json


def get_file_md5(file_path):
    m = hashlib.md5()

    with open(file_path, "rb") as f:
        while True:
            data = f.read(1024)
            if len(data) == 0:
                break
            m.update(data)

    return m.hexdigest().upper()


server_ip = input("服务器IP地址：")
server_port = int(input("服务器端口："))

# while True:
#     try:
#         sock = socket.socket()
#         sock.connect((server_ip, server_port))
#     except:
#         time.sleep(1)
#     else:
#         break

sock = socket.socket()
sock.connect((server_ip, server_port))


# def login_main():
#     '''
#     函数功能：用户登录验证
#     函数参数：无
#     返回值：登录验证成功返回用户名，失败返回False
#     '''
#     while True:
#         user_name = input("\n用户名：")
#         ret = check_user_name(user_name)
#         if ret == 0:
#             print("用户名不存在，请重新输入！")
#         elif ret == 1:
#             print("用户名格式错误，请重新输入！")
#         else:
#             break
#
#     while True:
#         password = input("\n密码：")
#         ret = check_password(password)
#         if ret == 0:
#             break
#         else:
#             print("密码格式错误，请重新输入！")
#
#     if check_uname_pwd(user_name, password):
#         return False
#     return user_name


def md5_passeord():
    m = hashlib.md5()
    m.update("kangkang123".encode())
    pawd = m.hexdigest().upper()
    return pawd


md5_passeord()


def user_client__reg_thread():
    f = {
        "op": 2,
        "args":
            {
                "uname": "kangkang",
                "passwd": "%s" % md5_passeord(),  # 真实密码的MD5值，使用大写表示
                "phone": "15871137690",  # 手机号
                "email": "904311392@qq.com"  # 邮箱
            }
    }

    f = json.dumps(f).encode()
    print(f)
    file_len = "{:<15}".format(len(f)).encode()
    print(file_len)
    sock.send(file_len)
    sock.send(f)

    data_len = sock.recv(15).decode().rstrip()
    print(data_len)
    if len(data_len) > 0:
        data_len = int(data_len)
        recv_size = 0
        json_data = b""
        while recv_size < data_len:
            tmp = sock.recv(data_len - recv_size)
            if tmp == 0:
                break
            json_data += tmp
            recv_size += len(tmp)
            json_data = json_data.decode()
            req = json.loads(json_data)
            if req['error_code'] == 1:
                print('注册失败')
                return 1
            else:
                print('注册成功')
                return 0


def login_requests():
    f = {
        "op": 1,
        "args":
            {
                "uname": "kangkang",
                "passwd": "%s" % md5_passeord()  # 真实密码的MD5值，使用大写表示
            }
    }
    f = json.dumps(f).encode()
    file_len = "{:<15}".format(len(f)).encode()
    sock.send(file_len)
    sock.send(f)

    data_len = sock.recv(15).decode().rstrip()
    if len(data_len) > 0:
        data_len = int(data_len)

        recv_size = 0
        json_data = b""
        while recv_size < data_len:
            tmp = sock.recv(data_len - recv_size)
            if tmp == 0:
                break
            json_data += tmp
            recv_size += len(tmp)
            json_data = json_data.decode()
            req = json.loads(json_data)
            if req["error_code"] == 1:
                print("登录失败")
                return 1
            else:
                print("登录成功")
                return 0


def commd_request():
    f = {
        "op": 3,
        "args":
            {
                "uname": "kangkang"
            }
    }
    f = json.dumps(f).encode()
    file_len = "{:<15}".format(len(f)).encode()
    sock.send(file_len)
    sock.send(f)

    data_len = sock.recv(15).decode().rstrip()
    if len(data_len) > 0:
        data_len = int(data_len)

        recv_size = 0
        json_data = b""
        while recv_size < data_len:
            tmp = sock.recv(data_len - recv_size)
            if tmp == 0:
                break
            json_data += tmp
            recv_size += len(tmp)
        json_data = json_data.decode()
        print(json_data)
        req = dict(eval(json_data))
        print(req)
        if req["error_code"] == 1:
            print("用户已存在")
            return 0
        else:
            print("用户不存在")
            return 1


def main():
    while True:
        print("1.注册信息")
        print("2.登录信息")
        print("3.校验用户")
        req1 = input(">>>")
        if req1 == "1":
            re = user_client__reg_thread()
            if re == 0:
                print("注册成功")
            else:
                print("注册失败")
        elif req1 == "2":
            long1 = login_requests()
            if long1 == 0:
                break
            else:
                print("登录失败")
        else:
            ve = commd_request()
            if ve == 0:
                print("用户已存在,请进行登录")
            else:
                print("用户不存在请注册")

    while True:
        file_path = sock.recv(300).decode().rstrip()
        if len(file_path) == 0:
            break

        file_size = sock.recv(15).decode().rstrip()
        if len(file_size) == 0:
            break
        file_size = int(file_size)

        file_md5 = sock.recv(32).decode()
        if len(file_md5) == 0:
            break

        # 如果为空文件夹
        if file_size == -1:
            print("\n成功接收空文件夹 %s" % file_path)
            os.makedirs(file_path, exist_ok=True)
            continue

        os.makedirs(os.path.dirname(file_path), exist_ok=True)

        print("\n正在接收文件 %s，请稍候......" % file_path)

        f = open(file_path, "wb")

        recv_size = 0
        while recv_size < file_size:
            file_data = sock.recv(file_size - recv_size)
            if len(file_data) == 0:
                break

            f.write(file_data)
            recv_size += len(file_data)
            print("\r拷贝进度为:%.2f%%" % (recv_size * 100 / file_size), end="")
            if recv_size >= file_size:
                break
        f.close()

        recv_file_md5 = get_file_md5(file_path)

        if recv_file_md5 == file_md5:
            print("成功接收文件 %s" % file_path)
        else:
            print("接收文件 %s 失败（MD5校验不通过）" % file_path)
            break

    sock.close()


if __name__ == '__main__':
    main()
