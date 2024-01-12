"""
    This module validates if there is free space in the MDF.
"""
import rpack


sizes = [(58, 206), (231, 176), (35, 113), (46, 109)]


def available_space_in_mdf():

    positions = rpack.pack(sizes)
    print(positions)
    available_space = True

    return available_space


if __name__ == '__main__':
    available_space_in_mdf()