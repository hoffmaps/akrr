# Part of XDMoD=>AKRR
# parser for HPCG Benchmarks AK
#
# initial contribution by Trey Dockendorf
#

import re
import os
import sys
from akrr.parsers.akrrappkeroutputparser import AppKerOutputParser, total_seconds
import akrr.util.log as log


def process_appker_output(appstdout=None, stdout=None, stderr=None, geninfo=None, resource_appker_vars=None):
    # set App Kernel Description
    parser = AppKerOutputParser(
        name='hpcg',
        version=1,
        description="HPCG Benchmark",
        url='http://www.hpcg-benchmark.org/index.html',
        measurement_name='HPCG'
    )
    # set obligatory parameters and statistics
    # set common parameters and statistics
    parser.add_common_must_have_params_and_stats()
    # set app kernel custom sets
    parser.add_must_have_parameter('App:ExeBinSignature')
    parser.add_must_have_parameter('App:Version')
    parser.add_must_have_parameter('Input:Distributed Processes')
    parser.add_must_have_parameter('Input:Global Problem Dimensions Nx')
    parser.add_must_have_parameter('Input:Global Problem Dimensions Ny')
    parser.add_must_have_parameter('Input:Global Problem Dimensions Nz')
    parser.add_must_have_parameter('Input:Local Domain Dimensions Nx')
    parser.add_must_have_parameter('Input:Local Domain Dimensions Ny')
    parser.add_must_have_parameter('Input:Local Domain Dimensions Nz')
    parser.add_must_have_parameter('Input:Number of Coarse Grid Levels')
    parser.add_must_have_parameter('Input:Threads per processes')
    parser.add_must_have_parameter('RunEnv:CPU Speed')
    parser.add_must_have_parameter('RunEnv:Nodes')

    parser.add_must_have_statistic('Floating-Point Performance, Raw DDOT')
    parser.add_must_have_statistic('Floating-Point Performance, Raw MG')
    parser.add_must_have_statistic('Floating-Point Performance, Raw SpMV')
    parser.add_must_have_statistic('Floating-Point Performance, Raw Total')
    parser.add_must_have_statistic('Floating-Point Performance, Raw WAXPBY')
    parser.add_must_have_statistic('Floating-Point Performance, Total')
    parser.add_must_have_statistic('Memory Bandwidth, Read')
    parser.add_must_have_statistic('Memory Bandwidth, Total')
    parser.add_must_have_statistic('Memory Bandwidth, Write')
    parser.add_must_have_statistic('Setup Time')
    parser.add_must_have_statistic('Wall Clock Time')

    # parse common parameters and statistics
    parser.parse_common_params_and_stats(appstdout, stdout, stderr, geninfo, resource_appker_vars)
    
    if hasattr(parser, 'appKerWallClockTime'):
        parser.set_statistic("Wall Clock Time", total_seconds(parser.appKerWallClockTime), "Second")

    # get path to YAML file
    # read data
    lines = []
    if os.path.isfile(appstdout):
        fin = open(appstdout, "rt")
        lines = fin.readlines()
        fin.close()

    # Parse YAML lines because YAML is often malformed
    yaml_lines = []
    # get yaml lines from appstdout
    bool_in_yaml_section = False
    for line in lines:
        if re.match(r"^====== .+\.yaml End   ======", line):
            break

        if bool_in_yaml_section:
            yaml_lines.append(line)

        if re.match(r"^====== .+\.yaml Start ======", line):
            bool_in_yaml_section = True

    from pprint import pprint
    import yaml
    # fix some issues with yaml
    if re.search(r"After confirmation please upload results from the YAML", yaml_lines[-1]):
        yaml_lines.pop()
    if re.search(r"You have selected the QuickPath option", yaml_lines[-1]):
        yaml_lines.pop()

    yaml_text = "".join(yaml_lines)

    yaml_text = re.sub(
        r"^ {6}HPCG 2\.4 Rating \(for historical value\) is:",
        "  HPCG 2.4 Rating (for historical value) is:",
        yaml_text,  flags=re.M)

    results_yaml = yaml.load(yaml_text)

    # Set Parameters
    # App version
    app_version_list = []
    for ver in [x for x in results_yaml.keys() if re.search("version", x)]:
        app_version_list.append(ver + " " + str(results_yaml[ver]))
    app_version = ", ".join(app_version_list)
    parser.set_parameter('App:Version', app_version)

    # Problem size
    parser.set_parameter('Input:Number of Coarse Grid Levels',
                         results_yaml['Multigrid Information']['Number of coarse grid levels'])

    parser.set_parameter('Input:Global Problem Dimensions Nx',
                         results_yaml['Global Problem Dimensions']['Global nx'])
    parser.set_parameter('Input:Global Problem Dimensions Ny',
                         results_yaml['Global Problem Dimensions']['Global ny'])
    parser.set_parameter('Input:Global Problem Dimensions Nz',
                         results_yaml['Global Problem Dimensions']['Global nz'])

    parser.set_parameter('Input:Local Domain Dimensions Nx',
                         results_yaml['Local Domain Dimensions']['nx'])
    parser.set_parameter('Input:Local Domain Dimensions Ny',
                         results_yaml['Local Domain Dimensions']['ny'])
    parser.set_parameter('Input:Local Domain Dimensions Nz',
                         results_yaml['Local Domain Dimensions']['nz'])

    parser.set_parameter('Input:Distributed Processes',
                         results_yaml['Machine Summary']['Distributed Processes'])
    parser.set_parameter('Input:Threads per processes',
                         results_yaml['Machine Summary']['Threads per processes'])

    if "cpu_speed" in parser.geninfo:
        ll = parser.geninfo["cpu_speed"].splitlines()
        cpu_speed_max = 0.0
        for l in ll:
            m = re.search(r'([\d.]+)$', l)
            if m:
                v = float(m.group(1).strip())
                if v > cpu_speed_max:
                    cpu_speed_max = v
        if cpu_speed_max > 0.0:
            parser.set_parameter("RunEnv:CPU Speed", cpu_speed_max, "MHz")

    # Set Statistics
    parser.successfulRun = results_yaml['Reproducibility Information']['Result'] == 'PASSED'

    parser.set_statistic('Setup Time',
                         results_yaml['Setup Information']['Setup Time'], 'Seconds')

    parser.set_statistic('Memory Bandwidth, Read',
                         results_yaml['GB/s Summary']['Raw Read B/W'], 'GB/s')
    parser.set_statistic('Memory Bandwidth, Write',
                         results_yaml['GB/s Summary']['Raw Write B/W'], 'GB/s')
    parser.set_statistic('Memory Bandwidth, Total',
                         results_yaml['GB/s Summary']['Raw Total B/W'], 'GB/s')

    parser.set_statistic(
        'Floating-Point Performance, Total',
        results_yaml['__________ Final Summary __________']['HPCG result is VALID with a GFLOP/s rating of'], 'GFLOP/s')

    parser.set_statistic('Floating-Point Performance, Raw DDOT',
                         results_yaml['GFLOP/s Summary']['Raw DDOT'], 'GFLOP/s')
    parser.set_statistic('Floating-Point Performance, Raw WAXPBY',
                         results_yaml['GFLOP/s Summary']['Raw WAXPBY'], 'GFLOP/s')
    parser.set_statistic('Floating-Point Performance, Raw SpMV',
                         results_yaml['GFLOP/s Summary']['Raw SpMV'], 'GFLOP/s')
    parser.set_statistic('Floating-Point Performance, Raw MG',
                         results_yaml['GFLOP/s Summary']['Raw MG'], 'GFLOP/s')
    parser.set_statistic('Floating-Point Performance, Raw Total',
                         results_yaml['GFLOP/s Summary']['Raw Total'], 'GFLOP/s')

    if __name__ == "__main__":
        # output for testing purpose
        print("parsing complete:", parser.parsing_complete(verbose=True))
        parser.print_params_stats_as_must_have()
        print(parser.get_xml())

    # return complete XML otherwise return None
    return parser.get_xml()

    
if __name__ == "__main__":
    """stand alone testing"""
    job_dir = sys.argv[1]
    print("Processing Output From", job_dir)
    process_appker_output(
        appstdout=os.path.join(job_dir, "appstdout"),
        stdout=os.path.join(job_dir, "stdout"),
        stderr=os.path.join(job_dir, "stderr"),
        geninfo=os.path.join(job_dir, "gen.info"))
