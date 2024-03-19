; LightBurn 1.3.01
; GRBL device profile, absolute coords
; Bounds: X0 Y0 to X800 Y0
G00 G17 G40 G21 G54
G90
M4
; Cut @ 600 mm/min, 95% power
M8
G0 X0Y0
; Layer Corte Pass 1 of 10
G1 X800S950F600
; Layer Corte Pass 2 of 10
G1 X0
; Layer Corte Pass 3 of 10
G1 X800
; Layer Corte Pass 4 of 10
G1 X0
; Layer Corte Pass 5 of 10
G1 X800
; Layer Corte Pass 6 of 10
G1 X0
; Layer Corte Pass 7 of 10
G1 X800
; Layer Corte Pass 8 of 10
G1 X0
; Layer Corte Pass 9 of 10
G1 X800
; Layer Corte Pass 10 of 10
G1 X0
M9
G1 S0
M5
G90
M2
