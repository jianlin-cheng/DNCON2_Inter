import copy
import os
import sys
import math

from classes.pdb_lines import pdb_lines


def get_name(file):
    return file.split("/")[-1][0:4]


def read_pdb(pdb):
    contents = []
    with open(pdb, "r") as f:
        for line in f:
            # if (line.startswith("ATOM")):
            #    pass
            contents.append(line)
    return contents


def split_line_to_tuple(line):
    a_pdb_line = pdb_lines()

    a_pdb_line.atom = line[0:6].strip()
    a_pdb_line.serial = line[6:12].strip()
    a_pdb_line.atom_name = line[12:16].strip()
    a_pdb_line.alt_loc = line[16].strip()
    a_pdb_line.res_name = line[17:20].strip()
    a_pdb_line.chain = line[20:22].strip()
    a_pdb_line.res_num = line[22:26].strip()
    a_pdb_line.icode = line[26:30].strip()
    a_pdb_line.x = line[30:38].strip()
    a_pdb_line.y = line[38:46].strip()
    a_pdb_line.z = line[46:54].strip()
    a_pdb_line.occupancy = line[54:60].strip()
    # a_pdb_line.temp_fact = line[60:76].strip()
    a_pdb_line.temp_fact = line[60:66].strip()
    a_pdb_line.element = line[76:78].strip()
    a_pdb_line.charge = line[78:80].strip()

    return a_pdb_line


def contents_to_info(contents):  # reads the ATOM line. Then splits the info into respective frames and returns the data
    split_contents = []
    for lines in contents:
        if lines.startswith("ATOM"):
            pdb_line = split_line_to_tuple(lines.strip())
            split_contents.append(pdb_line)
    return split_contents


def add_chain(pdb, val):
    for pdb_line in pdb:
        pdb_line.chain = str(val)
    return pdb


def remove_chain(pdb):
    for pdb_line in pdb:
        pdb_line.chain = ''
    return pdb


def write2File(_filename, _cont):
    with open(_filename, "w") as f:
        f.writelines(_cont)
        if _cont[len(_cont) - 1].strip() != "END":
            f.write("END")
    return


def separate_by_chain(_pdb, _name):
    print(_pdb)
    result = list(filter(lambda x: (x.chain == _name), _pdb))
    return result


def correct_format(_pdb_row):
    _pdb_copy = copy.deepcopy(_pdb_row)
    # https://www.cgl.ucsf.edu/chimera/docs/UsersGuide/tutorials/pdbintro.html
    _pdb_copy.atom = _pdb_copy.atom  # 1-4
    _pdb_copy.serial = space_returner(4 - len(str(_pdb_copy.serial))) + _pdb_copy.serial  # 7-11
    _pdb_copy.atom_name = _pdb_copy.atom_name + space_returner(3 - len(_pdb_copy.atom_name))  # 13-16
    _pdb_copy.alt_loc = space_returner(1 - len(_pdb_copy.alt_loc)) + _pdb_copy.alt_loc  # 17
    _pdb_copy.res_name = space_returner(3 - len(_pdb_copy.res_name)) + _pdb_copy.res_name  # 18-20
    _pdb_copy.chain = space_returner(1 - len(_pdb_copy.chain)) + _pdb_copy.chain  # 22
    _pdb_copy.res_num = space_returner(4 - len(_pdb_copy.res_num)) + _pdb_copy.res_num  # 23-26
    _pdb_copy.icode = space_returner(2 - len(_pdb_copy.chain)) + _pdb_copy.icode  # 27
    _pdb_copy.x = space_returner(8 - len(_pdb_copy.x)) + _pdb_copy.x  # 31-38
    _pdb_copy.y = space_returner(8 - len(_pdb_copy.y)) + _pdb_copy.y  # 39-46
    _pdb_copy.z = space_returner(8 - len(_pdb_copy.z)) + _pdb_copy.z  # 47-54
    _pdb_copy.occupancy = space_returner(6 - len(_pdb_copy.occupancy)) + _pdb_copy.occupancy  # 55-60
    _pdb_copy.temp_fact = space_returner(6 - len(_pdb_copy.temp_fact)) + _pdb_copy.temp_fact  # 61-66
    _pdb_copy.element = space_returner(4 - len(_pdb_copy.element)) + _pdb_copy.element  # 73-76
    _pdb_copy.charge = space_returner(2 - len(_pdb_copy.charge)) + _pdb_copy.charge  # 77-78
    content = _pdb_copy.atom + space_returner(3) + _pdb_copy.serial + space_returner(
        2) + _pdb_copy.atom_name + _pdb_copy.alt_loc + _pdb_copy.res_name + space_returner(
        1) + _pdb_copy.chain + _pdb_copy.res_num + _pdb_copy.icode + space_returner(
        3) + _pdb_copy.x + _pdb_copy.y + _pdb_copy.z + _pdb_copy.occupancy + _pdb_copy.temp_fact + space_returner(
        8) + _pdb_copy.element + _pdb_copy.charge
    return content


def space_returner(_input):
    i = 0
    space = ""
    while i < _input:
        space = space + " "
        i = i + 1
    return space


def convert_to_pdb(_pdb,_name):
    content = ''
    for x in _pdb:
        content += correct_format(x) + '\n'
    f = open(_name, "w")
    f.write(content)
    f.close()
    return _pdb


# cns format

def convert_to_cns_format(_pdb_row):
    _pdb_copy = copy.deepcopy(_pdb_row)
    # https://www.cgl.ucsf.edu/chimera/docs/UsersGuide/tutorials/pdbintro.html
    _pdb_copy.atom = _pdb_copy.atom  # 1-4
    _pdb_copy.serial = space_returner(4 - len(str(_pdb_copy.serial))) + str(_pdb_copy.serial)  # 7-11
    _pdb_copy.atom_name = _pdb_copy.atom_name + space_returner(3 - len(_pdb_copy.atom_name))  # 13-16
    _pdb_copy.alt_loc = space_returner(1 - len(_pdb_copy.alt_loc)) + _pdb_copy.alt_loc  # 17
    _pdb_copy.res_name = space_returner(3 - len(_pdb_copy.res_name)) + _pdb_copy.res_name  # 18-20
    _pdb_copy.chain = space_returner(1 - len(_pdb_copy.chain)) + _pdb_copy.chain  # 22
    _pdb_copy.res_num = space_returner(4 - len(_pdb_copy.res_num)) + _pdb_copy.res_num  # 23-26
    _pdb_copy.icode = space_returner(2 - len(_pdb_copy.chain)) + _pdb_copy.icode  # 27
    _pdb_copy.x = space_returner(8 - len(_pdb_copy.x)) + _pdb_copy.x  # 31-38
    _pdb_copy.y = space_returner(8 - len(_pdb_copy.y)) + _pdb_copy.y  # 39-46
    _pdb_copy.z = space_returner(8 - len(_pdb_copy.z)) + _pdb_copy.z  # 47-54
    _pdb_copy.occupancy = space_returner(6 - len(_pdb_copy.occupancy)) + _pdb_copy.occupancy  # 55-60
    _pdb_copy.temp_fact = space_returner(6 - len(_pdb_copy.temp_fact)) + _pdb_copy.temp_fact  # 61-66
    _pdb_copy.element = _pdb_copy.chain  # 73-76
    _pdb_copy.charge = space_returner(2 - len(_pdb_copy.charge)) + _pdb_copy.charge  # 77-78
    content = _pdb_copy.atom + space_returner(3) + _pdb_copy.serial + space_returner(
        2) + _pdb_copy.atom_name + _pdb_copy.alt_loc + _pdb_copy.res_name + space_returner(
        1) + _pdb_copy.chain + _pdb_copy.res_num + _pdb_copy.icode + space_returner(
        3) + _pdb_copy.x + _pdb_copy.y + _pdb_copy.z + _pdb_copy.occupancy + _pdb_copy.temp_fact + space_returner(
        6) + _pdb_copy.element
    return content


def convert_to_cns(_pdb, _filename):
    # file is outputted
    array = []
    content = ''
    for x in _pdb:
        val = convert_to_cns_format(x)
        array.append(val)
        content = content + val + '\n'
    f = open(_filename, "w")
    f.write(content + 'END')
    f.close()
    return array


def fix_serial(_array, _no=1):
    number = _no
    for x in _array:
        x.serial = number
        number = number + 1
    return _array


def write_to_pdb(_pdb, _file_name):
    content = ''
    for x in _pdb:
        content = content + x + '\n'
    f = open(_file_name, "w")
    f.write(content)
    f.close()
    return _pdb


def if_contains_chain(_pdb):
    for atom in _pdb:
        if len(atom.chain.strip()) > 0:
            return True
        else:
            return False


def file_array_return(_input_dir):
    output_array = []
    true_distance_file = open(_input_dir, "r")

    if true_distance_file.mode == 'r':
        output_array = true_distance_file.read()
        true_distance_file.close()
    return output_array


def pdb_array_sender(_pdb_file):
    file_content_array = []
    for y in file_array_return(_pdb_file).split("\n"):
        temp_array = []
        if y.split(' ')[0] != 'REMARK':
            for x in y.split(" "):
                if len(x.strip()) > 0 and x != "ATOM" and x != "\nATOM" and x != "END":
                    temp_array.append(x)

            file_content_array.append(temp_array)
    return file_content_array


def calc_distance(x1, y1, z1, x2, y2, z2):
    return math.sqrt((round(x1, 11) - (round(x2, 11))) ** 2 +
                     (round(y1, 11) - (round(y2, 11)) ** 2) +
                     (round(z1, 11) - (round(z2, 11))) ** 2)


def coordinate_finder(_pdb_a, _num):
    for val in _pdb_a:
        # cb ,resid,distance ,i
        if float(val[4]) == float(_num):
            return val[5], val[6], val[7]


def dist_file_reader(_dist_file):
    file_content_array = []
    for y in file_array_return(_dist_file).split("\n"):
        temp_array = []
        if len(y.split(' ')) == 5:
            temp_array.append(y.split(' '))

            file_content_array.append(temp_array)
    return file_content_array


def average_translation_finder(_model, _docked, _dist_file):
    _model = '/home/rajroy/Documents/Ongoing/1hlc_given/1HLC_b_cns_atomId.pdb'
    _docked = '/home/rajroy/Documents/Ongoing/1hlc_given/docking_picked.pdb'
    _dist_file = '/home/rajroy/Documents/Ongoing/1hlc_given/1HLC_dist_AB.txt'

    if not os.path.isfile(_docked):
        print(_docked, " does not exist.")
        sys.exit(1)

    if not os.path.isfile(_model):
        print(_model, " does not exist.")
        sys.exit(1)

    pdb_a = pdb_array_sender(_docked)

    pdb_b = pdb_array_sender(_model)

    dist_file = dist_file_reader(_dist_file)

    # look at 5 for resisdue and  678 and are corodioantes
    avg_x, avg_y, avg_z = 0, 0, 0

    for val in dist_file:
        x1, y1, z1 = coordinate_finder(pdb_a, val[0][1])
        x2, y2, z2 = coordinate_finder(pdb_b, val[0][1])
        avg_x = float(avg_x) + float(x2) - float(x1)
        avg_z = float(avg_z) + float(z2) - float(z1)
        avg_y = float(avg_y) + float(y2) - float(y1)
    print(avg_x / len(dist_file), avg_y / len(dist_file), avg_z / len(dist_file))


def average_translation_finder_modified(_model, _docked, _dist_file):
    dist_file = dist_file_reader(_dist_file)
    # look at 5 for resisdue and  678 and are corodioantes
    sum_x, sum_y, sum_z = 0, 0, 0
    # differenc between changed  docked - model   which will be added
    for val in dist_file:
        iniital = list(
            filter(lambda x: (x.res_num == val[0][1] and x.atom_name == ('CB' or 'CA' or 'C') and x.chain == 'B'),
                   copy.deepcopy(_model)))
        final = list(
            filter(lambda x: (x.res_num == val[0][1] and x.atom_name == ('CB' or 'CA' or 'C') and x.chain == 'B'),
                   copy.deepcopy(_docked)))  # CB priority then CA then C

        sum_x = float(sum_x) + float(final[0].x) - float(iniital[0].x)
        sum_y = float(sum_y) + float(final[0].y) - float(iniital[0].y)
        sum_z = float(sum_z) + float(final[0].z) - float(iniital[0].z)
    print(sum_x / len(dist_file), sum_y / len(dist_file), sum_z / len(dist_file))
    return sum_x / len(dist_file), sum_y / len(dist_file), sum_z / len(dist_file)


def docking_details_returner(_file_list, _output_file):
    details_array_all = []
    for x in _file_list:
        f = open(x, "r")
        if f.mode == 'r':
            contents = f.read()
            f.close()
        details_array = []
        for item in contents.split("\n"):
            if "Etotal=" in item:
                e_total = item.strip().split("=")[1].strip().split(" ")[0]
                details_array.append(x)
                details_array.append(float(e_total))
            if "Enoe=" in item:
                e_noe = item.strip().split("=")[2].strip().split(" ")[0]
                details_array.append(float(e_noe))
            if "rmsd bonds==" in item:
                rmsd_bonds = item.strip().split("=")[1].strip().split(" ")[0]
                details_array.append(float(rmsd_bonds))
            if "rmsd angles=" in item:
                rmsd_angles = item.strip().split("=")[2].strip().split(" ")[0]
                details_array.append(float(rmsd_angles))
                details_array_all.append(details_array)
                break
    return details_array_all


def translator(_model, _segment, _x, _y, _z):
    for val in _model:
        if val.chain.strip() == _segment :
            val.x = format(float(val.x) + float(_x),'.3f')
            val.y = format( float(val.y) + float(_y),'.3f')
            val.z =  format(float(val.z) + float(_z),'.3f')
    return _model
