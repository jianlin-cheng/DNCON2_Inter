#this script attempts to link the three .rr files to the structor prediction tool
#calls the structure_predictor/structure_predictor.py thrice
#needs three separate folder
import os,sys

fasta=sys.argv[1]
pdb_file=sys.argv[2]
outfolder=sys.argv[3]
dirnm=sys.argv[4]
if not dirnm.endswith("/"):dirnm+="/"
_id=fasta.split("/")[-1].replace(".fasta","")
pdb_dirname=os.path.dirname(os.path.abspath(pdb_file))
if not (pdb_dirname.endswith("/")): pdb_dirname+="/"

outfolder=os.path.abspath(outfolder)
#print (outdir_name)
#sys.exit()
print ("PDB_FILE:",pdb_file)
if not(outfolder.endswith("/")): outfolder+="/"
#os.system("ls ./"+outfolder+_id+"_inter_nointra_relax_remove_.rr")
pdb_list=[]
if ".atom" in pdb_file: os.system("ls "+pdb_dirname+pdb_file.split("/")[-1][0:4]+"*.atom > "+outfolder+"pdb_list.txt")
print ("ATOM")
if ".pdb" in pdb_file: os.system("ls "+pdb_dirname+pdb_file.split("/")[-1][0:4]+"*.pdb > "+outfolder+"pdb_list.txt")
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

print (new_pdb_list)

#sys.exit()
outdir_list=[]
for i in range (3):
    outdir_list.append(outfolder+"relax_remove_"+str(i)+"/")
    #s.system("python ../structure_predictor/structure_predictor.py "+_id+" "+new_pdb_list[0]+" "+new_pdb_list[1]+" "+outfolder+_id+"_inter_nointra_relax_remove_"+str(i)+".rr "+outdir_list[i]+"> error"+str(i)+".txt")
    os.system("python "+dirnm+"/structure_predictor/structure_predictor.py "+_id+" "+new_pdb_list[0]+" "+new_pdb_list[1]+" "+outfolder+_id+"_inter_nointra_relax_remove_"+str(i)+".rr "+outdir_list[i])
    sys.exit()







