import uinput
import inspect

# A list of event capability descriptors for a uinput Device
UINPUT_CAPAB_LIST = [attr[1] for attr in inspect.getmembers(uinput.ev) if attr[0].startswith('KEY')]
