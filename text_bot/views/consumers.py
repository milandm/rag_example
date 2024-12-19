import json
from .managers import ChatManager
from channels.generic.websocket import WebsocketConsumer
from channels.generic.websocket import AsyncWebsocketConsumer
from channels.layers import get_channel_layer
from text_bot.nlp_model.sales_agent.autogen_agent_perplexity import AutogenAgentPerplexity
from text_bot.nlp_model.openai_model import OpenaiModel
import asyncio
import uuid
from text_bot.nlp_model.sales_agent.chat_manager import ChatManager
from custom_logger.universal_logger import UniversalLogger

from channels.generic.websocket import AsyncWebsocketConsumer
import json



class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        await self.accept()
        await self.send(text_data=json.dumps({"message": "WebSocket connected!"}))

    async def disconnect(self, close_code):
        pass

    async def receive(self, text_data):
        await self.send(text_data=json.dumps({"message": f"You said: {text_data}"}))



class ChatConsumerNN(AsyncWebsocketConsumer):

    def __init__(self):
        super().__init__()
        # Create the AutogenAgentPerplexity instance with a callback reference
        self.autogen_agent_perplexity = AutogenAgentPerplexity(OpenaiModel(), self.ask_human_question)
        self.pending_requests = {}

    async def connect(self):
        await self.accept()

    async def disconnect(self, close_code):
        pass

    async def receive(self, text_data):
        data = json.loads(text_data)
        request_id = data.get('requestId')
        answer = data.get('answer')  # The user's response

        # If this matches a pending request, set its result
        if request_id and request_id in self.pending_requests:
            self.pending_requests[request_id].set_result(answer)
            del self.pending_requests[request_id]

    async def ask_human_question(self, question: str) -> str:
        """
        This method is the callback used by the agent to ask a human a question.
        It sends a message to the client and waits for the response.
        """
        request_id = str(uuid.uuid4())
        future = asyncio.get_event_loop().create_future()
        self.pending_requests[request_id] = future

        # Send the question to the human with a unique request ID
        await self.send(text_data=json.dumps({
            "action": "askHuman",
            "question": question,
            "requestId": request_id
        }))

        # Wait for the human's response
        try:
            answer = await asyncio.wait_for(future, timeout=300)  # e.g., 5 min timeout
            return answer
        except asyncio.TimeoutError:
            del self.pending_requests[request_id]
            return "No response received in time."

    # Optional method to initiate the process
    async def start_agent_task(self):
        # Example: start some task that may require human input
        result = await self.autogen_agent_perplexity.run_group_agent()
        await self.send(text_data=json.dumps({"info": "Agent task completed"}))



class ChatConsumer5(AsyncWebsocketConsumer):
    async def connect(self):
        await self.accept()
        self.chat_manager = ChatManager(self)
        print("WebSocket connected.")

    async def disconnect(self, close_code):
        print("WebSocket disconnected.")

    async def receive(self, text_data):
        """
        Handle incoming messages from the client.
        """
        message = json.loads(text_data)
        request_id = message.get("requestId")

        # Delegate message processing to ChatManager
        if request_id:
            await self.chat_manager.handle_client_response(message)
        else:
            await self.chat_manager.process_client_request(message)

    async def send_json(self, data):
        """
        Utility function to send JSON data.
        """
        await self.send(text_data=json.dumps(data))

    async def start_server_request(self):
        """
        Example: Send a server request to the client and wait for a response.
        """
        request_message = {"action": "getClientInfo", "details": "Requesting client information"}
        response = await self.chat_manager.send_request_to_client(request_message)
        print("Response received from client:", response)





# SyncWebSocketConsumer
class ChatConsumer6(AsyncWebsocketConsumer):

    def __init__(self):
        self.autogen_agent_perplexity = AutogenAgentPerplexity(OpenaiModel())




    async def connect(self):
        await self.accept()
        self.pending_requests = {}  # Store pending request futures


    async def disconnect(self, close_code):
        pass


    async def receive(self, text_data):
        data = json.loads(text_data)
        request_id = data.get('requestId')

        # If response matches a pending request, resolve the future
        if request_id and request_id in self.pending_requests:
            self.pending_requests[request_id].set_result(data)
            del self.pending_requests[request_id]


    async def send_message_and_wait(self, message):
        request_id = str(uuid.uuid4())  # Generate a unique request ID
        message['requestId'] = request_id

        # Create a future to wait for a response
        future = asyncio.get_event_loop().create_future()
        self.pending_requests[request_id] = future

        # Send the message
        await self.send(text_data=json.dumps(message))

        # Wait for the response
        try:
            response = await asyncio.wait_for(future, timeout=5)
            return response
        except asyncio.TimeoutError:
            del self.pending_requests[request_id]
            return {'error': 'Timeout waiting for client response'}


    async def send_and_get_response(self):
        # Example of sending a message and waiting for a synchronous response
        message = {"action": "getTime"}
        response = await self.send_message_and_wait(message)
        print("Received Response:", response)

        # You can send further messages or process the response as needed
        await self.send(text_data=json.dumps({"serverStatus": "Response processed"}))



    async def start_communication(self):
        # Initiating a request-response exchange
        await self.send_and_get_response()




class ChatConsumer4(AsyncWebsocketConsumer):


    async def connect(self):
        """
        Called when a WebSocket connection is opened.
        """
        self.group_name = "global_chat"  # Group name for all clients

        # Join the group
        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )
        await self.accept()


        await self.send(text_data=json.dumps({"message": "WebSocket connection established!"}))


        # self.chat_manager = ChatManager(self.room_group_name)
        self.autogen_agent_perplexity = AutogenAgentPerplexity(OpenaiModel())


        # Send welcome message
        await self.send(text_data=json.dumps({
            'message': f"Connected to room: {self.room_name}"
        }))



    async def disconnect(self, close_code):
        """
        Called when the WebSocket disconnects.
        """
        # Remove the client from the group
        await self.channel_layer.group_discard(self.group_name, self.channel_name)

    async def receive(self, text_data):
        """
        Called when a message is received from the client.
        """
        data = json.loads(text_data)
        message = data.get('message', 'No message')

        # Echo the message back to the client
        await self.send(text_data=json.dumps({
            "sender": "Server",
            "response": f"You said: {message}"
        }))

    async def chat_message(self, event):
        """
        Handles messages sent to the group from the backend.
        """
        message = event['message']

        # Send the message to WebSocket
        await self.send(text_data=json.dumps({
            "sender": "Backend",
            "message": message
        }))





class ChatConsumer1(WebsocketConsumer):

    def connect(self):
        self.accept()


    def disconnect(self, close_code):
        pass


    def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message = text_data_json['message']
        self.send(text_data=json.dumps({
            'message': message
        }))


class ChatConsumer3(WebsocketConsumer):

    async def connect(self):
        # Accept the WebSocket connection
        await self.accept()
        print("WebSocket connected")

        # Send a welcome message to the client
        await self.send(text_data=json.dumps({
            'message': 'Welcome to the WebSocket!',
            'status': 'connected'
        }))


    async def disconnect(self, close_code):
        # Handle disconnection
        print("WebSocket disconnected with code:", close_code)


    async def receive(self, text_data):
        """
        Receive a message from the WebSocket client and send a response back.
        """
        data = json.loads(text_data)  # Parse incoming message
        message = data.get('message', 'No message received')

        print("Received:", message)

        # Send a response back to the client
        await self.send(text_data=json.dumps({
            'response': f"Message received: {message}",
            'status': 'ok'
        }))




class ChatConsumer2(AsyncWebsocketConsumer):


    async def connect(self):
        self.room_name = self.scope['url_route']['kwargs']['room_name']
        self.room_group_name = f"chat_{self.room_name}"
        self.chat_manager = ChatManager(self.room_group_name)

        # Join the group
        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )
        await self.accept()

        # Send welcome message
        await self.send(text_data=json.dumps({
            'message': f"Connected to room: {self.room_name}"
        }))

    async def disconnect(self, close_code):
        # Leave the group
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )

    async def receive(self, text_data):
        """
        Handle receiving a message from the WebSocket client.
        """
        data = json.loads(text_data)
        message = data.get('message')
        username = data.get('username', 'Anonymous')

        # Send the message via ChatManager
        self.chat_manager.send_message(username, message)

    async def chat_message(self, event):
        """
        Handle messages sent to the group.
        """
        # Forward the received message to WebSocket
        await self.send(text_data=json.dumps({
            'username': event['username'],
            'message': event['message']
        }))


