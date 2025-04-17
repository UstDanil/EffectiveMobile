class Data:
    def __init__(self, data, ip):
        self.data = data
        self.receiver_ip = ip


class Server:
    count = 0

    def __init__(self):
        self.ip = self.count + 1
        self.increase_server_count()
        self.router = None

    @classmethod
    def increase_server_count(cls):
        cls.count += 1

    def send_data(self, data):
        self.router.buffer.append(data)

    def receive_message(self, msg):
        print(f"Сервер {str(self.ip)} принял сообщение: '{msg}'.")


class Router:
    def __init__(self):
        self.servers = dict()
        self.buffer = list()

    def link(self, server):
        self.servers[server.ip] = server
        server.router = self

    def unlink(self, server):
        server.router = None
        del self.servers[server.ip]

    def send_data(self):
        for data in self.buffer:
            if data.receiver_ip not in self.servers:
                continue

            server = self.servers[data.receiver_ip]
            server.receive_message(data.data)
        self.buffer = list()


# if __name__ == '__main__':
#     server_1 = Server()
#     server_2 = Server()
#     server_3 = Server()
#     router = Router()
#     router.link(server_1)
#     router.link(server_2)
#     router.link(server_3)
#     router.unlink(server_2)
#     server_1.send_data(Data('3333', 3))
#     server_3.send_data(Data('1111', 1))
#     router.send_data()
