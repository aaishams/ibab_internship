import os
import re

def extract_connectivity(pdb_file):
    connectivity = {}
    with open(pdb_file, 'r') as file:
        conect = file.readlines()
    for line in conect:
        if "CONECT" in line:
            c = line.split()
            connectivity[c[1]] = c[2:]
    return connectivity

def check_atom_repeats(line):
    numbers = re.findall(r'\[(\d+)\]', line)
    repeat = set(numbers)
    if len(numbers) == len(repeat):
        return True
    else:
        return False
    
def bfs_bond_distance(connectivity, start, target, output_validation): # Breadth-First Search (BFS) algorithm for graphs
    if not isinstance(start, list):
        queue = [(start, 0)]
    else:
        queue = []
        for s in start:
            queue.append((s,0))
    visited = set() 
    while queue: 
        current, depth = queue.pop(0) 
        visited.add(current)
        if current in target: 
            with open(output_validation, "a") as out:
                out.writelines(f"{start} -> {target} = {depth} ({depth >=3})\n")
            return depth >= 3
        for neighbor in connectivity.get(current, []): 
            if neighbor not in visited: 
                queue.append((neighbor, depth + 1))
    return False

def check_bond_distance(connectivity, line, output_validation):
    numbers = re.findall(r'\[(\d+)\]', line)
    if 'n' in line and len(numbers) == 3:
        lone, atom1, atom2 = numbers[0], numbers[1], numbers[2]
        return bfs_bond_distance(connectivity, lone, [atom1, atom2], output_validation)
    if 'n' not in line and len(numbers) == 4:
        atom1, atom2, atom3, atom4 = numbers[0], numbers[1], numbers[2], numbers[3]
        return bfs_bond_distance(connectivity, [atom1, atom2], [atom3, atom4], output_validation)
    
def check_long_range(connectivity, interaction_energies, long_range_behavior, output_validation):
    with open(interaction_energies, 'r') as file:
        content = file.readlines()
    with open(long_range_behavior, 'w'):
        pass
    with open(output_validation, "w"):
        pass
    for line in content:
        if check_atom_repeats(line) and check_bond_distance(connectivity, line, output_validation):
            with open(long_range_behavior, 'a') as out:
                out.writelines(line)

file_path = input("Enter the file path: ").strip()
while not os.path.exists:
    print("Please enter a valid file path!")
    file_path = input("Enter the file path: ").strip()
connectivity = extract_connectivity(file_path)
print(connectivity)
interaction_energies = "ie_output_" + os.path.basename(file_path.replace(".pdb", ".txt"))
long_range_behavior = "lrb_output_2" + os.path.basename(file_path.replace(".pdb", ".txt"))
output_validation = "ov" + os.path.basename(file_path.replace(".pdb", ".txt"))
check_long_range(connectivity, interaction_energies, long_range_behavior, output_validation)
if os.path.exists(long_range_behavior) and os.path.getsize(long_range_behavior) != 0:
    print(f"Successfully saved {long_range_behavior}")
else:
    print("Error in extraction! Please try again...")
if os.path.exists(output_validation) and os.path.getsize(output_validation) != 0:
    print(f"Successfully saved {output_validation}")
else:
    print("Error in extraction! Please try again...")