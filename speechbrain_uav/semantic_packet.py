import json

class SemanticPacket:
    def __init__(self, command_type, direction, altitude_action, magnitude_rank, urgency_rank, safety_rank, confidence):
        self.command_type = command_type
        self.direction = direction
        self.altitude_action = altitude_action
        self.magnitude_rank = magnitude_rank
        self.urgency_rank = urgency_rank
        self.safety_rank = safety_rank
        self.confidence = confidence

    def serialize(self) -> str:
        """Chuyển thành chuỗi JSON để gửi đi"""
        return json.dumps(self.__dict__)

    @classmethod
    def deserialize(cls, json_str: str) -> 'SemanticPacket':
        """Nhận chuỗi JSON và khôi phục lại Packet"""
        data = json.loads(json_str)
        return cls(**data)

    def to_token_sequence(self) -> list:
        """Chuyển thành chuỗi số để ném vào Semantic Comm Stub"""
        # Ví dụ mã hóa đơn giản
        return [
            hash(self.command_type) % 10, 
            hash(self.direction) % 10, 
            hash(self.altitude_action) % 10, 
            self.magnitude_rank, 
            self.urgency_rank, 
            self.safety_rank, 
            int(self.confidence * 100)
        ]