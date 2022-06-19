import json
import os

def convert_to_py(input_file, folder_path, py_path, markdown_path, markdown, line_breaks):
    flag = False

    try:
        with open(input_file, "r") as f:
            k = json.load(f)

        if os.path.exists(folder_path) == False:
            os.mkdir(folder_path)



        lines = []

        for i in k["cells"]:
            if i["cell_type"] == "code":
                for j in i["source"]:
                    lines.append(j.strip("\n"))
                if line_breaks:
                    lines.append("\n#----End Of Cell----\n")
                else:
                    lines.append("\n\n")

        with open(py_path, "w") as f:
            for i in lines:
                if (i!="" and i[0]=="%"):
                    continue
                f.write(i + "\n")


        lines1  = []
        if markdown:
            for i in k["cells"]:
                if i["cell_type"] == "markdown":
                    for j in i["source"]:
                        lines1.append(j.strip("\n"))
                    if line_breaks:
                        lines1.append("\n#### ----End Of Cell----\n")
                    else:
                        lines1.append("\n\n")

            with open(markdown_path, "w") as f:
                for i in lines1:
                    if (i!="" and i[0]=="%"):
                        continue
                    f.write(i + "\n")
        flag = True
    except:
        flag = False
    return flag


