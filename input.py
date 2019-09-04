import uinput
import event_util
from event_capability import UINPUT_CAPAB_LIST


class Input:
    
    def __init__(self):
        self.device = uinput.Device(UINPUT_CAPAB_LIST)
        self.state = set()

    def do_i2c_code(self, code):
        event, key = event_util.code_to_event(code)

        if event == event_util.PRESSED:
            self.state.add(key)

            if event_util.fn_pressed(self.state):
                fn_keys_combo = event_util.keys_to_fn(self.state)
                if fn_keys_combo:
                    self.device.emit_combo(fn_keys_combo)
            elif event_util.modifier_pressed(self.state):
                combo = event_util.modifiers_first(self.state)
                print(combo)
                if combo:
                    self.device.emit_combo(combo)
            else:
                self.device.emit_click(key)

        if event == event_util.RELEASED:
            self.state.remove(key)

