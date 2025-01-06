# Image to GCode Converter

## Table of contents
- [Overview](#overview)
- [What is GCode and CNC](#what-is-gcode-and-cnc)
- [How to generate GCode](#how-to-generate-gcode)
- [Why convert images to GCode](#why-convert-images-to-gcode)
- [How this converter works](#how-this-converter-works)
- [Results](#results)
- [Future plans](#future-plans)

## Overview
This code sample is part of a larger system that I built to convert Images into GCode. This code was originally meant to be used alongside a frontend application which could visualize the images and the generated GCode. I have converted it to a CLI interface to simplify it down to the core logic. 

## What is GCode and CNC
GCode, also known as Geometric Code is used to control CNC (computer numerical control) machines. Here is what a CNC machine looks like:  

![ezgif-6-36a6f9987d](https://github.com/user-attachments/assets/18919437-dbe0-46e9-a8bd-727d28c98ce4)

Some other examples include 3D printers, laser cutters, and pen plotters (this one will be important later). A CNC machine uses software to control the movement of its various tools. This software is called GCode. Here is what GCode looks like: 

```
; Basic GCode Example

G21             ; Set units to millimeters
G90             ; Absolute positioning

; Draw a line
G1 X10 Y10 F1000 ; Move to start point of the line
G1 X50 Y10 F1000 ; Draw a line to (50, 10)

; Draw a circle
G1 X30 Y30 F1000 ; Move to circle start point
G2 X50 Y30 I10 J0 F1000 ; Draw a clockwise circle with center at (40, 30)

M30              ; Program end
```

## How to generate GCode
Traditionally, GCode is generated with Computer Aided Design (CAD). Designers make 3D meshes using software such as AutoCAD. These meshes and designs are then compiled into GCode. This GCode can be loaded onto any CNC machine which will then produce the desired part. 

![image](https://github.com/user-attachments/assets/ccdb9121-e5a1-4ebb-b344-c3447442bf0a)

## Why convert images to GCode
Most CNC machines are used to presisely maunfacture 3D parts. Software such as AutoCAD and Onshape are built specifically to work with 3D models. However, the type of CNC machine that I want to produce GCode instructions for is called a pen plotter (my machine shown below). A pen plotter is used to draw pictures or write text using a pen. This machine is different from a traditional CNC machine as it can only move in 2D. 

<img width="1399" alt="Screenshot 2025-01-04 at 7 07 06 PM" src="https://github.com/user-attachments/assets/c7849c32-7c8d-4107-a87d-3546d19a563f" />

AutoCAD can produce GCode instructions for pen plotters. However, these 3D modeling softwares were never built with this type of functionality in mind. They struggle with modeling large amounts of text. Their options for formatting text are also very limited. Additionally, if you need your pen plotter to draw out an image, AutoCAD requires the image to be manually traced, a process that is clunky and not well-suited for a software primarily designed for engineering and architectural purposes. For this reason, I built this image to GCode converter so that I can easily produce instructions for my pen plotter. 

## How this converter works

- Step 1: Convert the input image into a binary format.
- Step 2: Turn the binary image into line traces.
- Step 3: Turn traces into toolpaths.
- Step 4: Resolve toolpaths into GCode.

### Step 1: Convert the input image into a binary format.
The `gcode_generator.py` file contains the main function which uses `argparser` to retrieve the path to the input image. The input image is transformed into a numpy array. A 1 is assigned to each pixel above the inputted brightness threshold, while a 0 is assigned to each pixel below the threshold. The pen plotter will draw the locations marked with a 1. 

### Step 2: Turn the binary image into line traces.
When you write text on a piece of paper, you place the pen down on the page, move it, and then pick it back up in preperation for the next character. Similarly, for this converter, I define a singular `trace` to be the previous 3 steps. We need to transform the binary image we produced in Step 1 into a list of traces. These traces are lists of connected components which can be drawn with a single stroke of a pen. The `trace_generator.py` file is responsile for finding these traces.

### Step 3: Turn traces into toolpaths.
This is the most involved step in the GCode generation logic. In `toolpath_generator.py`, we have access to the list of traces we need to draw. The traces are made up of hundreds of different points. GCode allows us to connect these points by moving the tool gantry in a straight line with the `G1` command from point to point. However, this is not optimal in many cases. If we need to draw a smooth curve, the linear `G1` command would cause the curve to appear jagged. 

To solve this problem, GCode allows us to move in arcs with the `G2` or `G3` instructions. The `ToolpathGenerator` looks at each trace and tries to find all of the points that it can connect with a arc. Within a single trace, there may be some points which do not fit well within a given arc. We allow some slack (tolerance) between the original points and the GCode arc that represents those points. If an arc can not be fit, we fallback to connecting the points with a straight line (`G1`). 

In order to find a circle or arc which best fits a set of points, I implemented a simple `least squares circle fit` algorithm. Some of the theory behind that algorithm can be found here: http://www.juddzone.com/ALGORITHMS/least_squares_circle.html

### Step 4: Resolve toolpaths into GCode.
The final step is to convert the `ToolpathCommand` objects into the text GCode format that the machine can understand. Here, we add the `PenUp`, `PenDown` and `return_to_home` commands that are needed in between the traces. Additionally, we add a header and footer to the GCode for machine-specific configurations. Finally, the GCode is saved in `output.txt` at the specified output directory. 

## Results
`Top`: Input image. `Bottom`: Visualized output GCode. 

<img width="491" alt="Screenshot 2025-01-06 at 3 10 56 AM" src="https://github.com/user-attachments/assets/da1fc957-16a5-42a1-9415-07ded3430200" />

### Watch working pen plotter hardware with the generated instructions:
https://github.com/user-attachments/assets/58ecec79-eaad-49ac-a0cb-0d6fe1f2feaf

## Future plans
- Replace machine raspberry PI with a custom FPGA module. This would allow me to have more control over the stepper motors with pulse width modulation. Currently experimenting with Basys2 FPGA. 
- I want to add support for more advanced GCode toolpaths involving variable feed rates. Straight lines should be drawn faster than tight curves.
- Build a 3D GCode visualiser. 
