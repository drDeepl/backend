from asgiref.sync import async_to_sync
from channels.generic.websocket import JsonWebsocketConsumer,AsyncWebsocketConsumer



class Consumer(JsonWebsocketConsumer):
    def connect(self): # add sync
        print("SOCKET CONNECT")
        async_to_sync(self.channel_layer.group_add)('players', self.channel_name)
        self.accept()

    def receive(self, text_data=None, bytes_data=None):
        self.send(text_data)
        print('SOCKET RECEIVE')
        

    def disconnect(self, code):
        async_to_sync(self.channel_layer.group_discard)('players', self.channel_name)

    def acquired_sale_offer(self, event):
        self.send_json(
             {
             'type': 'acquired.sale.offer',
             'id': event['id']
             }
             )
        print("SOCKET SEND ACQUIRED")

    def acquired_purchase_offer(self, event):
         self.send_json(
            {
                'type': 'acquired.purchase.offer',
                'id': event['id']
            }
        )

    def place_sale_offer(self, event):
         self.send_json(
            {
                'type': 'place.sale.offer',
                'id': event['id']
            }
            
        )
        

    def place_purchase_offer(self, event):
        self.send_json(
            {
            'type': 'place.purchase.offer',
            'id': event['id']
            }
            )
