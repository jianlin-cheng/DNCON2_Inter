#this script attempts to link the three .rr files to the structor prediction tool
#calls the structure_predictor/structure_predictor.py thrice
#needs three separate folder
import os,sys
#import numpy as np
#fnum=np.random.normal(size=3)

def noContact(file):
    lnum=0
    with open (file,"r") as f:
        for line in f:
            lnum+=1
    if lnum<=1: return True
    return False

fasta=sys.argv[1]
pdb_file=sys.argv[2]
outfolder=sys.argv[3]
dirnm=sys.argv[4]
rr_file=sys.argv[5]
sym=""#sys.argv[5]
if not dirnm.endswith("/"):dirnm+="/"
_id=fasta.split("/")[-1].replace(".fasta","")
print ("Processing for ID: "+_id)
pdb_dirname=os.path.dirname(os.path.abspath(pdb_file))
if not (pdb_dirname.endswith("/")): pdb_dirname+="/"

outfolder=os.path.abspath(outfolder)
#print (outdir_name)
#sys.exit()
print ("PDB_FILE:",pdb_file)
if not(outfolder.endswith("/")): outfolder+="/"
#os.system("ls ./"+outfolder+_id+"_inter_nointra_relax_remove_.rr")
pdb_list=[]
if ".atom" in pdb_file: os.system("ls "+pdb_dirname+pdb_file.split("/")[-1].split(".")[0]+"*.atom > "+outfolder+"pdb_list.txt")
print ("ATOM")
if ".pdb" in pdb_file: os.system("ls "+pdb_dirname+pdb_file.split("/")[-1].split(".")[0]+"*.pdb > "+outfolder+"pdb_list.txt")
print ("PDB")
#sys.exit()
print (outfolder+"pdb_list.txt")
#os.system("more "+outfolder+"pdb_list.txt")

#sys.exit()

with open (outfolder+"pdb_list.txt","r") as f:
    for line in f:
        if not (pdb_dirname in line.strip()): line=pdb_dirname+line.strip()
        pdb_list.append(line.strip())
print (pdb_list)
#rename the ".atom" files to ".pdb" files for structor_predictor
new_pdb_list=[]
for file in pdb_list:
    if (".atom" in file): os.system("cp "+file+" "+file.replace(".atom",".pdb"))
    file=file.replace(".atom",".pdb")
    new_pdb_list.append(file)


print('Translating file \n')
input_folder = outfolder+'/input_pdb/'
os.system('mkdir -p '+input_folder)
print ('copying the original pdb to '+ str(input_folder)+ '\n')
original_file = input_folder+_id+'.pdb'
os.system('cp '+new_pdb_list[0] + ' '+ original_file)

print ('Running the translator \n')
translate_cmd = 'python '+ dirnm +'/structure_predictor/coordinate_changer_one.py ' +  original_file  + ' '+ input_folder
print (str(translate_cmd) + '\n')
os.system(translate_cmd)
pdb_a = input_folder+_id+'_A'+'.pdb'
pdb_b = input_folder+_id+'_B'+'.pdb'


print (new_pdb_list)

#sys.exit()
outdir_list=[]
command=""
l=[]
"""
if noContact(outfolder+_id+"_inter_nointra_relax_remove_"+str(i)+".rr"):
        print ("The file "+outfolder+_id+"_inter_nointra_relax_remove_"+str(i)+".rr has no contacts. Skipping this.")
        continue
    command=command+"python "+dirnm+"/structure_predictor/structure_predictor.py "+_id+" "+pdb_a+" "+pdb_b+" "+outfolder+_id+"_inter_nointra_relax_remove_"+str(i)+".rr "+outdir_list[i] + "> structure_prediction_"+sym+"_"+_id+"_"+str(i)+".log & "
    l.append(i)
#    sys.exit()
"""
command=command+"python "+dirnm+"/structure_predictor/structure_predictor.py "+_id+" "+pdb_a+" "+pdb_b+" "+rr_file+" "+outfolder + "> structure_prediction_"+_id+".log & "
print ("\nRunning command ...\n")
print (command)
print("")
os.system(command)
print ("This will take a while as cns_solve will generate around 100 different structures.\n".upper())
print ("The structure prediction is running in the background.\n".upper())
print ("")
print ("Please keep checking the log files structure_prediction_"+sym+"_"+_id+"_0.log, structure_prediction_"+sym+"_"+_id+"_1.log and structure_prediction_"+sym+"_"+_id+"_2.log for updates\n")
#for num in l:
print ("The top five final structures will be available in the folder "+outfolder+_id+"_inter_nointra_relax_remove_"+"/"+_id+"/sorted/")
#print ("The final structures will be available in the folder "+outfolder+_id+"_inter_nointra_relax_remove_1/"+_id+"/initialized.pdb")
#print ("The final structures will be available in the folder "+outfolder+_id+"_inter_nointra_relax_remove_2/"+_id+"/initialized.pdb\n")
print ("The structure prediction is running in the background.\n".upper())
print ("You can check the work progress using 'top' command")







