name = """xdmod.benchmark.gpu.shoc"""
info = """shoc


"""

nickname = """xdmod.benchmark.gpu.shoc.@nnodes@"""
uri = ""
context = '''@batchpre@ -nodes=@nnodes@:@ppn@ -type=@batchFeature@ -walllimit=@walllimit@ -exec="@@"'''
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
walllimit=20


