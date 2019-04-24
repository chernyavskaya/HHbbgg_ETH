export WORKDIR=`pwd`
echo "Working on a machine:" `uname -a`
cd $WORKDIR

#g++ test_root.C -g -o test_root  `root-config --cflags --glibs`
#g++ treeForRegression_2018.C -g -o a_root `root-config --cflags --glibs` -lMLP -lXMLIO

num=1
max=1000
#num=1001
#max=1597
name=TTbar_nanoAOD

counter=0
#counter=100
while [ $num -lt $max ]
do

#	num2=$(( $num + 1 ))
	num2=$(( $num + 10 ))
	qsub -q all.q batch.sh $num $num2 $counter $name 
	sleep 2 

	echo $num $counter
#	num=$(( $num + 1 ))
	num=$(( $num + 10 ))
	counter=$(( $counter + 1 ))
done

