# Image to GCode Converter

## Table of contents
- Overview
- What is GCode / CNC
- How to generate GCode

## Overview
This code example is part of a larger system that I built to convert Images into GCode.

## What is GCode / CNC
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
