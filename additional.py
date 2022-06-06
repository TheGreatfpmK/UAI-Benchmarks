import os
import subprocess
import sys

dir_path = os.path.dirname(os.path.realpath(__file__))

directory = os.fsencode(dir_path + '/models/uai-additional')
models = [ f.path for f in os.scandir(directory) if f.is_dir() ]
logs_dir = os.fsencode(dir_path + '/logs/additional-logs/')

if len(sys.argv) > 1:
    paynt_path = sys.argv[1]
else:
    paynt_path = "paynt/paynt.py"

print("Additional PAYNT benchmark started")
print("----------------------------")

for model in models:
    model_name = os.path.basename(model).decode("utf-8")
    project = model.decode("utf-8") + "/"

    if "grid-avoid-4-0.1" in model_name:
        command = "timeout 1800 python3 {} --project {} --fsc-synthesis --fsc-memory-injection".format(paynt_path, project)
    else:
        command = "timeout 1800 python3 {} --project {} --incomplete-search --fsc-synthesis --fsc-memory-injection".format(paynt_path, project)

    process = subprocess.Popen(command.split(), stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    output, error = process.communicate()
    process.wait()

    with open(logs_dir.decode("utf-8") + model_name + "-" + "logs.txt", "w") as text_file:
        text_file.write(output.decode("utf-8"))

    print(model_name, "DONE")
    if error:
        print(error)