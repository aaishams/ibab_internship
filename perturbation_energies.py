import os

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
        if inside_section:
            with open(output_file, 'a') as out_file:
                out_file.writelines(line)

file_path = input("Enter the log file path: ").strip()
while not os.path.exists(file_path):
    print("Please enter a valid file path!")
    file_path = input("Enter the log file path: ").strip()
output_file = "pe_output_" + os.path.basename(file_path.replace(".log", ".txt"))
extract_energies(file_path, output_file)
if os.path.exists(output_file) and os.path.getsize(output_file) != 0:
    print(f"Successfully saved {output_file}")
else:
    print("Error in extraction! Please try again...")