

def draw_g_code(file_g_code_name):
    """
    G-code commands to cut a product in the laser machine.

    :return: list with g-code draw
    """

    # with open(file_g_code_name, 'r') as g_code:
    #    data = g_code.readline()

    data_split = open(file_g_code_name, 'r')

    # data_split = data  # .split(b'\n')
    # data_split = data.replace(b'M3 S255;', b'M4 S1000;').replace(b'\n', b'').split(b';')
    # data_split.remove(b'G90')

    # while data_split[0] == b'M5':
    #     data_split.pop(0)

    # if data_split[-1] == b'':
    #     data_split.pop(-1)

    # if data_split[-1] == b'M5':
    #     data_split.pop(-1)

    # first_point = data_split[0]
    # data_split.pop(0)

    first_point = None
    command_list = data_split

    return first_point, command_list
