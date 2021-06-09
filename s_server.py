#!/usr/bin/python3
import socket
import time

HOST = '127.0.0.1'
PORT = 65432
TIME_START_SERVER = time.time()

def uptime_command():
    return time.strftime("%H:%M:%S", time.gmtime(time.time() - TIME_START_SERVER))

def info_command():
    return str('Ver 1.0, Server start: ' + time.ctime(TIME_START_SERVER))

def help_command():
    return str("""
            uptime - czas zycia serwera,\n
            info - numer wersji serwera, data utworzenia,\n
            help - pomoc,\n
            stop - zamyka serwer i klienta\n
            """)

def stop_command():
    pass

def wrong_command():
    return str('Wrong command')

def main():
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind((HOST,PORT))
    server.listen()
    print("Wait to connect client")
    conn, addr = server.accept()
    print("Connected by", addr)
    conn.send('Welcome in my serwer'.encode())
    commands = {
            'uptime': uptime_command,
            'info': info_command,
            'help': help_command,
            'stop': server.close
        }
    try:
        while True:
            message = (conn.recv(64)).decode()
            if message in commands:
                re_message = commands[message]()
            else:
                re_message = wrong_command()
            conn.send(re_message.encode())

    except:
        server.close()
        return
    finally:
        server.close()
        return

main()
