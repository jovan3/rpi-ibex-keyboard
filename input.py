import uinput
from event_capability import UINPUT_CAPAB_LIST
from layout import KEY_CODES, MODIFIER_KEYS, FN_KEYS

class Input:

    PRESSED = 'pressed'
    RELEASED = 'released'
    
    def __init__(self):
        self.device = uinput.Device(UINPUT_CAPAB_LIST)
        self.state = set()

    def do_i2c_code(self, code):
        event, key = self.code_to_event(code)

        if event == Input.PRESSED:
            self.state.add(key)

            if self.fn_pressed():
                fn_keys_combo = self.keys_to_fn()
                if fn_keys_combo:
                    self.device.emit_combo(fn_keys_combo)
            elif self.modifier_pressed():
                combo = self.modifiers_first()
                print(combo)
                if combo:
                    self.device.emit_combo(combo)
            else:
                self.device.emit_click(key)

        if event == Input.RELEASED:
            self.state.remove(key)

    def modifier_pressed(self):
        return any(pressed in MODIFIER_KEYS for pressed in self.state)

    def fn_pressed(self):
        return uinput.ev.KEY_FN in self.state

    def keys_to_fn(self):
        combo = []
        for key in self.state:
            if key == uinput.ev.KEY_FN:
                continue
            
            combo += FN_KEYS.get(key, [key])
            
        return combo

    def modifiers_first(self):
        modifiers = []
        other = []
        
        for key in self.state:
            print(key)
            if key in MODIFIER_KEYS:
                modifiers.append(key)
            else:
                other.append(key)

        return modifiers + other
    
    def code_to_event(self, code):
        if code > 100:
            code_real_value = code - 100
            event = Input.PRESSED
        else:
            code_real_value = code
            event = Input.RELEASED
            
        key = KEY_CODES[code_real_value]

        return event, key
