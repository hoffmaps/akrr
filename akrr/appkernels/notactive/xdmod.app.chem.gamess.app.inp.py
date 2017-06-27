name = """xdmod.app.chem.gamess"""
nickname = """xdmod.app.chem.gamess.@ncpus@"""
uri = """file:///home/charngda/Inca-Reporter//xdmod.app.chem.gamess"""
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
walllimit=13

parser="xdmod.app.chem.gamess.py"
#path to run script relative to AppKerDir on particular resource
runScriptPath="gamess/run"
runScriptArgs="input01"
