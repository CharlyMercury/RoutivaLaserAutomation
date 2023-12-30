#!/usr/bin/env python
# -*- coding: utf-8 -*-
#  DXF-GCODE.py
#  DXF to G-Code converter VERSION 2
#  Turns only Lines and Polylines into engraving machining moves on layer 'CUT' (not arcs or circles etc.)
#  Drill holes through all circles smaller than set radius.
#  Turns Polylines into through machining moves on layer 'THROUGH' (not arcs or circles etc.)
#  https://sites.google.com/site/richardcncprojects/
#  This program is free software; you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation; either version 2 of the License, or
#  (at your option) any later version.
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#  You should have received a copy of the GNU General Public License
#  along with this program; if not, write to the Free Software
#  Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston,
#  MA 02110-1301, USA.
import os
import datetime

# Alter these variables and file paths to suit your PC and CNC machine
open_file_path = r"C:\Users\Charly Mercury\Desktop\dxt_to_g_code\examples\example_2_circle.dxf"
save_file = r"C:\Users\Charly Mercury\Desktop\dxt_to_g_code\examples\example_2_circle.txt"
safe_height = "10"
SKIMHEIGHT = "3"
STARTHEIGHT = "1"
CUTDEPTH = "-2"  # PCB=-0.15 Wood=-2
FEEDRATE = "600"  # PCB=200 Engrave=600
TCUTDEPTH = -8  # Through cut depth
TFEEDRATE = "200"  # Through cut feed rate
TSTEP = -2  # Through cut depth step size
DRILLDEPTH = "-1.8"  # Depth of drilled through holes
DRILLRATE = "100"  # PCB=30
FINISHPOS = "G0 Y100"  # Move out the way when finished
QTY = 1000  # Quantity of memory to be used
R = 2  # Round off to decimal places
CIRCLERAD = 0.51  # Maximum circle radius to drill
ZEROFLAG = False  # Machines 'L' at x0 y0 to check for missed steps

# Varibles used by program. Do not alter !
TEXT = ""
ERROR = ""
VALUE = ""
LINECOUNT = 1
LINEPOST = 0
HOLECOUNT = 1
BIGCOUNT = 0
COUNT = 0
POLYCOUNT = 0
POLYPOSITION = 0
POLYPOST = 0
THROUGHPOST = 0
FEEDFLAG = 0
XMAX = 0
XMIN = 0
YMAX = 0
YMIN = 0
XSTART = [0 for i in range(QTY)]
YSTART = [0 for i in range(QTY)]
XEND = [0 for i in range(QTY)]
YEND = [0 for i in range(QTY)]
XHOLE = [0 for i in range(QTY)]
YHOLE = [0 for i in range(QTY)]
RADIUS = [0 for i in range(QTY)]
POLYLINEX = [[0 for k in range(QTY)] for j in range(QTY)]
POLYLINEY = [[0 for k in range(QTY)] for j in range(QTY)]
POLYLINEQTY = [0 for k in range(QTY)]
POLYOPEN = [0 for k in range(QTY)]  # 0=open 1=closed
POLYLAYER = ["" for i in range(QTY)]
LINELAYER = ["" for i in range(QTY)]
HOLELAYER = ["" for i in range(QTY)]
DXFPATH, DXFNAME = os.path.split(open_file_path)
ZEROCHECK = "( ZERO CHECK )\n"
ZEROCHECK = ZEROCHECK + "G0 Z10\n"
ZEROCHECK = ZEROCHECK + "X0\n" + " Y2.54\n"
ZEROCHECK = ZEROCHECK + "Z1\n"
ZEROCHECK = ZEROCHECK + "G1 Z-0.15 F30\n"
ZEROCHECK = ZEROCHECK + "Y0 F200\n"
ZEROCHECK = ZEROCHECK + "X2.54\n"
ZEROCHECK = ZEROCHECK + "G0 Z10\n"


# Read DXF file #
file = open(open_file_path, "r")

while True:  #### Main DXF read loop ####
    TEXT = file.readline()
    TEXT = TEXT.strip()  # Remove spaces
    if TEXT == "LINE":  # Found line ( was 'AcDbLine' )
        while True:
            TEXT = file.readline()  # Read identifier
            TEXT = TEXT.strip()
            if TEXT == "0":  # No more data
                if (YSTART[LINECOUNT] > YMAX): YMAX = YSTART[LINECOUNT]
                if (YSTART[LINECOUNT] < YMIN): YMIN = YSTART[LINECOUNT]
                if (YEND[LINECOUNT] > YMAX): YMAX = YEND[LINECOUNT]
                if (YEND[LINECOUNT] < YMIN): YMIN = YEND[LINECOUNT]
                if (XSTART[LINECOUNT] > XMAX): XMAX = XSTART[LINECOUNT]
                if (XSTART[LINECOUNT] < XMIN): XMIN = XSTART[LINECOUNT]
                if (XEND[LINECOUNT] > XMAX): XMAX = XEND[LINECOUNT]
                if (XEND[LINECOUNT] < XMIN): XMIN = XEND[LINECOUNT]
                LINECOUNT = LINECOUNT + 1
                break
            VALUE = file.readline()  # Read value
            VALUE = VALUE.strip()
            if TEXT == "8":  # Layer
                LINELAYER[LINECOUNT] = VALUE
                TEXT = "NOTHING"
            if TEXT == "10":
                # TEXT = file.readline() # Read X start poosition
                # TEXT = TEXT.strip()
                XSTART[LINECOUNT] = float(VALUE)
                TEXT = "NOTHING"
            if TEXT == "20":
                # TEXT = file.readline() # Read Y start poosition
                # TEXT = TEXT.strip()
                YSTART[LINECOUNT] = float(VALUE)
                TEXT = "NOTHING"
            if TEXT == "11":
                # TEXT = file.readline() # Read X end poosition
                # TEXT = TEXT.strip()
                XEND[LINECOUNT] = float(VALUE)
                TEXT = "NOTHING"
            if TEXT == "21":
                # TEXT = file.readline() # Read Y end poosition
                # TEXT = TEXT.strip()
                YEND[LINECOUNT] = float(VALUE)
                TEXT = "NOTHING"
    if TEXT == "CIRCLE":  # Found circle
        while True:
            TEXT = file.readline()  # Read identifier
            TEXT = TEXT.strip()
            if TEXT == "0":  # No more data
                if XHOLE[HOLECOUNT] + RADIUS[HOLECOUNT] > XMAX: XMAX = XHOLE[HOLECOUNT]
                if XHOLE[HOLECOUNT] - RADIUS[HOLECOUNT] < XMIN: XMIN = XHOLE[HOLECOUNT]
                if YHOLE[HOLECOUNT] + RADIUS[HOLECOUNT] > YMAX: YMAX = YHOLE[HOLECOUNT]
                if YHOLE[HOLECOUNT] - RADIUS[HOLECOUNT] < YMIN: YMIN = YHOLE[HOLECOUNT]
                HOLECOUNT = HOLECOUNT + 1
                break
            VALUE = file.readline()  # Read value
            VALUE = VALUE.strip()
            if TEXT == "8":  # Layer
                HOLELAYER[HOLECOUNT] = VALUE
                TEXT = "NOTHING"
            if TEXT == "10":
                # TEXT = file.readline() # Read X centre poosition
                # TEXT = TEXT.strip()
                XHOLE[HOLECOUNT] = float(VALUE)
                TEXT = "NOTHING"
            if TEXT == "20":
                # TEXT = file.readline() # Read Y centre poosition
                # TEXT = TEXT.strip()
                YHOLE[HOLECOUNT] = float(VALUE)
                TEXT = "NOTHING"
            if TEXT == "40":
                # TEXT = file.readline() # Read radius
                # TEXT = TEXT.strip()
                RADIUS[HOLECOUNT] = float(VALUE)
                if RADIUS[HOLECOUNT] > CIRCLERAD: BIGCOUNT = BIGCOUNT + 1
                TEXT = "NOTHING"
    if TEXT == "LWPOLYLINE":  # Found Polyline (was 'AcDbPolyline')
        POLYCOUNT = POLYCOUNT + 1
        POLYPOSITION = 1
        FOUNDFLAG = False
        while True:
            TEXT = file.readline()  # Read identifier
            TEXT = TEXT.strip()
            if TEXT == "0" and FOUNDFLAG == True:  # End of data
                POLYLINEQTY[POLYCOUNT] = POLYPOSITION
                break  # No more data
            VALUE = file.readline()  # Read value
            VALUE = VALUE.strip()
            if TEXT == "8":  # Layer
                POLYLAYER[POLYCOUNT] = VALUE
                TEXT = "NOTHING"
            if TEXT == "70":  # Open or closed loop
                POLYOPEN[POLYCOUNT] = float(VALUE)
                TEXT = "NOTHING"
            if TEXT == "10":  # X Position
                POLYLINEX[POLYCOUNT][POLYPOSITION] = float(VALUE)
                TEXT = "NOTHING"
                if float(VALUE) > XMAX: XMAX = float(VALUE)
                if float(VALUE) < XMIN: XMIN = float(VALUE)
                FOUNDFLAG = True
            if TEXT == "20":  # Y Position
                POLYLINEY[POLYCOUNT][POLYPOSITION] = float(VALUE)
                TEXT = "NOTHING"
                if float(VALUE) > YMAX: YMAX = float(VALUE)
                if float(VALUE) < YMIN: YMIN = float(VALUE)
                POLYPOSITION = POLYPOSITION + 1
    if LINECOUNT >= QTY:
        ERROR = ERROR + "ERROR - Ran out of dimentioned line arrey. Increase QTY value.\n"
        TEXT = "EOF"
        break
    if HOLECOUNT >= QTY:
        ERROR = ERROR + "ERROR - Ran out of dimentioned circle arrey. Increase QTY value.\n"
        TEXT = "EOF"
        break
    if TEXT == "EOF":
        break
file.close()


# Display data from .DXF	#
for i in range(1, LINECOUNT):  # Display line data
    print("Line", i, "Start X ", XSTART[i], " Y", YSTART[i], " End X", XEND[i], " Y", YEND[i], " Layer =", LINELAYER[i])
for i in range(1, HOLECOUNT):  # Display hole data
    print("Circle ", i, " X", XHOLE[i], " Y", YHOLE[i], " Radius", RADIUS[i], " Layer =", HOLELAYER[i])
for i in range(1, POLYCOUNT + 1):  # Display polyline data
    print("Polyline =", i, "    Open/Closed =", POLYOPEN[i], "    Layer =", POLYLAYER[i])
    for j in range(1, POLYLINEQTY[i]):
        print("X", POLYLINEX[i][j], " Y ", POLYLINEY[i][j])
    # Next j
# Next i


# Create G-Code #
GCODE = "(" + DXFNAME + ")\n"
# GCODE = GCODE + "(" + str(datetime.datetime.now()) + ")\n"
AAA = datetime.datetime.now()
BBB = AAA.strftime("%d %B %Y %H:%M:%S")
GCODE = GCODE + "(" + BBB + ")\n"
GCODE = GCODE + "(X MIN=" + str(round(XMIN, R)) + " MAX=" + str(round(XMAX, R)) + ")\n"
GCODE = GCODE + "(Y MIN=" + str(round(YMIN, R)) + " MAX=" + str(round(YMAX, R)) + ")\n"
GCODE = GCODE + "G90 G17 G21\n"  # Absolute, XY plane, MM
GCODE = GCODE + "G0 Z" + safe_height + "\n"
GCODE = GCODE + "(OUTSIDE TEST)\n"
GCODE = GCODE + "G0 X" + str(round(XMIN, R)) + " Y" + str(round(YMIN, R)) + "\n"
GCODE = GCODE + "G0 Y" + str(round(YMAX, R)) + "\n"
GCODE = GCODE + "G0 X" + str(round(XMAX, R)) + "\n"
GCODE = GCODE + "G0 Y" + str(round(YMIN, R)) + "\n"
GCODE = GCODE + "G0 X" + str(round(XMIN, R)) + "\n"
GCODE = GCODE + "M3 S1000\n"  # Spindle motor on
if ZEROFLAG:
    GCODE = GCODE + ZEROCHECK


# Engrave polilines ( Layer = CUT ) #
GCODE = GCODE + "(MACHINE POLYLINES)\n"  # Remark
GCODE = GCODE + "G0 Z" + SKIMHEIGHT + "\n"
for i in range(1, POLYCOUNT + 1):
    if POLYLAYER[i] == "CUT":
        POLYPOST = POLYPOST + 1
        GCODE = GCODE + "(POLYLINE " + str(POLYPOST) + ")\n"
        GCODE = GCODE + "G0 X" + str(round(POLYLINEX[i][1], R)) + "\n"
        GCODE = GCODE + "G0 Y" + str(round(POLYLINEY[i][1], R)) + "\n"
        GCODE = GCODE + "G1 Z" + CUTDEPTH + " F" + DRILLRATE + "\n"
        FEEDFLAG = 0
        for j in range(2, POLYLINEQTY[i]):
            GCODE = GCODE + "G1 X" + str(round(POLYLINEX[i][j], R)) + " Y" + str(round(POLYLINEY[i][j], R))
            if FEEDFLAG == 0:
                GCODE = GCODE + " F" + FEEDRATE
                FEEDFLAG = 1
            # End if
            GCODE = GCODE + "\n"
        # Next j
        if POLYOPEN[i] == 1:
            GCODE = GCODE + "G1 X" + str(round(POLYLINEX[i][1], R)) + " Y" + str(round(POLYLINEY[i][1], R)) + "\n"
        # End if
        GCODE = GCODE + "G0 Z" + SKIMHEIGHT + "\n"
# Next i
GCODE = GCODE + "G0 Z" + safe_height + "\n"  # Rapid up to safe height


# Engrave Lines #
GCODE = GCODE + "(MACHINE LINES)\n"  # Remark
for i in range(1, LINECOUNT):
    if LINELAYER[i] == "CUT":
        LINEPOST = LINEPOST + 1
        # Line start different to last line finish point. Rapid then feed down.
        if XSTART[i] != XEND[i - 1] or YSTART[i] != YEND[i - 1]:
            GCODE = GCODE + "G0 Z" + SKIMHEIGHT + "\n"
            GCODE = GCODE + "(LINE " + str(LINEPOST) + ")\n"
            # GCODE = GCODE + "G0"
            # if ( XSTART[i] != XEND[i] ): GCODE = GCODE + " X" + str(round(XSTART[i],R))
            # if ( YSTART[i] != YEND[i] ): GCODE = GCODE + " Y" + str(round(YSTART[i],R))
            # GCODE = GCODE + "\n"
            GCODE = GCODE + "G0 X" + str(round(XSTART[i], R)) + "\n"
            GCODE = GCODE + "G0 Y" + str(round(YSTART[i], R)) + "\n"
            GCODE = GCODE + "G0 Z" + STARTHEIGHT + "\n"
            GCODE = GCODE + "G1 Z" + CUTDEPTH + " F" + DRILLRATE + "\n"
            FEEDFLAG = 0
        # End if
        # Machine to line end point
        # GCODE = GCODE + "G1"
        # if ( XSTART[i] != XEND[i] ): GCODE = GCODE + " X" + str(round(XEND[i],R))
        # if ( YSTART[i] != YEND[i] ): GCODE = GCODE + " Y" + str(round(YEND[i],R))
        GCODE = GCODE + "G1 X" + str(round(XEND[i], R)) + " Y" + str(round(YEND[i], R))
        if FEEDFLAG == 0:
            GCODE = GCODE + " F" + FEEDRATE
            FEEDFLAG = 1
        # End if
        GCODE = GCODE + "\n"
# NEXT i
GCODE = GCODE + "G0 Z" + safe_height + "\n"  # Rapid up to safe height
if ZEROFLAG:
    GCODE = GCODE + ZEROCHECK


# Drill Holes #
GCODE = GCODE + "(DRILL HOLES)\n"  # Remark
for i in range(1, HOLECOUNT):
    # print "Circle X centre", XHOLE[i], " Y centre", YHOLE[i] , " Radius" , RADIUS[i]
    if RADIUS[i] < CIRCLERAD:
        COUNT = COUNT + 1
        GCODE = GCODE + "(HOLE " + str(COUNT) + ")\n"
        GCODE = GCODE + "G0 X" + str(round(XHOLE[i], R)) + "\n"
        GCODE = GCODE + "G0 Y" + str(round(YHOLE[i], R)) + "\n"
        GCODE = GCODE + "G0 Z" + STARTHEIGHT + "\n"
        GCODE = GCODE + "G1 Z" + DRILLDEPTH + " F" + DRILLRATE + "\n"
        GCODE = GCODE + "G0 Z" + SKIMHEIGHT + "\n"
# NEXT i
GCODE = GCODE + "G0 Z" + safe_height + "\n"  # Rapid up to safe height


# Cut polilines through ( Layer = THROUGH ) #
GCODE = GCODE + "(CUT THROUGH POLYLINES)\n"  # Remark
GCODE = GCODE + "G0 Z" + SKIMHEIGHT + "\n"
PASSCOUNT = 0
for D in range(TSTEP, TCUTDEPTH + TSTEP, TSTEP):
    PASSCOUNT = PASSCOUNT + 1
    THROUGHPOST = 0
    for i in range(1, POLYCOUNT + 1):
        if POLYLAYER[i] == "THROUGH":
            THROUGHPOST = THROUGHPOST + 1
            GCODE = GCODE + "(POLYLINE " + str(THROUGHPOST) + "  PASS " + str(PASSCOUNT) + ")\n"
            GCODE = GCODE + "G0 X" + str(round(POLYLINEX[i][1], R)) + "\n"
            GCODE = GCODE + "G0 Y" + str(round(POLYLINEY[i][1], R)) + "\n"
            GCODE = GCODE + "G1 Z" + str(D) + " F" + DRILLRATE + "\n"
            FEEDFLAG = 0
            for j in range(2, POLYLINEQTY[i]):
                GCODE = GCODE + "G1 X" + str(round(POLYLINEX[i][j], R)) + " Y" + str(round(POLYLINEY[i][j], R))
                if FEEDFLAG == 0:
                    GCODE = GCODE + " F" + TFEEDRATE
                    FEEDFLAG = 1
                # End if
                GCODE = GCODE + "\n"
            # Next j
            if POLYOPEN[i] == 1:
                GCODE = GCODE + "G1 X" + str(round(POLYLINEX[i][1], R)) + " Y" + str(round(POLYLINEY[i][1], R)) + "\n"
            # End if
            GCODE = GCODE + "G0 Z" + SKIMHEIGHT + "\n"
    # Next i
    GCODE = GCODE + "G0 Z" + safe_height + "\n"  # Rapid up to safe height


# Finish and go home #
GCODE = GCODE + "G0 Z" + safe_height + "\n"  # Rapid up to safe height
if ZEROFLAG:
    GCODE = GCODE + ZEROCHECK
GCODE = GCODE + "M5\n"  # Spindle motor off
GCODE = GCODE + "G0 X0\n" + "Y0\n"  # Go home rapid
GCODE = GCODE + FINISHPOS


# Display findings and G-Code #
print(GCODE)
print("Lines Found     ", LINECOUNT - 1)
print("Polylines Found ", POLYCOUNT)
print("Circles Found   ", HOLECOUNT - 1)
print("Circles bigger than R" + str(CIRCLERAD) + " found ", BIGCOUNT)
print("Polylines posted =", POLYPOST)
print("Lines     posted =", LINEPOST)
print("Holes     posted =", COUNT)
print("Through   posted =", THROUGHPOST, "   Using", PASSCOUNT, "Passes")
print("X Min ", XMIN)
print("X Max ", XMAX)
print("Y Min ", YMIN)
print("Y Max ", YMAX)

if ERROR != "":
    print(ERROR)


# Save to text file #
FILE = open(save_file, "w")
FILE.write(GCODE)
FILE.close()
print("G-Code written to file > ", save_file)
