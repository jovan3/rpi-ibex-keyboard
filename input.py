import uinput
from event_capability import UINPUT_CAPAB_LIST
from layout import KEY_CODES, MODIFIER_KEYS

class Input:

    PRESSED = 'pressed'
    RELEASED = 'released'
    
    def __init__(self):
        self.device = uinput.Device(UINPUT_CAPAB_LIST)
        self.state = set()

    def do_i2c_code(self, code):
        event, key = self.code_to_event(code)

        print key
        
        if event == Input.PRESSED:
            self.state.add(key)
            
            if any(pressed in MODIFIER_KEYS for pressed in self.state):
                self.device.emit_combo(list(self.state))
            else:
                self.device.emit_click(key)

        if event == Input.RELEASED:
            self.state.remove(key)

        print "New state ", self.state

    def code_to_event(self, code):
        if code > 100:
            code_real_value = code - 100
            event = Input.PRESSED
        else:
            code_real_value = code
            event = Input.RELEASED
            
        key = KEY_CODES[code_real_value]

        return event, key
