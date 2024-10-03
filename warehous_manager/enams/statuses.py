from enum import Enum

class Statuses(str, Enum):
    IN_PROGRESS = 'в процессе'
    SENT = 'отправлен'
    DELIVERED = 'доставлен'
