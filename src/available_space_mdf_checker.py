"""
    This module validates if there is free space in the MDF.
"""
import json
import rpack


def available_space_in_mdf(gcode_path):
    height, width = read_gcode_parameters(gcode_path)
    rectangle_data = {gcode_path: [height, width]}

    sizes = sizes_of_rectangles_a_new_rectangle(rectangle_data)
    positions = []
    counter = 2

    heights = set([element[1] for element in sizes])
    partial_height = min(heights)

    while True:
        try:
            positions = rpack.pack(sizes, max_width=800, max_height=partial_height)  # (anchura, altura)
            break
        except Exception as err:
            heights = set([element[1] for element in sizes])
            if len(heights) == 1:
                partial_height = min(heights) * counter
                counter += 1
                print(partial_height)
            print(f'An error has occurred: {err}')

    positions_cp = calculate_new_position_with_new_positions(positions)
    print(positions_cp)


def sizes_of_rectangles_a_new_rectangle(rectangle_data: dict) -> list:
    sizes = []

    with open('src/rectangles.json', 'r') as rectangles:
        data = json.load(rectangles)
        data.append(rectangle_data)

    with open('src/rectangles.json', 'w') as rectangles:
        json.dump(data, rectangles, indent=2)

    for element in data:
        height_and_width = tuple(element[list(element.keys())[0]])
        sizes.append(height_and_width)  # sizes[ (height, width) ]

    return sizes


def calculate_new_position_with_new_positions(positions_cp: list) -> list:
    positions_to_bd = []

    with open('src/assigned_positions.json', 'r+') as assigned_positions_prev:
        old_assigned_positions = json.load(assigned_positions_prev)

    for element_old in old_assigned_positions:
        if tuple(element_old['assigned_position']) in positions_cp:
            positions_cp.remove(tuple(element_old['assigned_position']))

    for element in old_assigned_positions:
        height_and_width = {'assigned_position': element['assigned_position']}
        positions_to_bd.append(height_and_width)
    positions_to_bd.append({'assigned_position': positions_cp[0]})

    with open('src/assigned_positions.json', 'w') as assigned_positions_:
        json.dump(positions_to_bd, assigned_positions_, indent=2)

    return positions_cp


def read_gcode_parameters(gcode_path):
    """
        This function extracts the parameters of the gcode. For example
        weight and height of the design.
    """

    g_code_data = open(gcode_path, 'r')

    for g_code_command in g_code_data:

        if 'Bounds: X0 Y0 to' in g_code_command:
            height_and_width = g_code_command.split('Bounds: X0 Y0 to')[1].strip().split(' ')
            height = int(height_and_width[0].replace('X', ''))  # Anchura
            width = int(height_and_width[1].replace('Y', ''))  # Altura
            return height, width


if __name__ == '__main__':
    new_file = 'example_3_cajita_6_6'
    gcode_path_ = f"examples/{new_file}.gcode"
    available_space_in_mdf(gcode_path_)
