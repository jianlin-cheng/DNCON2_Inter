import copy
import pdb_libs.file_handler as file_handler
import time
import glob, os

# ATOM      1  N   GLU     1      25.947  23.974  55.339  1.00 37.85           N  :format input
from pdb_libs import pdb_reader, pdb_reader

_output_file = '/home/rajroy/Documents/Qurantine/Experiment_1/'
_input_model_a = '//home/rajroy/Documents/Qurantine/Experiment_1/1HLCA.pdb'
_input_model_b = '//home/rajroy/Documents/Qurantine/Experiment_1/1HLCB_t.pdb'
_input_dist_file = '/home/rajroy/Documents/Qurantine/1HLC_dist_AB.txt'
cns_dir = '/home/rajroy/cns/cns_solve_1.3/'
_model_count = 10
# Clean_pdb
# Read check chain insert chain
# Separate based on segment (we will given seperate pdb) its not necessary
# Insert chain
model_a = pdb_reader.contents_to_info(pdb_reader.read_pdb(_input_model_a))
if not pdb_reader.if_contains_chain(model_a):
    model_a = pdb_reader.add_chain(model_a, 'A')

model_b = pdb_reader.contents_to_info(pdb_reader.read_pdb(_input_model_b))
if not pdb_reader.if_contains_chain(model_b):
    model_b = pdb_reader.add_chain(model_b, 'B')

# convert to cns form (further)
# mkdir initialzaion
initialization_dir = _output_file + 'initialization/'
os.system("mkdir -p " + initialization_dir)
# cns_model_a = pdb_reader.convert_to_cns(copy.deepcopy(model_a), _output_file + '/initialization/model_a_cns.pdb')
# cns_model_b = pdb_reader.convert_to_cns(copy.deepcopy(model_b), _output_file + '/initialization/model_b_cns.pdb')

# make contact table using contrains
restrains_file_name = initialization_dir + 'res.restraints'
file_handler.convert_dist_to_restrain(_input_dir=_input_dist_file, _segment_1='A', _segment_2='B',
                                      _output_dir=restrains_file_name)

# fix atom no
merge_cns_b = pdb_reader.fix_serial(model_b, len(model_a) + 1)
# merge the file

merged_pdb = model_a + merge_cns_b
merged_pdb_name = _output_file + str('cns_format.pdb')
merged_pdb_cns = pdb_reader.convert_to_cns(merged_pdb,merged_pdb_name)

# choose a fixed pdb
# generate docking.inp file
docking_dir = _output_file+'/docking/'
os.system('mkdir -p '+docking_dir)
file_handler.docking_inp(merged_pdb_name, 'A', restrains_file_name, _output_dir=docking_dir,_fixed_moving_chain='none')
#number can be very few adjust it and addd the change things
file_handler.job_docking(cns_dir,docking_dir)
os.system('chmod +x '+docking_dir+'/job_docking.sh')
# run the file
# os.chdir(docking_dir)
start = time.time()
process_state = os.system('./job_docking.sh')
print(process_state)
# select low scoring file
break_val = False

done = time.time()
elapsed = done - start
print(' time elapsed ' + str(elapsed) + '\n')
# read_file and get value
# keep the track

os.chdir(docking_dir)
file_list = []
for file in glob.glob("docking_*.pdb"):
    if not "start" in file:
        file_list.append(docking_dir+"/"+file)

details_array_all = pdb_reader.docking_details_returner(file_list,_model_count, docking_dir)

details_array_all = sorted(details_array_all, key=lambda energy: energy[1])
docked_pdb = pdb_reader.contents_to_info(pdb_reader.read_pdb(copy.deepcopy(details_array_all[0][0])))
print(details_array_all[0][0])
print(_input_model_b)
#x, y, z = pdb_reader.average_translation_finder_modified(model_b, docked_pdb, _input_dist_file)
#print(x, y, z)
new_generated = pdb_reader.translator(copy.deepcopy(merged_pdb),'B',-30.31,-7.7,-1.52)

pdb_reader.convert_to_cns(new_generated,_output_file+'/initialized.pdb')
