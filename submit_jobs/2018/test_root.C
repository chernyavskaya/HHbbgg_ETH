#include "TROOT.h"
#include "TSystem.h"
#include "TApplication.h"
#include <cstdlib>
#include <iostream>
#include <map>
#include <string>


using namespace std;

int main(int argc, char* argv[]){
//	char* variable_name = (argv[1]);
//	char* type = (argv[2]);
	char cmd[50];
	char cmd2[50];
	cout<<argc<<argv[4]<<endl;

	sprintf(cmd2,"treeForRegression_2018(%i,%i,%i,\"%s\")",atoi(argv[1]),atoi(argv[2]),atoi(argv[3]),argv[4]);
//	cout<<cmd<<endl;
	cout<<cmd2<<endl;
	gROOT->ProcessLine(".L treeForRegression_2018.C++");
	gROOT->ProcessLine(cmd2);
	return 0;
}

