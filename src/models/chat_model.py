class Message:
    """
    Una clase de datos simple para representar un mensaje en el chat.
    """
    def __init__(self, user_name: str, text: str, message_type: str):
        self.user_name = user_name
        self.text = text
        self.message_type = message_type