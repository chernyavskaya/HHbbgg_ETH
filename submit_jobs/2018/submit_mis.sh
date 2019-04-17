export WORKDIR=`pwd`
echo "Working on a machine:" `uname -a`
cd $WORKDIR

#g++ test_root.C -g -o test_root  `root-config --cflags --glibs`
#g++ treeForRegression_2017.C -g -o a_root `root-config --cflags --glibs` -lMLP -lXMLIO

num=1
max=166 
name=TTbar_nanoAOD

#counter=0
for num in `cat missing_1.txt`
do
	counter=$(( $num + 1 ))
	num2=$(( $num + 2 ))
	qsub -q all.q batch.sh $counter $num2 $num $name 
	echo $counter $num2 $num $name 
	sleep 10 
#	echo $num
done

