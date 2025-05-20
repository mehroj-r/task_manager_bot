from enum import Enum

class TasksListMessageType(Enum):
    """
    Enum for the type of message in the tasks list.
    """
    MESSAGE = "message"
    CALLBACK_QUERY = "callback_query"