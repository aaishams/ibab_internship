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
    
def bfs_bond_distance(connectivity, start, target, flag): # Breadth-First Search (BFS) algorithm for graphs
    queue = [(start, 0)] # list to store atoms and the number of bonds (depth)
    visited = set() # initialize set to store visited atoms
    while queue: # process elements in queue until its empty
        current, depth = queue.pop(0) # current is the current atom (start); depth accounts for the number of bonds; pop(0) pops the 0th element of the list and assigns the value to the variable
        visited.add(current) # otherwise, the current atom is added to the visited set
        if current == target: # if the target atom is reached and depth >= 3, it returns true, else false
            if flag == 4:
                return depth >= 4
            if flag == 5:
                return depth >= 5  
        for neighbor in connectivity.get(current, []): # for getting the list of connected atoms of the current atom from connectivity data
            if neighbor not in visited: 
                queue.append((neighbor, depth + 1))
    return False #default return false

def check_bond_distance(connectivity, line):
    numbers = re.findall(r'\[(\d+)\]', line)
    if 'n' in line and len(numbers) == 3:
        lone, atom1, atom2 = numbers[0], numbers[1], numbers[2]
        return bfs_bond_distance(connectivity, lone, atom1, flag = 4) or bfs_bond_distance(connectivity, lone, atom2, flag = 4)
    if 'n' not in line and len(numbers) == 4:
        atom1, atom2, atom3, atom4 = numbers[0], numbers[1], numbers[2], numbers[3]
        return bfs_bond_distance(connectivity, atom1, atom3, flag = 5) or bfs_bond_distance(connectivity, atom1, atom4, flag = 5) or bfs_bond_distance(connectivity, atom2, atom3, flag = 5) or bfs_bond_distance(connectivity, atom2, atom4, flag = 5)

def check_long_range(connectivity, interaction_energies, long_range_behavior):
    with open(interaction_energies, 'r') as file:
        content = file.readlines()
    with open(long_range_behavior, 'w'):
        pass
    for line in content:
        if check_atom_repeats(line) and check_bond_distance(connectivity, line):
            with open(long_range_behavior, 'a') as out:
                out.writelines(line)

file_path = input("Enter the file path: ").strip()
while not os.path.exists:
    print("Please enter a valid file path!")
    file_path = input("Enter the file path: ").strip()
connectivity = extract_connectivity(file_path)
print(connectivity)
interaction_energies = "ie_output_" + os.path.basename(file_path.replace(".pdb", ".txt"))
long_range_behavior = "lrb_output_" + os.path.basename(file_path.replace(".pdb", ".txt"))
check_long_range(connectivity, interaction_energies, long_range_behavior)
if os.path.exists(long_range_behavior) and os.path.getsize(long_range_behavior) != 0:
    print(f"Successfully saved {long_range_behavior}")
else:
    print("Error in extraction! Please try again...")