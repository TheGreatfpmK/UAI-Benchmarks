import os
import subprocess
import sys

dir_path = os.path.dirname(os.path.realpath(__file__))

directory = os.fsencode(dir_path + '/models/uai')
models = [ f.path for f in os.scandir(directory) if f.is_dir() ]
logs_dir_first = os.fsencode(dir_path + '/logs/storm-logs/first/')
logs_dir_best = os.fsencode(dir_path + '/logs/storm-logs/best/') 
logs_dir_over = os.fsencode(dir_path + '/logs/storm-logs/over-approximation/') 

if len(sys.argv) > 1:
    storm_path = sys.argv[1]
else:
    storm_path = "./storm/build/bin/storm-pomdp"

print("Storm benchmark started")
print("----------------------------")

for model in models:
    model_name = os.path.basename(model).decode("utf-8")
    sketch_file = model.decode("utf-8") + "/sketch.templ"
    props_file = model.decode("utf-8") + "/sketch.props"

    os.system('rm -f {}/../test.txt'.format(dir_path))

    # BEST
    if "drone-4-2" in model_name:
        command = "{} --prism {} --prop {} --belief-exploration unfold --timeout 1800 --gap-threshold 0 --size-threshold 0 --clip-resolution 2 --expl-heuristic bfs --clipping-mode grid -tm --signal-timeout 60 --sound --lpsolver glpk --glpk:inttol 1e-9 --topological:minmax svi".format(storm_path, sketch_file, props_file)
    elif "rocks" in model_name:
        command = "{} --prism {} --prop {} --belief-exploration unfold --timeout 1800 --gap-threshold 0 --size-threshold 0 --clip-resolution 4 --expl-heuristic bfs --clipping-mode grid -tm --signal-timeout 60 --sound --lpsolver glpk --glpk:inttol 1e-9 --topological:minmax svi".format(storm_path, sketch_file, props_file)
    elif "hallway" in model_name:
        command = "{} --explicit-drn {} --prop {} --belief-exploration unfold --timeout 1800 --gap-threshold 0 --size-threshold 0 --clip-resolution 2 --expl-heuristic bfs --clipping-mode grid -tm --signal-timeout 60 --sound --lpsolver glpk --glpk:inttol 1e-9 --topological:minmax svi --buildchoicelab".format(storm_path, sketch_file, props_file)
    else:
        command = "{} --prism {} --prop {} --belief-exploration unfold --timeout 1800 --gap-threshold 0 --size-threshold 0 --clip-resolution 2 --expl-heuristic bfs --clipping-mode grid -tm --signal-timeout 60 --sound --lpsolver glpk --glpk:inttol 1e-9 --topological:minmax svi".format(storm_path, sketch_file, props_file)

    process = subprocess.Popen(command.split(), stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    output, error = process.communicate()
    process.wait()

    print(model_name, "best DONE")

    # FIRST
    if "hallway" in model_name:
        command_first = "{} --explicit-drn {} --prop {} --belief-exploration unfold --size-threshold 0 --gap-threshold 0 --clipping-threshold 0 --expl-heuristic bfs -tm --signal-timeout 60 --buildchoicelab".format(storm_path, sketch_file, props_file)
    else:
        command_first = "{} --prism {} --prop {} --belief-exploration unfold --size-threshold 0 --gap-threshold 0 --clipping-threshold 0 --expl-heuristic bfs -tm --signal-timeout 60".format(storm_path, sketch_file, props_file)

    process2 = subprocess.Popen(command_first.split(), stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    output_first, error_first = process2.communicate()
    process2.wait()

    print(model_name, "first DONE")

    # OVER-APP
    if "hallway" in model_name:
        command_over = "{} --explicit-drn {} --prop {} --belief-exploration discretize --resolution 8 --gap-threshold 0 --triangulationmode static -tm --signal-timeout 60 --sound --lpsolver gurobi --gurobi:inttol 1e-9 --gurobi:opttol 1e-9 --topological:minmax svi --buildchoicelab".format(storm_path, sketch_file, props_file)
    elif "maze" in model_name:
        command_over = "{} --prism {} --prop {} --belief-exploration discretize --resolution 8 --gap-threshold 0 --triangulationmode static -tm --signal-timeout 60 --sound --lpsolver gurobi --gurobi:inttol 1e-9 --gurobi:opttol 1e-9 --topological:minmax svi".format(storm_path, sketch_file, props_file)
    elif "grid-large" in model_name:
        command_over = "{} --prism {} --prop {} --belief-exploration discretize --resolution 4 --gap-threshold 0 --triangulationmode static -tm --signal-timeout 60 --sound --lpsolver gurobi --gurobi:inttol 1e-9 --gurobi:opttol 1e-9 --topological:minmax svi".format(storm_path, sketch_file, props_file)
    else:
        command_over = None

    if command_over is not None:

        process3 = subprocess.Popen(command_over.split(), stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        output_over, error_over = process3.communicate()
        process3.wait()

        print(model_name, "over-approximation DONE")


    with open(logs_dir_best.decode("utf-8") + model_name + "-" + "logs.txt", "w") as text_file:
        text_file.write(output.decode("utf-8"))

    with open(logs_dir_first.decode("utf-8") + model_name + "-" + "logs.txt", "w") as text_file:
        text_file.write(output_first.decode("utf-8"))

    if command_over is not None:
        with open(logs_dir_over.decode("utf-8") + model_name + "-" + "logs.txt", "w") as text_file:
            text_file.write(output_over.decode("utf-8"))

    print(model_name, "DONE")
    if error:
        print(error)