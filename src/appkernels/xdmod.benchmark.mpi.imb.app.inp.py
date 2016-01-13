walllimit=30

parser="xdmod.benchmark.mpi.imb.py"

#path to run script relative to AppKerDir on particular resource
#runScriptPath="execs/intel_mpi_bench/run"
#runScriptArgs=""
executabledir="execs/imb/src"
executable=executabledir+"/IMB-MPI1"
#Not really input
input=executabledir+"/IMB-EXT"

runScriptPreRun="""#create working dir
mkdir workdir
cd workdir

export AKRR_APPKER_EXEC_DIR={appKerDir}/{executabledir}
"""

akrrGenerateAppKernelSignature="""#Generate AppKer signature
appsigcheck.sh {appKerDir}/{executabledir}/IMB-MPI1 $AKRR_TASK_WORKDIR/.. >> $AKRR_APP_STDOUT_FILE
appsigcheck.sh {appKerDir}/{executabledir}/IMB-EXT  $AKRR_TASK_WORKDIR/.. >> $AKRR_APP_STDOUT_FILE
"""

akrrRunAppKernelTemplate="""#Execute AppKer
echo "Checking that running one process per node (for debugging)"
${{RUNMPI}} hostname

writeToGenInfo "appKerStartTime" "`date`"
${{RUNMPI}} ${{AKRR_APPKER_EXEC_DIR}}/IMB-MPI1 -multi 0 -npmin {akrrNNodes} -iter 1000 >> $AKRR_APP_STDOUT_FILE 2>&1
${{RUNMPI}} ${{AKRR_APPKER_EXEC_DIR}}/IMB-EXT  -multi 0 -npmin {akrrNNodes} -iter 1000 >> $AKRR_APP_STDOUT_FILE 2>&1
writeToGenInfo "appKerEndTime" "`date`"
"""

runScriptPostRun="""#clean-up
cd ..
if [ "${{AKRR_DEBUG=no}}" = "no" ]
then
        echo "Deleting input files"
        rm -rf workdir
fi
"""
