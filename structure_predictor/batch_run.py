import os.path
import sys

#
prog_dir =sys.arg[1]
pdb_files = sys.argv[2]
rr_files = sys.argv[3]
output_dir = sys.arg[4]

# prog_dir = '/home/rajroy/Documents/Git_MyScripts/Objective_2/cns_based_intact.py'
# pdb_files = '/home/rajroy/Downloads/input-1/test'
# rr_files = '/home/rajroy/Downloads/input-1/test_rr'
# output_dir = '/home/rajroy/Documents/Obj2_test2'

if not os.path.exists(output_dir):
    os.system("mkdir -p " + output_dir + '\n')

if not os.path.exists(rr_files):
    print("Failed to find " + rr_files + '\n')
    exit()

if not os.path.exists(prog_dir):
    print("Failed to find " + prog_dir + '\n')
    exit()

if not os.path.exists(pdb_files):
    print("Failed to find " + pdb_files + '\n')
    exit()

fileNames = []
# fileNames = glob.glob(fasta_dir + "/*fasta")
for root, directories, files in os.walk(rr_files):
    for file in files:
        if ".rr" in file:
            if not file.split(".")[0] in fileNames:
                fileNames.append(file.split("_")[0])

print(fileNames)

for file_name in fileNames:
    rr_file = rr_files + '/' + file_name + '_AB.rr'
    model_a = pdb_files + '/' + file_name + 'A.pdb'
    model_b = pdb_files + '/' + file_name + 'B.pdb'
    outfile = output_dir + '/' + file_name + '/'
    os.system('mkdir -p ' + outfile)
    command = 'python ' + prog_dir + ' ' + model_a + ' ' + model_b + ' ' + rr_file + ' ' + outfile
    print(command)
    os.system(command+' &> '+outfile+'log.txt')
