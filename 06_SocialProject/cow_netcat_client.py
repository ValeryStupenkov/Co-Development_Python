import cmd
import threading
import select
import shlex
import socket
import sys
import pyreadline3

readline = pyreadline3.Readline()

class NetcatClient(cmd.Cmd):
    def __init__(self, socket, locker):
        super().__init__()
        self.socket = socket
        self.locker = locker

    def send(self, message):
        self.socket.send(message.encode())

    def receive(self, timeout):
        readable, _, _ = select.select([self.socket], [], [], timeout)
        for socket in readable:
            message = socket.recv(1024).decode()
            return message
        return None
    
    def do_who(self, args):
        self.send("who\n")

    def do_cows(self, args):
        self.send("cows\n")

    def do_login(self, args):
        self.send(f"login {shlex.split(args)[0]}\n")

    def do_say(self, args):
        self.send(f"say {args.strip()}\n")

    def do_yield(self, args):
        self.send(f"yield {args.strip()}\n")

    def do_exit(self, args):
        self.send("exit\n")
        return True

    def complete_login(self, text):
        with self.locker:
            self.send("cows\n")
            msg = self.receive(timeout=None)
            for c in ["'", "[", "]", ","]:
                msg = msg.replace(c, "")
            cows = msg.strip().split()[2:]
            result = []
            for s in cows:
                if s.startswith(text):
                    result.append(s)
            return result
        
    def complete_send(self, text):
        with self.locker:
            if len(text.split()) <= 1:
                self.send("who\n")
                msg = self.receive(timeout=None)
                for c in ["'", "[", "]", ","]:
                    msg = msg.replace(c, "")
                who = msg.strip().split()[2:]
                result = []
                for s in who:
                    if s.startswith(text):
                        result.append(s)
                return result
            
    def start_messaging_thread(self):
        while True:
            with self.locker:
                msg = self.receive(timeout=0)
                if msg:
                    print(msg.strip())
                    print(f"{self.prompt}{readline.get_line_buffer()}", end="", flush=True)


if __name__ == '__main__':
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        if len(sys.argv) > 2:
            s.connect((sys.argv[1], int(sys.argv[2])))
        else:
            s.connect((sys.argv[1], 1337))
        s.setblocking(False)
        locker = threading.Lock()
        client = NetcatClient(s, locker)
        gm = threading.Thread(target=client.start_messaging_thread)
        gm.start()
        client.cmdloop()