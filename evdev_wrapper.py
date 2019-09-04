from evdev import UInput, ecodes
import event_util


def uinput_key_ev_to_ecode(uinput_ev):
    """ Returns ecode (integer) for uinput key event, asuming the event is a tuple with "1" ass the first element ((1, X), where X is the actual key code. """
    _, code = uinput_ev
    return code

def ecode_to_uinput_key_ev(ecode):
    _, code = ecode
    return (1, code)

class EvdevInput:
    """ evdev wrapper around the uinput keyboard device. Some game emulators can't handle
events coming from python-uinput directly, but have no issues with evdev generated input events. """

    def __init__(self):
        self.uinput = UInput()
        self.state = set()

    def do_i2c_code(self, code):
        event, key = event_util.code_to_event(code)
        ecode = uinput_key_ev_to_ecode(key)
        
        if event == event_util.PRESSED:
            self.state.add(key)

            if event_util.fn_pressed(self.state):
                fn_keys_combo = event_util.keys_to_fn(self.state)

                if fn_keys_combo:
                    evdev_key_combo = [uinput_key_ev_to_ecode(k) for k in fn_keys_combo]
                    for key in evdev_key_combo:
                        self.press(key)
                    for key in evdev_key_combo:
                        self.release(key)
            else:
                self.press(ecode)        

        elif event == event_util.RELEASED:
            self.release(ecode)
            self.state.remove(key)


    def press(self, key):
        self.uinput.write(ecodes.EV_KEY, key, 1)
        self.uinput.syn()

    def release(self, key):
        self.uinput.write(ecodes.EV_KEY, key, 0)
        self.uinput.syn()
        
