import os
import sys

class Colors:
    GREEN = "\033[92m"
    RED = "\033[91m"
    YELLOW = "\033[93m"
    BLUE = "\033[94m"
    BOLD = "\033[1m"
    RESET = "\033[0m"

def color_enabled(stream=None)->bool:
    """ True if we can enable colored output """
    stream = stream if stream is not None else sys.stdout
    if "NO_COLOR" in os.environ:
        return False
    return stream.isatty()

def paint(txt: str, *codes: str)->str:
    """ Paint text with codes """
    if not color_enabled():
        return txt
    return "".join(codes) + txt + Colors.RESET
