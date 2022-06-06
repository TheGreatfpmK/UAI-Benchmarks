import os
import subprocess
import sys

dir_path = os.path.dirname(os.path.realpath(__file__))

directory = os.fsencode(dir_path + '/models/uai')
models = [ f.path for f in os.scandir(directory) if f.is_dir() ]
logs_dir_fast = os.fsencode(dir_path + '/logs/paynt-logs/fastest/')
logs_dir_best = os.fsencode(dir_path + '/logs/paynt-logs/best/')

models_same_strat = ["grid-avoid-4-0", "grid-avoid-4-0.1", "crypt-4", "nrp-8", "drone-4-1", "drone-4-2", "network-prio-2-8-20", "rocks-12"]

if len(sys.argv) > 1:
    paynt_path = sys.argv[1]
else:
    paynt_path = "paynt/paynt.py"

print("PAYNT benchmark started")
print("----------------------------")

for model in models:
    model_name = os.path.basename(model).decode("utf-8")
    project = model.decode("utf-8") + "/"

    # FASTEST
    if "hallway" in model_name:
        command = "timeout 1800 python3 {} --project {} --filetype drn --incomplete-search --fsc-synthesis --fsc-memory-injection".format(paynt_path, project)
    else:
        command = "timeout 1800 python3 {} --project {} --incomplete-search --fsc-synthesis --fsc-memory-injection".format(paynt_path, project)

    process = subprocess.Popen(command.split(), stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    output, error = process.communicate()
    process.wait()

    print(model_name, "first part DONE")

    # BEST
    if model_name in models_same_strat:
        output2 = output
    else:
        if "grid-large" in model_name:
            command2 = "timeout 1800 python3 {} --project {} --method hybrid --incomplete-search --fsc-synthesis --fsc-memory-injection".format(paynt_path, project)
        elif "maze" in model_name or "refuel" in model_name:
            command2 = "timeout 1800 python3 {} --project {} --incomplete-search --fsc-synthesis".format(paynt_path, project)
        elif "hallway" in model_name:
            command2 = "timeout 1800 python3 {} --project {} --filetype drn --incomplete-search --fsc-synthesis".format(paynt_path, project)

        process2 = subprocess.Popen(command2.split(), stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        output2, error2 = process2.communicate()
        process2.wait()

    with open(logs_dir_fast.decode("utf-8") + model_name + "-" + "logs.txt", "w") as text_file:
        text_file.write(output.decode("utf-8"))

    with open(logs_dir_best.decode("utf-8") + model_name + "-" + "logs.txt", "w") as text_file:
        text_file.write(output2.decode("utf-8"))

    print(model_name, "DONE")
    if error:
        print(error)