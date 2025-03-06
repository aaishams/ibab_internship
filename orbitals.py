import os

def extract_orbitals(file_path, output_file):
    with open(file_path, 'r') as input:
        content = input.readlines()
    start_pattern = "(Occupancy)   Bond orbital / Coefficients / Hybrids"
    inside_section = False
    with open(output_file, 'w'):
        pass
    for line in content:
        if start_pattern in line:
            inside_section = True
            continue
        if inside_section and "RY" in line:
            inside_section = False
            break
        if inside_section and "(" in line:
            with open(output_file, 'a') as output:
                output.writelines(line)

def orbital_type(output_file):
    with open(output_file, 'r') as input:
        content = input.readlines()
    orbitals = {}
    for line in content:
        if "LP" in line:
            n = line.split()
            orbitals[f"{n[0]} {n[5]}[{n[6]}]"] = f"1 n orbital"
        if "BD ( 1)" in line:
            s = line.split()
            orbitals[f"{s[0]} {s[5]}[{s[6].replace("-", "")}]-{s[7]}[{s[8]}]"] = f"1 σ orbital"
        if "BD ( 2)" in line:
            sp = line.split()
            orbitals[f"{sp[0]} {sp[5]}[{sp[6].replace("-", "")}]-{sp[7]}[{sp[8]}]"] = f"1 π orbital"
        if "BD ( 3)" in line:
            sp2 = line.split()
            orbitals[f"{sp2[0]} {sp2[5]}[{sp2[6].replace("-", "")}]-{sp2[7]}[{sp2[8]}]"] = f"1 π orbital"
        if "BD* ( 1)" in line:
            ss = line.split()
            orbitals[f"{ss[0]} {ss[5]}[{ss[6].replace("-", "")}]-{ss[7]}[{ss[8]}]"] = f"1 σ* orbital"
        if "BD* ( 2)" in line:
            sps = line.split()
            orbitals[f"{sps[0]} {sps[5]}[{sps[6].replace("-", "")}]-{sps[7]}[{sps[8]}]"] = f"1 π* orbital"
        if "BD* ( 3)" in line:
            sp2s = line.split()
            orbitals[f"{sp2s[0]} {sp2s[5]}[{sp2s[6].replace("-", "")}]-{sp2s[7]}[{sp2s[8]}]"] = f"1 π* orbital"
    return orbitals

def extract_energies(file_path, output_file):
    with open(file_path, 'r') as file:
        content = file.readlines()
    start_pattern = "SECOND ORDER PERTURBATION THEORY ANALYSIS OF FOCK MATRIX IN NBO BASIS"
    end_pattern = "NATURAL BOND ORBITALS (Summary)"
    inside_section = False
    with open(output_file, 'w'):
        pass
    for line in content:
        if start_pattern in line:
            inside_section = True
            with open(output_file, 'a') as out_file:
                out_file.write(line)
            continue
        if inside_section and end_pattern in line:
            inside_section = False
            break
        if inside_section and "RY" not in line and "CR" not in line:
            with open(output_file, 'a') as out_file:
                out_file.writelines(line)

file_path = input("Enter the log file path: ").strip()
if not os.path.exists(file_path):
    print("Please enter a valid file path!")
    file_path = input("Enter the log file path: ").strip()
output_file1 = "or_output_" + os.path.basename(file_path.replace(".log", ".txt"))
extract_orbitals(file_path, output_file1)
if os.path.exists(output_file1) and os.path.getsize(output_file1) != 0:
    print(f"Successfully saved {output_file1}")
else:
    print("Error in extraction! Please try again...")
orbitals = orbital_type(output_file1)
print(orbitals)
output_file2 = "pe_output_" + os.path.basename(file_path.replace(".log", ".txt"))
extract_energies(file_path, output_file2)
if os.path.exists(output_file2) and os.path.getsize(output_file2) != 0:
    print(f"Successfully saved {output_file2}")
else:
    print("Error in extraction! Please try again...")