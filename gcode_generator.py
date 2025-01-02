import numpy as np
import sys
from contour_generator import ContourGenerator
from PIL import Image
from toolpaths import *
from toolpath_generator import ToolpathGenerator

class GCodeGenerator: 

    def __init__(self, toolpaths, feed_rate=500.0,): 
        self.toolpaths = toolpaths
        self.feed_rate = feed_rate
        self.gcode = []
        self.pen_up_command = PenUp()
        self.pen_down_command = PenDown()
    
    def return_to_home_gcode(self): 
        return LinearMove(0, 0).to_gcode()
    
    def generate_header(self): 
        self.gcode.append("; GCode generated from image by Saad Ata.")
        self.gcode.append("G21 ; Set units to millimeters.")
        self.gcode.append("G90 ; Use absolute positioning.")
        self.gcode.append(self.pen_up_command.to_gcode())
        self.gcode.append(self.return_to_home_gcode())
    
    def convert_toolpath_to_gcode(self): 
        for i, toolpath in enumerate(self.toolpaths): 
            if not toolpath: 
                continue
                
            self.gcode.append(self.pen_down_command.to_gcode())
            for command in toolpath: 
                self.gcode.append(command.to_gcode())
            self.gcode.append(self.pen_up_command.to_gcode())
    
    def generate_footer(self): 
        self.gcode.append(self.return_to_home_gcode())
        self.gcode.append("M2 ; End the program.")
    
    def compile_gcode(self): 
        self.generate_header()
        self.convert_toolpath_to_gcode()
        self.generate_footer()
    
    def save_gcode(self): 
        with open('output.txt', 'w') as f: 
            f.write("\n".join(self.gcode))

def main(): 
    try:
        img = Image.open("/Users/saad/Downloads/descologo.png").convert("L")
    except IOError:
        print(f"Error: Unable to open image file.")
        sys.exit(1)

    width, height = img.size
    pixels = np.array(img)
    binary_image = np.where(pixels >= 0.5, 1, 0)

    contour_generator = ContourGenerator(binary_image, width, height)
    contours = contour_generator.find_contours()

    toolpath_gen = ToolpathGenerator(contours, scale=1, arc_tolerance=0)
    toolpath_gen.generate_toolpaths()

    gcode_gen = GCodeGenerator(
        toolpaths=toolpath_gen.toolpaths,
        feed_rate=500
    )
    gcode_gen.compile_gcode()
    gcode_gen.save_gcode()

if __name__ == '__main__':
    main()