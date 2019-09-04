import uinput
from layout import KEY_CODES, MODIFIER_KEYS, FN_KEYS

PRESSED = 'pressed'
RELEASED = 'released'

def modifier_pressed(state):
    return any(pressed in MODIFIER_KEYS for pressed in state)

def fn_pressed(state):
    return uinput.ev.KEY_FN in state

def keys_to_fn(state):
    combo = []
    for key in state:
        if key == uinput.ev.KEY_FN:
            continue
        
        combo += FN_KEYS.get(key, [key])
        
    return combo

def modifiers_first(state):
    modifiers = []
    other = []
        
    for key in state:
        print(key)
        if key in MODIFIER_KEYS:
            modifiers.append(key)
        else:
            other.append(key)
            
    return modifiers + other
    
def code_to_event(code):
    if code > 100:
        code_real_value = code - 100
        event = PRESSED
    else:
        code_real_value = code
        event = RELEASED
        
    key = KEY_CODES[code_real_value]
    
    return event, key
