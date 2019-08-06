import uinput
from event_capability import UINPUT_CAPAB_LIST

KEY_CODES = {
    51: uinput.KEY_3,
    52: uinput.KEY_4,
    53: uinput.KEY_5,
    54: uinput.KEY_6,
    55: uinput.KEY_7
}

class Input:

    PRESSED = 'pressed'
    UNPRESSED = 'unpressed'
    
    def __init__(self):
        self.device = uinput.Device(UINPUT_CAPAB_LIST)
        self.state = {}

    def do_i2c_code(self, code):
        event, key = self.code_to_event(code)

        if event == Input.PRESSED:
            print "click", key
            self.device.emit_click(key)

    def code_to_event(self, code):
        if code > 100:
            code_real_value = code - 100
            event = Input.UNPRESSED
        else:
            code_real_value = code
            event = Input.PRESSED
            
        key = KEY_CODES[code_real_value]

        return event, key
