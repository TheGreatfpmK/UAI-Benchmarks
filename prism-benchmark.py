import os
import subprocess
import sys

dir_path = os.path.dirname(os.path.realpath(__file__))

directory = os.fsencode(dir_path + '/uai-prism')
models = [ f.path for f in os.scandir(directory) if f.is_dir() ]
logs_dir = os.fsencode(dir_path + '/logs/prism-logs/')

if len(sys.argv) > 1:
    prism_path = sys.argv[1]
else:
    prism_path = "prism"

print("Prism benchmark started")
print("----------------------------")

for model in models:
    model_name = os.path.basename(model).decode("utf-8")
    sketch_file = model.decode("utf-8") + "/sketch.templ"
    props_file = model.decode("utf-8") + "/sketch.props"

    if "hallway" in model_name:
        command = "timeout 7200 {} {} {} --gridresolution 2 -javamaxmem 16g -maxiters 1000000".format(prism_path, sketch_file, props_file)
    elif "grid-avoid" in model_name or "refuel" in model_name:
        command = "timeout 7200 {} {} {} --gridresolution 3 -javamaxmem 16g -maxiters 1000000".format(prism_path, sketch_file, props_file)
    elif "crypt" in model_name :
        command = "timeout 7200 {} {} {} --gridresolution 4 -javamaxmem 16g -maxiters 1000000".format(prism_path, sketch_file, props_file)
    elif "network" in model_name or "maze" in model_name or "nrp" in model_name:
        command = "timeout 7200 {} {} {} --gridresolution 10 -javamaxmem 16g -maxiters 1000000".format(prism_path, sketch_file, props_file)
    else:
        command = "timeout 7200 {} {} {} --gridresolution 2 -javamaxmem 16g -maxiters 1000000".format(prism_path, sketch_file, props_file)

    process = subprocess.Popen(command.split(), stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    output, error = process.communicate()
    process.wait()

    with open(logs_dir.decode("utf-8") + model_name + "-" + "logs.txt", "w") as text_file:
        text_file.write(output.decode("utf-8"))

    print(model_name, "DONE")
    if error:
        print(error)