#This software uses the predicted intrachain contact map in the RR format and the PDB structure of the monomer to create an interchain prediction.

#Three predictions are created- no relax removal, relax removal = 1 and relax removal = 2

#The low confidence contacts (p < 0.5) and the short range contacts (|i-j|<6) are filtered out from the predictions. This makes the number of contacts more sparse and cns_solve works faster.
#csn_solve will producte upto 100 structures and will so take a while. The software will run in the background until it finishes. Keep checking the log files to see if the task has been completed. 

#The tasks can also be monitored using "top" command. 

#The folder /exports/store1/casp14_capri/test_sample/ contains some sample test data.

#There are two types of predictions that can be made- symmetric and asymetric
#Symmetric predictions are for dimers that form a symmetric complex. The final prediction contact map is converted into a symmetric matrix and a new contact map is generated containing both the upper and lower triangles. 
#Asymetric prediction only contains the upper triangle. 

#The package is installed in the folder: /exports/store1/casp14_capri/
#In this folder, the "run_full_prediction_v2.sh file" can be used to run the software.
#Please follow the following commands to run the software:
#	$ cd /exports/store1/casp14_capri/
# 	$ sh run_full_prediction_v2.sh <fasta_file> <contact_map_file> <input_pdb_of_one_chain> <outputfolder> <symmetry or asymetry>
#For example:
#	$ sh run_full_prediction_v2.sh ./test_sample/selected_interchains/fasta_folder/1A64.fasta ./test_sample/selected_interchains/dncon2/1A64.dncon2.rr ./test_sample/selected_interchains/test_pdb_folder/1A64_A.pdb ./test_sample/outfolder_symmetric_filtered_1A64_test symmetry

#This will cause cns_solve to run in the background. 


