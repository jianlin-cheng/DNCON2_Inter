#!/bash/bin
#$1= fasta_file
#$2= intrachain_prediction_rr_file
#$3= pdb_file
#$4= outfolder
#$5= symmetry/asymmetry
#$6= filter_confidence=True/False
#$7= Top={5,10,L/10,L,5,L/2,L,2L,all}
source ./python3_venv/bin/activate
echo "Starting prediction tool..."
dirnm=$(dirname $(readlink -e $0))
#echo "DIR_NAME=" $dirnm

echo "Starting structure prediction..."
#python ./structure_predictor/structure_predictor.py $1 $2 $2 $3 $4
#python $dirnm/casp14_prediction_tool/link_2_structure_predictor.py $1 $3 $4 $dirnm #>structure_error.txt

python $dirnm/casp14_prediction_tool/link_update_v2.py $1 $3 $4 $dirnm $5 #>structure_prediction_main.log

echo "Please follow the structure_prediction_ log files"
if [ $? != 0 ]; then
    echo "Oops something went wrong with the structure tool! $?"
    exit 2
fi
#echo "Structure Prediction complete"

deactivate
