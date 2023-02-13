from asgiref.sync import async_to_sync
from channels.generic.websocket import WebsocketConsumer


class Consumer(WebsocketConsumer):
    def connect(self):
        self.accept()
        async_to_sync(self.add_group)('players')

    def receive(self, text_data=None, bytes_data=None):
        # self.send(text_data)
        pass

    def disconnect(self, code):
        pass
