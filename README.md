# Image to GCode Converter

## Table of contents
- Overview
- What is GCode / CNC
- How to generate GCode
- Why convert images to GCode

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

## How to generate GCode
Traditionally, GCode is generated with Computer Aided Design (CAD). Designers make 3D meshes using software such as AutoCAD. These meshes and designs are then compiled into GCode. This GCode can be loaded onto any CNC machine which will then produce the desired part. 

![image](https://github.com/user-attachments/assets/ccdb9121-e5a1-4ebb-b344-c3447442bf0a)

## Why convert images to GCode
Most CNC machines are used to presisely maunfacture 3D parts. Software such as AutoCAD and Onshape are built specifically to work with 3D models. However, the type of CNC machine that I want to produce GCode instructions for is called a pen plotter (my machine shown below). A pen plotter is used to draw pictures or write text using a pen. This machine is different from a traditional CNC machine as it can only move in 2D. 

<img width="1399" alt="Screenshot 2025-01-04 at 7 07 06 PM" src="https://github.com/user-attachments/assets/c7849c32-7c8d-4107-a87d-3546d19a563f" />


AutoCAD can produce GCode instructions for pen plotters. However, these 3D modeling softwares were never built with this type of functionality in mind. They struggle with modeling large amounts of text. Their options for formatting text is also very limited. Additionally, if you need your pen plotter to draw out an image, AutoCAD requires the image to be manually traced, a process that is clunky and not well-suited for a software primarily designed for engineering and architectural purposes. For this reason, I built this image to GCode converter so that I can easily produce instructions for my pen plotter. 
