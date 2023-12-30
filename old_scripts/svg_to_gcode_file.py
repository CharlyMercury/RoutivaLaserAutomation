from svg_to_gcode.svg_parser import parse_file
from svg_to_gcode.compiler import Compiler, interfaces


def svg_file_to_g_code(path_to_file, output_dir):

    # Instantiate a compiler, specifying the interface type and the speed at which the tool should move.
    # pass_depth controls
    # how far down the tool moves after every pass. Set it to 0 if your machine does not support Z axis movement.
    gcode_compiler = Compiler(interfaces.Gcode, movement_speed=8000, cutting_speed=600, pass_depth=0)

    curves = parse_file(path_to_file)  # Parse a svg file into geometric curves

    gcode_compiler.append_curves(curves)
    gcode_compiler.compile_to_file(output_dir, passes=1)
