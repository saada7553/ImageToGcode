class ToolpathCommand: 
    def to_gcode(self): 
        raise NotImplemented("Must Implement Specific GCODE Instruction.")

class MoveTo(ToolpathCommand): 
    """
    Rapidly move to a given (X,Y) coordinate. 
    Uses G0 GCODE Instruction. 
    """ 
    def __init__(self, x, y): 
        self.x = x
        self.y = y
    
    def to_gcode(self):
        return f"G0 X{self.x:.3f} Y{self.y:.3f}"
    
class LinearMove(ToolpathCommand):
    """
    Move the machine in a straight line with G1 command. 
    """
    def __init__(self, x, y):
        self.x = x
        self.y = y
    
    def to_gcode(self):
        return f"G1 X{self.x:.3f} Y{self.y:.3f}"

class ArcMove(ToolpathCommand):
    """
    CW or CCW curved move with G2/G3 Command
    """
    def __init__(self, x, y, i, j, clockwise=True):
        self.x = x
        self.y = y
        self.i = i
        self.j = j
        self.clockwise = clockwise
    
    def to_gcode(self):
        cmd = "G2" if self.clockwise else "G3"
        return f"{cmd} X{self.x:.3f} Y{self.y:.3f} I{self.i:.3f} J{self.j:.3f}"

class SetFeedRate(ToolpathCommand):
    def __init__(self, feed_rate):
        self.feed_rate = feed_rate
    
    def to_gcode(self):
        return f"F{self.feed_rate:.1f}"

class PenUp(ToolpathCommand):
    """
    Actuates servo motor attached to pen gantry. 
    Used to stop drawing. 
    """
    def __init__(self, mode='M3'):
        self.mode = mode 
    
    def to_gcode(self):
        return self.mode

class PenDown(ToolpathCommand):
    """
    Pushes the pen down / starts drawing. 
    S20 is machine specific, 20 degrees
    rotation on servo is sufficiant for my 
    machine. 
    """
    def __init__(self, mode='M5 S20'):
        self.mode = mode 
    
    def to_gcode(self):
        return self.mode 

class ProgramEnd(ToolpathCommand):
    def to_gcode(self):
        return "M2" 
