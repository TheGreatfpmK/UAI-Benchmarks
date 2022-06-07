# UAI-Benchmarks

## Benchmark script

Run benchmarks with command:

> ./benchmark.sh -s PATH_TO_STORM_EXEC -p PATH_TO_PAYNT_EXEC -i PATH_TO_PRISM_EXEC [-x]

- `-s` specify path to Storm executable and run Storm benchmarks
- `-p` specify path to PAYNT executable and run PAYNT benchmarks
- `-i` specify path to Prism executable and run Prism benchmarks
- `-x` use this flag to run additional PAYNT benchmarks. This flag will only work if you specified path to PAYNT executable using the flag `-p`

For Storm and PAYNT benchmark models including their analysed properties will be taken from folder `models/uai`. For Prism they will be taken from folder `models/uai-prism`. And the models for additional PAYNT experiments will be taken from `models/uai-additional`.

Experiments will only run for specified flags i.e. if you run the benchmark with the only flag `-s`, only Storm benchmarks will be run.

The logs from all benchmarks will be saved to folder called `logs` in the directory from which you run the script. 

## Used versions of tools

- Prism - version 4.7.dev (http://www.prismmodelchecker.org/download.php)
- Storm - modified version 1.6.3 (https://zenodo.org/record/5734826)

## Original logs

The folder `original-logs` includes all log files from the original experiments for our paper.

The subfolders `paynt-logs`, `storm-logs` and `prism-logs` contain all of the experiments included in the main table of the paper, sectioned in the same way.

The subfolder `additional-logs` contain experiments which were not included in the main table but were mentioned in the paper.

### PAYNT experiments settings

List of settings:
- Incomplete search (*inc*) - `--incomplete-search`
- Complete search (*com*) - implicit if incomplete search is not used
- Synthesis method (*AR* or *Hyb*) - AR (implicit), Hybrid (`--method hybrid`)
- Synthesis with memory injection (*mem*) - `--fsc-memory-injection`
- Iterative synthesis (*iter*) - implicit if memory injection is not used

Default settings: Incomplete search, AR and Memory injection (inc, AR, mem)

|     **Model**    | **Fastest** |     **Best**    |
|------------------|:-----------:|:---------------:|
| crypt-4          |   Default   | Default         |
| drone-4-1        |   Default   | Default         |
| drone-4-2        |   Default   | Default         |
| grid-av-4-0      |   Default   | Default         |
| grid-av-4-0.1    |   Default   | (com, AR, iter) |
| grid-l-30-5      |   Default   | (inc, Hyb, mem) |
| hallway          |   Default   | (inc, AR, iter) |
| maze             |   Default   | (inc, AR, iter) |
| network-p-2-8-20 |   Default   | Default         |
| nrp-8            |   Default   | Default         |
| refuel-06        |   Default   | (inc, AR, iter) |
| rocks-12         |   Default   | Default         |

