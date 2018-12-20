import os
import sys
from akrr.appkernelsparsers.akrrappkeroutputparser import AppKerOutputParser, total_seconds


def process_appker_output(appstdout=None, stdout=None, stderr=None, geninfo=None, resource_appker_vars=None):
    """
    Process test appkernel output.
    """
    # set App Kernel Description
    parser = AppKerOutputParser(
        name='test',
        version=1,
        description="Test the resource deployment",
        url='http://xdmod.buffalo.edu',
        measurement_name='test'
    )
    # set obligatory parameters and statistics
    # set common parameters and statistics
    parser.add_common_must_have_params_and_stats()
    # set app kernel custom sets
    parser.add_must_have_statistic('Wall Clock Time')
    parser.add_must_have_statistic('Shell is BASH')
    # parse common parameters and statistics
    parser.parse_common_params_and_stats(appstdout, stdout, stderr, geninfo)

    # set statistics
    if parser.wallClockTime is not None:
        parser.set_statistic("Wall Clock Time", total_seconds(parser.wallClockTime), "Second")

    # read output
    lines = []
    if os.path.isfile(stdout):
        fin = open(stdout, "rt")
        lines = fin.readlines()
        fin.close()

    # process the output
    parser.set_statistic('Shell is BASH', 0)
    j = 0
    while j < len(lines):
        if lines[j].count("Checking that the shell is BASH") > 0 and lines[j + 1].count("bash") > 0:
            parser.set_statistic('Shell is BASH', 1)
        j += 1

    if __name__ == "__main__":
        # output for testing purpose
        print(("parsing complete:", parser.parsing_complete()))
        parser.print_params_stats_as_must_have()
        print((parser.get_xml()))

    # return complete XML otherwise return None
    return parser.get_xml()


if __name__ == "__main__":
    """stand alone testing"""
    jobdir = sys.argv[1]
    print(("Processing Output From", jobdir))
    process_appker_output(appstdout=os.path.join(jobdir, "appstdout"),
                          stdout=os.path.join(jobdir, "stdout"),
                          stderr=os.path.join(jobdir, "stderr"),
                          geninfo=os.path.join(jobdir, "gen.info"))
