import os
import sys
import Bio, math
import numpy as np

input_dir = '/home/rajroy/Downloads/input/atom/2F7SB.pdb'


def space_returner(_input):
    i = 0
    space = ""
    while i < _input:
        space = space + " "
        i = i + 1
    return space


def file_array_return(_input_dir):
    output_array = []
    true_distance_file = open(_input_dir, "r")

    if true_distance_file.mode == 'r':
        output_array = true_distance_file.read()
        true_distance_file.close()
    return output_array


def write_pdb_from_array(_array, _name):
    name_of_file = input_dir.split('/')
    dir_str = "/"
    i = 0
    while len(name_of_file) - 1 > i:
        dir_str = dir_str + name_of_file[i] + "/"
        i = i + 1
    name_of_output_file = dir_str + name_of_file[len(name_of_file) - 1]
    name_of_output_file = name_of_output_file[0:len(name_of_output_file) - 4] + '_' + str(_name) + ".pdb"
    print(name_of_output_file)
    f = open(name_of_output_file, "w")
    content = ""
    val = 0
    for values in _array:
        # if int(values[0])  > 2563:
        #     print(values)
        if len(values) > 0:

            content = "ATOM" + space_returner(7 - len(str(values[0]))) + str(values[0]) + "  " + str(
                values[1]) + space_returner(4 - len(str(values[1]))) + str(values[2]) + space_returner(
                6 - len(values[3])) + str(
                values[3]) + space_returner(12 - len(str(values[4]))) + str(values[4]) + space_returner(
                8 - len(str(values[5]))) + str(
                values[5]) + space_returner(8 - len(str(values[6]))) + str(values[6]) + "  " + str(
                values[7]) + space_returner(6 - len(str(values[8]))) + str(values[8]) + "           " + str(values[9])
            f.write(content + "\n")
        val = val + 1
    f.write("END")
    f.close()


def translate(x, y, z, input):
    counter = 0
    for val in input:
        if len(val) > 0:
            val[4] = format(float(val[4]) + x, '.3f')
            val[5] = format(float(val[5]) + y, '.3f')
            val[6] = format(float(val[6]) + z, '.3f')
            counter = counter + 1
    return input


# https://en.wikipedia.org/wiki/Rotation_matrix
def rotation_x(_degree, _input):
    x_matrix = [[1, 0, 0], [0, math.cos(_degree), -math.sin(_degree)], [0, math.sin(_degree), math.cos(_degree)]]

    for val in _input:
        if len(val) > 0:
            x = float(val[4])
            y = float(val[5])
            z = float(val[6])
            values = [[x], [y], [z]]
            new_values = np.dot(x_matrix, values)
            val[4] = format(float(new_values[0]), '.3f')
            val[5] = format(float(new_values[1]), '.3f')
            val[6] = format(float(new_values[2]), '.3f')

    return _input


def rotation_y(_degree, _input):
    y_matrix = [[math.cos(_degree), 0, math.sin(_degree)], [0, 1, 0], [-math.sin(_degree), 0, math.cos(_degree)]]

    for val in _input:
        if len(val) > 0:
            x = float(val[4])
            y = float(val[5])
            z = float(val[6])
            values = [[x], [y], [z]]
            new_values = np.dot(y_matrix, values)
            val[4] = format(float(new_values[0]), '.3f')
            val[5] = format(float(new_values[1]), '.3f')
            val[6] = format(float(new_values[2]), '.3f')

    return _input


def rotation_z(_degree, _input):
    y_matrix = [[math.cos(_degree), -math.sin(_degree), 0], [math.sin(_degree), math.cos(_degree), 0], [0, 0, 1]]

    for val in _input:
        if len(val) > 0:
            x = float(val[4])
            y = float(val[5])
            z = float(val[6])
            values = [[x], [y], [z]]
            new_values = np.dot(y_matrix, values)
            val[4] = format(float(new_values[0]), '.3f')
            val[5] = format(float(new_values[1]), '.3f')
            val[6] = format(float(new_values[2]), '.3f')

    return _input


if not os.path.isfile(input_dir):
    print(input_dir, " does not exist.")
    sys.exit(1)

file_content_array = []
for y in file_array_return(input_dir).split("\n"):
    temp_array = []
    for x in y.split(" "):

        if len(x) > 0 and x != "ATOM" and x != "\nATOM" and x != "END":
            temp_array.append(x)

    file_content_array.append(temp_array)

translated_array = translate(-90.00, -100.00, -155.00, file_content_array)
data = rotation_z(90, translated_array)
print(data)
# print(translated_array)
write_pdb_from_array(data, 'rotation_trans_z_' + str(-135))
