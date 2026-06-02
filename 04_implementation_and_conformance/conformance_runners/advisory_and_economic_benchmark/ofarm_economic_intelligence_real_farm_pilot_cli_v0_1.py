import argparse
import json
import subprocess
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
VALIDATOR = HERE / 'ofarm_economic_intelligence_real_farm_pilot_validator_v0_2.py'
RUNNER = HERE / 'ofarm_economic_intelligence_real_farm_pilot_runner_v0_2.py'
DEFAULT_DATASET = HERE / 'ofarm_economic_intelligence_real_farm_pilot_dataset_illustrative_v0_2.json'


def main() -> None:
    parser = argparse.ArgumentParser(description='Validate then run the bounded OFARM economics real-farm pilot.')
    parser.add_argument('dataset', nargs='?', default=str(DEFAULT_DATASET), help='Path to pilot dataset JSON.')
    parser.add_argument('--output-dir', default=None, help='Optional output directory for reports/results.')
    args = parser.parse_args()

    dataset = Path(args.dataset).resolve()
    cmd_common = [str(dataset)]
    if args.output_dir:
        cmd_common += ['--output-dir', str(Path(args.output_dir).resolve())]

    print('== Running readiness validator ==')
    subprocess.run([sys.executable, str(VALIDATOR), *cmd_common], check=True)
    print('== Running bounded pilot ==')
    subprocess.run([sys.executable, str(RUNNER), *cmd_common], check=True)
    print('== Complete ==')


if __name__ == '__main__':
    main()
