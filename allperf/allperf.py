import subprocess
import argparse
import os
import uuid
import cli
import config_parser

from perf_tests import gprof, time, cachegrind

def main():
    parser = argparse.ArgumentParser(description='AllPerf a Git compatible Performance tester')
    parser.add_argument("directory", action="store", help="The directory of the project to be tested")
    parser.add_argument("init", action="store_true", help="Enters the ")

    args = parser.parse_args()
    
    cfg = config_parser.ConfigParser(args.directory)

    interface = cli.CLI(cfg)
    interface.run()

    run = interface.get_run()

    run_id = uuid.uuid4()
    try:
        os.mkdir('/tmp/allperf')
    except FileExistsError:
        pass
    tmp_dir = '/tmp/allperf/{}'.format(run_id)
    os.mkdir(tmp_dir)
    os.system('cp -r {} {}'.format(args.directory, tmp_dir))

    os.system('cd {} && git checkout {}'.format(tmp_dir, run['git_ref']))

    test_type = run['test']
    if test_type == 'Time':
        time.run_test(run, tmp_dir)
    elif test_type == 'GProf':
        gprof.run_test(run, tmp_dir)
    elif test_type == 'Cachegrind':
        cachegrind.run_test(run, tmp_dir)

    return 0

if __name__ == "__main__":
    main()
