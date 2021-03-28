#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Mar 17 14:19:07 2020

@author: farhan
"""

import os,sys

def getName(file):
    return file.split("/")[-1].split(".")[0]

fasta_file=sys.argv[1]
rr_file=sys.argv[2]
pdb_file=sys.argv[3]
outfolder=sys.argv[4]
dirnm=sys.argv[5]
sym=sys.argv[6]
filter_conf=sys.argv[7]
top=sys.argv[8]

#if (filter_conf)

if not (os.path.exists(fasta_file)):
    sys.exit("Fasta file not found. Quitting")
    
if not (os.path.exists(rr_file)):
    sys.exit("Contact map file not found. Quitting")

if not (os.path.exists(pdb_file)):
    sys.exit("PDB file not found. Quitting")

if not (dirnm.endswith("/")): dirnm+="/"

if not(os.path.isdir(outfolder)): os.makedirs(outfolder)
if not(outfolder.endswith("/")):outfolder+="/"
name=getName(pdb_file)
if not (os.path.isdir(outfolder+"workdir/")):os.mkdir(outfolder+"workdir/")
workdir=outfolder+"workdir/"
os.system("scp "+fasta_file+" "+workdir+"current_job.fasta")
fasta_file=workdir+"current_job.fasta"
os.system("scp "+pdb_file+" "+workdir+"current_job.pdb")
pdb_file=workdir+"current_job.pdb"
os.system("python ./scripts/sortrr.py "+rr_file+" True > "+workdir+"current_job.rr")
#os.system("scp "+rr_file+" "+workdir+"current_job.rr")
rr_file=workdir+"current_job.rr"
#exit_code=os.system("python "+dirnm+"casp14_prediction_tool/scripts/pdb2distancemonomer.py "+pdb_file+" "+fasta_file+" 8 "+workdir+"current_job_intra")
#print ("##### Here ######")
#if (exit_code!=0): sys.exit("Oops! Something went wrong while executing\n"+"python "+dirnm+"casp14_prediction_tool/scripts/pdb2distancemonomer.py "+pdb_file+" "+fasta_file+" 8 "+outfolder+getName(pdb_file))

#exit_code=os.system("python "+dirnm+"casp14_prediction_tool/scripts/createPredictionFromContacts.py "+rr_file+" "+workdir+"current_job_intra.rr"+" "+dirnm+" "+filter_conf+" "+top)
#sys.exit()

#if (exit_code!=0): sys.exit("Oops! Something went wrong while executing\n"+"python ./scripts/createPredictionFromContacts.py "+rr_file+" "+workdir+"current_job_intra.rr "+dirnm+" "+filter_conf+" "+top)
#print ("Prediction successfull!")
"""
if (sym=="True" or sym=="symmetric" or sym == "symmetry"):
    print ("Creating symmetric contact map files...")
    for i in range(3):
        os.system("python "+dirnm+"casp14_prediction_tool/scripts/makeSymmetry.py "+workdir+"current_job_sorted_nointra_relax_remove_"+str(i)+".rr "+workdir+"current_job_sorted_nointra_relax_remove_"+str(i)+".rr "+dirnm+" "+top)
"""
#os.system("mv "+workdir+"current_job_intra.rr "+" "+outfolder+name+"_true_intra.rr")
os.system("mv "+workdir+"current_job.rr "+" "+outfolder+name+".rr")
#os.system("mv "+workdir+"current_job_sorted_nointra_relax_remove_1.rr "+" "+outfolder+name+"_inter_nointra_relax_remove_1.rr")
#os.system("mv "+workdir+"current_job_sorted_nointra_relax_remove_2.rr "+" "+outfolder+name+"_inter_nointra_relax_remove_2.rr")
os.system("rm -rf "+workdir)
#print ("mv "+workdir+"current_job_result* "+"* "+outfolder)

