import copy
import config
# import pdb_libs.file_handler as file_handler

import time
import glob, os
import sys
sys.path.append("./pdb_libs/")
from pdb_libs import file_handler, pdb_reader
# ATOM      1  N   GLU     1      25.947  23.974  55.339  1.00 37.85           N  :format input


#
# _output_file = '/home/rajroy/Documents/Qurantine/Experiment_100_new/'
# _input_model_a = '/home/rajroy/Downloads/input-1/test/1I88A.pdb'
# _input_model_b = '/home/rajroy/Downloads/input-1/test/1I88B.pdb'
# _input_dist_file = '/home/rajroy/Downloads/input-1/test_rr/1I88_AB.rr'

_input_model_a = sys.argv[1]
_input_model_b = sys.argv[2]
_input_dist_file = sys.argv[3]
_output_file = sys.argv[4]

_model_count = config.MODEL_COUNT

if not os.path.exists(_input_model_a):
    print('Not found' + str(_input_model_a) + '\n')
    exit()
else:
    print(_input_model_a + '\n')

if not os.path.exists(_input_model_b):
    print('Not found' + str(_input_model_a) + '\n')
    exit()
else:
    print(_input_model_b + '\n')

if not os.path.exists(_input_dist_file):
    print('Not found' + str(_input_dist_file) + '\n')
    exit()
else:
    print(_input_dist_file + '\n')

if not os.path.exists(_output_file):
    os.system("mkdir -p " + _output_file + '\n')
else:
    print(_output_file + '\n')

cns_dir = config.CNS_DIRECTORY

input_dir_name = _output_file + '/input'
print('Creating input folder \n')
os.system("mkdir -p " + input_dir_name + '\n')

# Clean_pdb
# Read check chain insert chain
# Separate based on segment (we will given seperate pdb) its not necessary
# Insert chain

model_a = pdb_reader.contents_to_info(pdb_reader.read_pdb(_input_model_a))
if not pdb_reader.if_contains_chain(model_a):
    model_a = pdb_reader.add_chain(model_a, 'A')
print('chain A inserted \n')

model_b = pdb_reader.contents_to_info(pdb_reader.read_pdb(_input_model_b))
if not pdb_reader.if_contains_chain(model_b):
    model_b = pdb_reader.add_chain(model_b, 'B')
print('chain B inserted  \n')

# convert to cns form (further)
# mkdir initialzaion
initialization_dir = _output_file + 'initialization/'
os.system("mkdir -p " + initialization_dir)
restrains_file_name = initialization_dir + 'res.restraints'
file_handler.convert_dist_to_restrain(_input_dir=_input_dist_file, _segment_1='A', _segment_2='B',
                                      _output_dir=restrains_file_name)
print('restrain file created  \n')
# fix atom no
merge_cns_b = pdb_reader.fix_serial(model_b, len(model_a) + 1)
# merge the file
merged_pdb = model_a + merge_cns_b
merged_pdb_name = _output_file + str('cns_format.pdb')
merged_pdb_cns = pdb_reader.convert_to_cns(merged_pdb, merged_pdb_name)
print('file merged  \n')
# choose a fixed pdb
# generate docking.inp file
docking_dir = _output_file + '/docking/'
print('Initializing docking  \n')
os.system('mkdir -p ' + docking_dir)
file_handler.docking_inp(_input_pdb=merged_pdb_name, _fixed_chain='A', _fixed_moving_chain='B',
                         _restrain_file=restrains_file_name, _output_dir=docking_dir, _model_count=_model_count)

# number can be very few adjust it and addd the change things
file_handler.job_docking(cns_dir, docking_dir)
os.system('chmod +x ' + docking_dir + '/job_docking.sh')
# run the file
os.chdir(docking_dir)
start = time.time()
print('submitting job  \n')
process_state = os.system('./job_docking.sh')
print(process_state)
# select low scoring file
break_val = False

done = time.time()
elapsed = done - start
print(' time elapsed ' + str(elapsed) + '\n')

# read_file and get value and  keep the track

os.chdir(docking_dir)
file_list = []
for file in glob.glob("docking_*.pdb"):
    if not "start" in file:
        file_list.append(docking_dir + "/" + file)

details_array_all = pdb_reader.docking_details_returner(file_list, docking_dir)

details_array_all = sorted(details_array_all, key=lambda energy: energy[1])
# docked_pdb = pdb_reader.contents_to_info(pdb_reader.read_pdb(copy.deepcopy(details_array_all[0][0])))
print(details_array_all[0][0])
os.system('cp ' + details_array_all[0][0] + ' ' + _output_file + '/initialized.pdb')
