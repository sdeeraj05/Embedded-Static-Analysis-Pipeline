import argparse
import os
import subprocess
import sys
import xml.etree.ElementTree as ET

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
PARENT_DIR = os.path.dirname(SCRIPT_DIR)

if os.path.exists(os.path.join(SCRIPT_DIR, "Project 1.dax")):
    TEMPLATE_DAX = os.path.join(SCRIPT_DIR, "Project 1.dax")
elif os.path.exists(os.path.join(PARENT_DIR, "Project 1.dax")):
    TEMPLATE_DAX = os.path.join(PARENT_DIR, "Project 1.dax")
else:
    print(
        f"[MISRA ERROR]: 'Project 1.dax' could not be found in either:\n  1. {SCRIPT_DIR}\n  2. {PARENT_DIR}",
        file=sys.stderr,
    )
    sys.exit(1)

A3_EXE = "a3"


def build_and_run_dax(module_name, sources, includes, out_dir, execute_now):
    os.makedirs(out_dir, exist_ok=True)

    output_dax = os.path.abspath(
        os.path.join(out_dir, f"CICD_{module_name.upper()}_MISRA.dax")
    )

    local_report_dir = os.path.join(out_dir, "reports")
    os.makedirs(local_report_dir, exist_ok=True)

    tree = ET.parse(TEMPLATE_DAX)
    root = tree.getroot()

    namespace = ""
    if "}" in root.tag:
        namespace = root.tag.split("}")[0][1:]
        ET.register_namespace("", namespace)

    def tag(name):
        return f"{{{namespace}}}{name}" if namespace else name

    name_node = root.find(tag("name"))
    if name_node is not None:
        name_node.text = f"CICD_{module_name.upper()}_MISRA"

    for elem in root.iter():
        if elem.tag.endswith("files"):
            for child in list(elem):
                elem.remove(child)
            for src in sources:
                ET.SubElement(elem, tag("file")).text = src.replace("\\", "/")
            break

    for elem in root.iter():
        if elem.tag.endswith("includes"):
            for child in list(elem):
                elem.remove(child)
            for inc in includes:
                ET.SubElement(elem, tag("include")).text = inc.replace("\\", "/")
            break

    for elem in root.iter():
        if elem.tag.endswith("report-file"):
            curr = elem.attrib.get("file", "")
            if curr:
                macro_tail = curr.replace("\\", "/").split("/")[-1]
                new_path = os.path.join(local_report_dir, macro_tail)
                elem.attrib["file"] = new_path.replace("/", "\\")

    if hasattr(ET, "indent"):
        ET.indent(tree, space="    ", level=0)

    tree.write(output_dax, encoding="utf-8", xml_declaration=True)
    print(f"-- [MISRA] Generated config -> {output_dax}")

    if execute_now:
        safe_exe = f'"{A3_EXE}"' if " " in A3_EXE else A3_EXE
        log_file = os.path.join(local_report_dir, f"{module_name.lower()}_run.log")

        cmd = f'{safe_exe} --batch --log-file "{log_file}" "{output_dax}"' #This line is the command to execute the dax file using command prompt change of needed

        print(f"-- [MISRA] Analyzing {module_name} in background...")
        result = subprocess.run(cmd, shell=True)

        if result.returncode == 0:
            print(f"-- [MISRA] [SUCCESS] {module_name}: Clean compile.")
        else:
            print(f"-- [MISRA] [FAILED] {module_name}: Triggered Exit Code {result.returncode}")
            print(f"-- [MISRA] Check log: {log_file}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="CMake to AbsInt Bridge")

    parser.add_argument("--module", required=True)
    parser.add_argument("--sources", nargs="+", required=True)
    parser.add_argument("--includes", nargs="*", default=[])
    parser.add_argument("--out-dir", required=True)
    parser.add_argument("--run", action="store_true")

    args = parser.parse_args()

    build_and_run_dax(
        args.module, args.sources, args.includes, args.out_dir, args.run
    )