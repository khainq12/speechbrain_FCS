import re
from typing import Dict, Tuple

class UAVMapper:
    def __init__(self):
        # BẢNG ÁNH XẠ DỰ KIẾN (Bạn cần điền thêm 31 intents của FSC vào đây)
        self.mapping_table = {
            # --- HE THONG (Lights/Lamp/Music) ---
            ("activate", "lamp", "none"): {"command_type": "system", "direction": "hover", "altitude_action": "hold", "magnitude": "medium", "urgency": "low", "safety": "strict"},
            ("activate", "lights", "bedroom"): {"command_type": "system", "direction": "hover", "altitude_action": "hold", "magnitude": "medium", "urgency": "low", "safety": "strict"},
            ("activate", "lights", "kitchen"): {"command_type": "system", "direction": "hover", "altitude_action": "hold", "magnitude": "medium", "urgency": "low", "safety": "strict"},
            ("activate", "lights", "none"): {"command_type": "system", "direction": "hover", "altitude_action": "hold", "magnitude": "medium", "urgency": "low", "safety": "strict"},
            ("activate", "lights", "washroom"): {"command_type": "system", "direction": "hover", "altitude_action": "hold", "magnitude": "medium", "urgency": "low", "safety": "strict"},
            ("activate", "music", "none"): {"command_type": "system", "direction": "hover", "altitude_action": "hold", "magnitude": "medium", "urgency": "low", "safety": "relaxed"},
            
            ("deactivate", "lamp", "none"): {"command_type": "system", "direction": "hover", "altitude_action": "hold", "magnitude": "medium", "urgency": "medium", "safety": "strict"},
            ("deactivate", "lights", "bedroom"): {"command_type": "system", "direction": "hover", "altitude_action": "hold", "magnitude": "medium", "urgency": "medium", "safety": "strict"},
            ("deactivate", "lights", "kitchen"): {"command_type": "system", "direction": "hover", "altitude_action": "hold", "magnitude": "medium", "urgency": "medium", "safety": "strict"},
            ("deactivate", "lights", "none"): {"command_type": "system", "direction": "hover", "altitude_action": "hold", "magnitude": "medium", "urgency": "medium", "safety": "strict"},
            ("deactivate", "lights", "washroom"): {"command_type": "system", "direction": "hover", "altitude_action": "hold", "magnitude": "medium", "urgency": "medium", "safety": "strict"},
            ("deactivate", "music", "none"): {"command_type": "system", "direction": "hover", "altitude_action": "hold", "magnitude": "medium", "urgency": "low", "safety": "normal"},
            
            # --- TRUY XUAT / GIAO TIEP (Bring items) ---
            ("bring", "juice", "none"): {"command_type": "fetch", "direction": "forward", "altitude_action": "lower", "magnitude": "small", "urgency": "medium", "safety": "normal"},
            ("bring", "newspaper", "none"): {"command_type": "fetch", "direction": "forward", "altitude_action": "lower", "magnitude": "small", "urgency": "medium", "safety": "normal"},
            ("bring", "shoes", "none"): {"command_type": "fetch", "direction": "forward", "altitude_action": "lower", "magnitude": "small", "urgency": "medium", "safety": "normal"},
            ("bring", "socks", "none"): {"command_type": "fetch", "direction": "forward", "altitude_action": "lower", "magnitude": "small", "urgency": "medium", "safety": "normal"},
            
            # --- CAU HINH (Change language) ---
            ("change language", "Chinese", "none"): {"command_type": "config", "direction": "hover", "altitude_action": "hold", "magnitude": "medium", "urgency": "low", "safety": "normal"},
            ("change language", "English", "none"): {"command_type": "config", "direction": "hover", "altitude_action": "hold", "magnitude": "medium", "urgency": "low", "safety": "normal"},
            ("change language", "German", "none"): {"command_type": "config", "direction": "hover", "altitude_action": "hold", "magnitude": "medium", "urgency": "low", "safety": "normal"},
            ("change language", "Korean", "none"): {"command_type": "config", "direction": "hover", "altitude_action": "hold", "magnitude": "medium", "urgency": "low", "safety": "normal"},
            ("change language", "none", "none"): {"command_type": "config", "direction": "hover", "altitude_action": "hold", "magnitude": "medium", "urgency": "low", "safety": "normal"},
            
            # --- DIEU CHINH MOI TRUONG (Heat/Volume) ---
            ("decrease", "heat", "bedroom"): {"command_type": "adjust", "direction": "hover", "altitude_action": "hold", "magnitude": "small", "urgency": "medium", "safety": "strict"},
            ("decrease", "heat", "kitchen"): {"command_type": "adjust", "direction": "hover", "altitude_action": "hold", "magnitude": "small", "urgency": "medium", "safety": "strict"},
            ("decrease", "heat", "none"): {"command_type": "adjust", "direction": "hover", "altitude_action": "hold", "magnitude": "small", "urgency": "medium", "safety": "strict"},
            ("decrease", "heat", "washroom"): {"command_type": "adjust", "direction": "hover", "altitude_action": "hold", "magnitude": "small", "urgency": "medium", "safety": "strict"},
            ("decrease", "volume", "none"): {"command_type": "adjust", "direction": "hover", "altitude_action": "hold", "magnitude": "small", "urgency": "low", "safety": "relaxed"},
            
            ("increase", "heat", "bedroom"): {"command_type": "adjust", "direction": "hover", "altitude_action": "hold", "magnitude": "large", "urgency": "high", "safety": "strict"},
            ("increase", "heat", "kitchen"): {"command_type": "adjust", "direction": "hover", "altitude_action": "hold", "magnitude": "large", "urgency": "high", "safety": "strict"},
            ("increase", "heat", "none"): {"command_type": "adjust", "direction": "hover", "altitude_action": "hold", "magnitude": "large", "urgency": "high", "safety": "strict"},
            ("increase", "heat", "washroom"): {"command_type": "adjust", "direction": "hover", "altitude_action": "hold", "magnitude": "large", "urgency": "high", "safety": "strict"},
            ("increase", "volume", "none"): {"command_type": "adjust", "direction": "hover", "altitude_action": "hold", "magnitude": "large", "urgency": "low", "safety": "relaxed"},
        }
        self.default_command = {
            "command_type": "unknown", 
            "direction": "hover", 
            "altitude_action": "hold"
        }

    def parse_fsc_string(self, fsc_raw_string: str) -> Tuple[str, str, str]:
        """Tách chuỗi dị của FSC ra thành 3 thành phần."""
        # Regex xử lý lỗi dư ':' ở action và dấu '|' phân cách
        match = re.findall(r'"action:"\s*"([^"]+)"\s*\|\s*"object":\s*"([^"]+)"\s*\|\s*"location":\s*"([^"]+)"', fsc_raw_string)
        if match:
            action, obj, loc = match[0]
            return action.strip(), obj.strip(), loc.strip()
        return None, None, None

    def map_fsc_to_uav(self, fsc_raw_string: str) -> Dict[str, str]:
        """Hàm chính: Nhận 1 chuỗi string, trả về dict UAV."""
        action, obj, loc = self.parse_fsc_string(fsc_raw_string)
        
        if not action:
            return self.default_command

        key = (action, obj, loc)
        return self.mapping_table.get(key, self.default_command)