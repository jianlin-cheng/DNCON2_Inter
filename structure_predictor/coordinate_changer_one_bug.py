import os.path
import sys

from pdb_libs import pdb_reader
import copy

pdb_files = rr_files = sys.argv[1]
output_dir =  sys.argv[2]


def translate_new(x, y, z, input):
    for val in input:
        if val:
            val.x = format(float(val.x) + x, '.3f')
            val.y = format(float(val.y) + y, '.3f')
            val.z = format(float(val.z) + z, '.3f')
    return input


class pdb_lines:
    atom = ''
    serial = ''
    atom_name = ''
    alt_loc = ''
    res_name = ''
    chain = ''
    res_num = ''
    icode = ''
    x = ''
    y = ''
    z = ''
    occupancy = ''
    temp_fact = ''
    element = ''
    charge = ''

    pass


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
def pdb_from_array(_pdb, _filename):
    array = []
    content = ''
    for x in _pdb:
        val = string_array_from_pdb_array(x)
        array.append(val)
        content = content + val + '\n'
    f = open(_filename, "w")
    f.write(content + 'END')
    f.close()
    return array

def space_returner(_input):
    i = 0
    space = ""
    while i < _input:
        space = space + " "
        i = i + 1
    return space



def string_array_from_pdb_array(_pdb_row):
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
    _pdb_copy.element = space_returner(4-len(  _pdb_copy.element ))+  _pdb_copy.element   # 73-76
    _pdb_copy.charge = space_returner(2 - len(_pdb_copy.charge)) + _pdb_copy.charge  # 77-78
    content = _pdb_copy.atom + space_returner(3) + _pdb_copy.serial + space_returner(
        2) + _pdb_copy.atom_name + _pdb_copy.alt_loc + _pdb_copy.res_name + space_returner(
        1) + _pdb_copy.chain + _pdb_copy.res_num + _pdb_copy.icode + space_returner(
        3) + _pdb_copy.x + _pdb_copy.y + _pdb_copy.z + _pdb_copy.occupancy + _pdb_copy.temp_fact + space_returner(
        6) + _pdb_copy.element
    return content
def contents_to_info(contents):  # reads the ATOM line. Then splits the info into respective frames and returns the data
    split_contents = []
    for lines in contents:
        if lines.startswith("ATOM"):
            pdb_line = split_line_to_tuple(lines.strip())
            split_contents.append(pdb_line)
    return split_contents


if not os.path.exists(output_dir):
    os.system("mkdir -p " + output_dir + '\n')

if not os.path.exists(pdb_files):
    print("Failed to find " + pdb_files + '\n')
    exit()

name = os.path.basename(pdb_files).split(".")[0]
model_a_loc = output_dir + '/' + name + '_A.pdb'
os.system('cp ' + pdb_files + ' ' + model_a_loc)
print(' original final copied to ' + model_a_loc)

x_translate = 100
y_translate = 100
z_translate = 100

file_content_array = []
model = contents_to_info(pdb_reader.read_pdb(pdb_files))
translated_array = translate_new(x_translate, y_translate, z_translate, copy.deepcopy(model))

name = output_dir + '/' + name + '_B.pdb'

pdb_from_array(translated_array, name)

print(' Translated complete and file copied to ' + name)