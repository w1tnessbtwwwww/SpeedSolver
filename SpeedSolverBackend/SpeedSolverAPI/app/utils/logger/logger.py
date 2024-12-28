from abc import ABC, abstractmethod

class Logger(ABC):
    
    @abstractmethod
    async def send_log(message: str = "Empty Log"):
        ...