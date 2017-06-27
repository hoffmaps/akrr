walllimit=13

parser="xdmod.app.md.namd.py"

#path to run script relative to AppKerDir on particular resource
executable="execs"
input="inputs/namd/apoa1_nve"

#common commands among resources to be executed prior the application kernel execution
#usually copying of input parameters, application signature calculation
runScriptPreRun="""#create working dir
export AKRR_TMP_WORKDIR=`mktemp -d {networkScratch}/namd.XXXXXXXXX`
echo "Temporary working directory: $AKRR_TMP_WORKDIR"
cd $AKRR_TMP_WORKDIR

#Copy inputs
cp {appKerDir}/{input}/* ./
"""

#common commands among resources to be executed after the application kernel execution
#usually cleaning up
runScriptPostRun="""
#clean-up
cd $AKRR_TASK_WORKDIR
if [ "${{AKRR_DEBUG=no}}" = "no" ]
then
        echo "Deleting temporary files"
        rm -rf $AKRR_TMP_WORKDIR
else
        echo "Copying temporary files"
        cp -r $AKRR_TMP_WORKDIR workdir
        rm -rf $AKRR_TMP_WORKDIR
fi
"""
