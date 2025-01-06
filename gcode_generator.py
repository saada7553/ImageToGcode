import argparse
import numpy as np
import os
import sys
from trace_generator import TraceGenerator
from PIL import Image
from toolpaths import *
from toolpath_generator import ToolpathGenerator

class GCodeGenerator: 
    def __init__(self, toolpaths, output_path, feed_rate=500.0): 
        self.toolpaths = toolpaths
        self.feed_rate = feed_rate
        self.output_path = output_path
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
        for toolpath in self.toolpaths: 
            for i, command in enumerate(toolpath):
                # 0th command moves pen gantry to correct location with pen up. 
                # 1st command moves pen down to begin drawing. 
                if i == 0: 
                    self.gcode.append(self.pen_up_command.to_gcode())
                elif i == 1: 
                    self.gcode.append(self.pen_down_command.to_gcode()) 
                self.gcode.append(command.to_gcode())
    
    def generate_footer(self): 
        self.gcode.append(self.pen_up_command.to_gcode())
        self.gcode.append(self.return_to_home_gcode())
        self.gcode.append("M2 ; End the program.")
    
    def compile_gcode(self): 
        self.generate_header()
        self.convert_toolpath_to_gcode()
        self.generate_footer()
    
    def save_gcode(self): 
        with open(os.path.join(self.output_path, 'output.txt'), 'w') as f: 
            f.write("\n".join(self.gcode))

def main(): 
    parser = argparse.ArgumentParser(description="Convert a image into GCode by Saad Ata.")
    parser.add_argument("--input", "-i", required=True, help="Path to input image.")
    parser.add_argument("--output", "-o", required=True, help="Path to output GCode file.")
    parser.add_argument("--threshold", type=int, default=128,
                        help="Threshold for binarizing the image (0-255). Default=128")
    parser.add_argument("--scale", type=float, default=1,
                        help="Pixel to machine unit scale.")
    parser.add_argument("--arc_tolerance", type=float, default=0,
                        help="Maximum allowable deviation for arc fitting.")
    args = parser.parse_args()
   
    try:
        img = Image.open(args.input).convert("L")
    except IOError:
        print(f"Could not open the file.")
        sys.exit(1)

    # First convert the image to binary.
    # Every ON (1) pixel is where we need to draw. 
    width, height = img.size
    pixels = np.array(img)
    binary_image = np.where(pixels >= args.threshold, 0, 1)

    # Find the connected lines. 
    trace_generator = TraceGenerator(binary_image, width, height)
    traces = trace_generator.find_all_moore_traces()

    # Turn lines into toolpaths. 
    # This converter supports G1 (line) and G2/G3 (circular) instructions. 
    toolpath_gen = ToolpathGenerator(traces, scale=1, arc_tolerance=args.arc_tolerance)
    toolpath_gen.generate_toolpaths()

    # Turn the toolpaths into text which can be loaded directly to a CNC machine.
    gcode_gen = GCodeGenerator(
        toolpaths=toolpath_gen.toolpaths,
        output_path=args.output, 
        feed_rate=500
    )
    gcode_gen.compile_gcode()
    gcode_gen.save_gcode()

if __name__ == '__main__':
    main()
