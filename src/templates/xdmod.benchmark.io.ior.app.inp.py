#which IO API/formats to check
testPOSIX=True
testMPIIO=True
testHDF5=True
testNetCDF=True

#will do write test first and after that read, that minimize the caching impact from storage nodes
#require large temporary storage easily 100s GiB 
doAllWritesFirst=True

appKernelRunEnvironmentTemplate="""
#load application environment
module load hdf5
module list

#set executable location
EXE=$AKRR_APPKER_DIR/execs/ior/src/ior

#set how to run mpirun on all nodes
for node in $AKRR_NODELIST; do echo $node>>all_nodes; done
RUNMPI="mpiexec -n $AKRR_CORES -f all_nodes"

#set how to run mpirun on all nodes with offset, first print all nodes after node 1 and then node 1
sed -n "$(($AKRR_CORES_PER_NODE+1)),$(($AKRR_CORES))p" all_nodes > all_nodes_offset
sed -n "1,$(($AKRR_CORES_PER_NODE))p" all_nodes >> all_nodes_offset
RUNMPI_OFFSET="mpiexec -n $AKRR_CORES -f all_nodes_offset"

#set striping for lustre file system
RESOURCE_SPECIFIC_OPTION_N_to_1="-O lustreStripeCount=$AKRR_NODES"
RESOURCE_SPECIFIC_OPTION_N_to_N=""

#other resource specific options
RESOURCE_SPECIFIC_OPTION=""
"""



