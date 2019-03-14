import re
import xml.etree.cElementTree as ET
regex_float_pattern = r'[-+]?(\d+(\.\d*)?|\.\d+)([eE][-+]?\d+)?'

def build_tree(xgtree, base_xml_element, var_indices):
    parent_element_dict = {'0':base_xml_element}
    pos_dict = {'0':'s'}
    for line in xgtree.split('\n'):
        if not line: continue
        if ':leaf=' in line:
            #leaf node
            result = re.match(r'(\t*)(\d+):leaf=({0})$'.format(regex_float_pattern), line)
            if not result:
                print line
            depth = result.group(1).count('\t')
            inode = result.group(2)
            res = result.group(3)
            node_elementTree = ET.SubElement(parent_element_dict[inode], "Node", pos=str(pos_dict[inode]),
                                             depth=str(depth), NCoef="0", IVar="-1", Cut="0.0e+00", cType="1", res=str(res), rms="0.0e+00", purity="0.0e+00", nType="-99")
        else:
            #\t\t3:[var_topcand_mass<138.19] yes=7,no=8,missing=7
            result = re.match(r'(\t*)([0-9]+):\[(?P<var>.+)<(?P<cut>{0})\]\syes=(?P<yes>\d+),no=(?P<no>\d+)'.format(regex_float_pattern),line)
            
            if not result:
                print line
            depth = result.group(1).count('\t')
            inode = result.group(2)
            var = result.group('var')
            cut = result.group('cut')
            lnode = result.group('yes')
            rnode = result.group('no')
            pos_dict[lnode] = 'l'
            pos_dict[rnode] = 'r'
            node_elementTree = ET.SubElement(parent_element_dict[inode], "Node", pos=str(pos_dict[inode]),
                                             depth=str(depth), NCoef="0", IVar=str(var_indices[var]), Cut=str(cut),
                                             cType="1", res="0.0e+00", rms="0.0e+00", purity="0.0e+00", nType="0")
            parent_element_dict[lnode] = node_elementTree
            parent_element_dict[rnode] = node_elementTree
            
def convert_model(model, input_variables, output_xml, input_variables_names, kind="Classification"):
    NTrees = len(model)
    var_list = input_variables
    var_indices = {}
    var_names = input_variables_names
    
    # <MethodSetup>
    MethodSetup = ET.Element("MethodSetup", Method="BDT::BDT")

    # <Variables>
    Variables = ET.SubElement(MethodSetup, "Variables", NVar=str(len(var_list)))
    for ind, val in enumerate(var_list):
        name = val[0]
        #here removing "noexpand:" which is the common way for scikit-learn to save expressions
        expression = input_variables_names[ind].replace("noexpand:","")
        #if you have weird variables with / in the name you need this, otherwise doesn't matter
        internal=input_variables_names[ind].replace("noexpand:","").replace("(","_").replace(")","_").replace("/","_D_")
        var_type = val[1]
        var_indices[name] = ind
#        change also internal
        Variable = ET.SubElement(Variables, "Variable", VarIndex=str(ind), Type=val[1], 
            Expression=expression, Label=name, Title=name, Unit="", Internal=internal, 
            Min="0.0e+00", Max="0.0e+00")

    # <GeneralInfo>
    GeneralInfo = ET.SubElement(MethodSetup, "GeneralInfo")
    Info_Creator = ET.SubElement(GeneralInfo, "Info", name="Creator", value="xgboost2TMVA")
    if (kind=="Classification"):
        Info_AnalysisType = ET.SubElement(GeneralInfo, "Info", name="AnalysisType", value="Classification")
    elif (kind=="Multiclass"):
        print("setting up conversion for multiclass classification")
        Info_AnalysisType = ET.SubElement(GeneralInfo, "Info", name="AnalysisType", value="Multiclass")
    
    
    # <Options>
    Options = ET.SubElement(MethodSetup, "Options")
    Option_NodePurityLimit = ET.SubElement(Options, "Option", name="NodePurityLimit", modified="No").text = "5.00e-01"
    Option_BoostType = ET.SubElement(Options, "Option", name="BoostType", modified="Yes").text = "Grad"

    if (kind=="Multiclass"):
        Classes = ET.SubElement(MethodSetup, "Classes", NClass="3")
        Classes_Name1 = ET.SubElement(Classes,"Class", Name="Background", Index="0")
        Classes_Name2 = ET.SubElement(Classes,"Class", Name="Background2", Index="1")
        Classes_Name3 = ET.SubElement(Classes,"Class", Name="Signal", Index="2")
    
    # <Weights>
    Weights = ET.SubElement(MethodSetup, "Weights", NTrees=str(NTrees), AnalysisType="1")
    
    for itree in range(NTrees):
        BinaryTree = ET.SubElement(Weights, "BinaryTree", type="DecisionTree", boostWeight="1.0e+00", itree=str(itree))
        build_tree(model[itree], BinaryTree, var_indices)

        
    tree = ET.ElementTree(MethodSetup)
    tree.write(output_xml)
    # format it with 'xmllint --format'
    
# example
## branch_names is the list of variables used to train, clf is the trained model
# model = clf.get_booster().get_dump()
#vartypes = ['F']*len(branch_names)
#varfakenames =[]
##the variables in the pkl file are just saved as f0,f1...the naming is done manually
#for i in range(0,len(branch_names)):
#    print i
#    varfakenames.append('f%s'%str(i))
#x2tmva.convert_model(model,input_variables=zip(varfakenames,vartypes,Multiclass),output_xml='2017_training_Mjj.xml',input_variables_names=branch_names)

