name = """xdmod.benchmark.io.ior"""
nickname = """xdmod.benchmark.io.ior.@ncpus@"""
uri = """file:///home/charngda/Inca-Reporter//xdmod.benchmark.io.ior"""
context = '''@batchpre@ -nodes=:@ppn@:@ncpus@ -walllimit=@walllimit@ -type=@batchFeature@ -exec="@@"'''
resourceSetName = """defaultGrid"""
action = """add"""
schedule = [
    """? ? 0-31/10 * *""",
]
arg_version = """no"""
arg_verbose = 1
arg_help = """no"""
arg_bin_path = """@bin_path@"""
arg_log = 5
walllimit=40
