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
    current_bond = ""
    for line in content:
        if "BD" in line or "BD*" in line or "LP" in line:
            data = line.split()
            bond_type = data[2]
            if "LP" in line:
                orbitals[f"{data[0]}"] = "n"
            elif "BD " in line:
                bond_key = f"{data[0]} {data[5]}[{data[6].replace("-", "")}]-{data[7]}[{data[8]}]"
                current_bond = bond_key
                orbitals[current_bond] = bond_type
            elif "BD*" in line:
                bond_key = f"{data[0]} {data[4]}[{data[5].replace("-", "")}]-{data[6]}[{data[7]}]"
                current_bond = bond_key
                orbitals[current_bond] = bond_type
        elif current_bond and "p" in line:
            values = line.split()
            for item in values:
                if "%)d" in item:
                    p_contribution = float(item.split("%)d")[0])
            if "BD*" in orbitals[current_bond]:
                if p_contribution > 95:
                    orbitals[current_bond] = "π*"
                elif p_contribution < 95:
                    orbitals[current_bond] = "σ*"
            elif "BD" in orbitals[current_bond]:
                if p_contribution > 95:
                    orbitals[current_bond] = "π"
                elif p_contribution < 95:
                    orbitals[current_bond] = "σ"
    modified_orbitals = {}
    for k, v in orbitals.items():
        modified_orbitals[k.split()[0]] = v
    return modified_orbitals

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

def interaction_energies(input_file, output_file, orbitals):
    with open(input_file, 'r') as infile:
        content = infile.readlines()
    with open(output_file, 'w'):
        pass
    start_pattern = "within unit  1"
    inside_section = False
    for line in content:
        if start_pattern in line:
            inside_section = True
            continue
        if inside_section:
            data = line.split()
            orbitals1 = orbitals
            for k, v in orbitals.items():
                for k1, v1, in orbitals1.items():
                    if "LP" in line and k == data[0] and k1 == data[6]:
                        with open(output_file, 'a', encoding = "utf-8") as outfile:
                            outfile.writelines(f"{k} {v} ({data[4]}[{data[5]}]) -> {k1} {v1} ({data[9]}[{data[10].replace("-", "")}]-{data[11]}[{data[12]}]) => {data[13]} kcal/mol \n")
                    if "BD" in line and k == data[0] and k1 == data[8]:
                        with open(output_file, 'a', encoding = "utf-8") as outfile:
                            outfile.writelines(f"{k} {v} ({data[4]}[{data[5].replace("-", "")}]-{data[6]}[{data[7]}]) -> {k1} {v1} ({data[11]}[{data[12].replace("-", "")}]-{data[13]}[{data[14]}]) => {data[15]} kcal/mol \n")
                
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
output_file3 = "ie_output_" + os.path.basename(file_path.replace(".log", ".txt"))

interaction_energies(output_file2, output_file3, orbitals)
if os.path.exists(output_file3) and os.path.getsize(output_file3) != 0:
    print(f"Successfully saved {output_file3}")
else:
    print("Error in extraction! Please try again...")