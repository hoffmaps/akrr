name = """xdmod.app.chem.nwchem"""
nickname = """xdmod.app.chem.nwchem.@ncpus@"""
uri = """file:///home/charngda/Inca-Reporter//xdmod.app.chem.nwchem"""
context = '''@batchpre@ -nodes=:@ppn@:@ncpus@ -type=@batchFeature@ -walllimit=@walllimit@ -exec="@@"'''
resourceSetName = """defaultGrid"""
action = """add"""
schedule = [
    """? ? */10 * *""",
]
arg_version = """no"""
arg_verbose = 1
arg_help = """no"""
arg_bin_path = """@bin_path@"""
arg_log = 5
walllimit=22

parser="xdmod.app.chem.nwchem.py"
#path to run script relative to AppKerDir on particular resource
runScriptPath="nwchem/run"
runScriptArgs="input01"

