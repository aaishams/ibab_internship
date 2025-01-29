import re
import math
import os

def extract_coordinates(file_path):
    coordinates = []
    with open(file_path, 'r') as file:
        content = file.readlines()
    start_pattern = re.compile("Charge =  0 Multiplicity = 1")
    end_pattern = re.compile("  ")
    inside_section = False
    for line in content:
        if start_pattern.search(line):
            inside_section = True
            continue
        if inside_section and end_pattern.match(line):
            break
        if inside_section:
            c = line.split()
            if len(c) == 4:
                atom = str(c[0])
                x, y, z = float(c[1]), float(c[2]), float(c[3])
                coordinates.append((atom, x, y, z))
    return coordinates

def convert_to_xyz(file_path, coordinates):
    output_file = file_path.replace('.log', '.xyz')
    with open(output_file, 'w') as xyz:
        xyz.write(f"{len(coordinates)}\n")
        xyz.write(f"{output_file}\n")
        for atom_data in coordinates:
            atom, x, y, z = atom_data
            xyz.write(f"{atom}       {x:.5f}       {y:.5f}       {z:.5f}\n")
        xyz.write("END\n")
    print(f"Successfully created '{output_file}'.")

def extract_connectivity(pdb_file):
    connectivity = {}
    with open(pdb_file, 'r') as file:
        conect = file.readlines()
    for line in conect:
        if "CONECT" in line:
            c = line.split()
            connectivity[c[1]] = c[2:]
    return connectivity

#here, get() function searches for atom1 (key) in connectivity (dictionary) and returns its values as a list in [], then, atom2 (value) is searched in that list 
def check_length_connectivity(atom1, atom2, connectivity):
    return atom2 in connectivity.get(atom1, []) 

def check_angle_connectivity(atom2, atom1, atom3, connectivity):
    return atom1 in connectivity.get(atom2, []) and atom3 in connectivity.get(atom2, [])

def bond_length(atom1, atom2, coordinates):
    x1, y1, z1 = map(float, coordinates[atom1 - 1][1:])
    x2, y2, z2 = map(float, coordinates[atom2 - 1][1:])
    return math.sqrt((x2 - x1)**2 + (y2 - y1)**2 + (z2 - z1)**2)

def bond_angle(atom2, atom1, atom3, coordinates):
    x1, y1, z1 = map(float, coordinates[atom1 - 1][1:])
    x2, y2, z2 = map(float, coordinates[atom2 - 1][1:])
    x3, y3, z3 = map(float, coordinates[atom3 - 1][1:])
    vec21 = (x1 - x2, y1 - y2, z1 - z2)
    vec23 = (x3 - x2, y3 - y2, z3 - z2)
    dot_product = vec21[0]*vec23[0] + vec21[1]*vec23[1] + vec21[2]*vec23[2]
    mag1 = math.sqrt(vec21[0]**2 + vec21[1]**2 + vec21[2]**2)
    mag2 = math.sqrt(vec23[0]**2 + vec23[1]**2 + vec23[2]**2)
    cos_theta = dot_product / (mag1 * mag2)
    return math.degrees(math.acos(cos_theta))

def dihedral_angle(atom1, atom2, atom3, atom4, coordinates):
    x1, y1, z1 = map(float, coordinates[atom1 - 1][1:])
    x2, y2, z2 = map(float, coordinates[atom2 - 1][1:])
    x3, y3, z3 = map(float, coordinates[atom3 - 1][1:])
    x4, y4, z4 = map(float, coordinates[atom4 - 1][1:])
    vec12 = (x1 - x2, y1 - y2, z1 - z2)
    vec32 = (x3 - x2, y3 - y2, z3 - z2)
    vec23 = (x2 - x3, y2 - y3, z2 - z3)
    vec43 = (x4 - x3, y4 - y3, z4 - z3)
    n123 = [vec12[1]*vec32[2] - vec12[2]*vec32[1], vec12[2]*vec32[0] - vec12[0]*vec32[2], vec12[0]*vec32[1] - vec12[1]*vec32[0]]
    n234 = [vec23[1]*vec43[2] - vec23[2]*vec43[1], vec23[2]*vec43[0] - vec23[0]*vec43[2], vec23[0]*vec43[1] - vec23[1]*vec43[0]]
    dot_pdt = n123[0]*n234[0] + n123[1]*n234[1] + n123[2]*n234[2]
    mag123 = math.sqrt(n123[0]**2 + n123[1]**2 + n123[2]**2)
    mag234 = math.sqrt(n234[0]**2 + n234[1]**2 + n234[2]**2)
    cross_pdt = [n123[1]*n234[2] - n123[2]*n234[1], n123[2]*n234[0] - n123[0]*n234[2], n123[0]*n234[1] - n123[1]*n234[0]]
    dihedral_angle = math.acos(dot_pdt / (mag123 * mag234))
    if cross_pdt[2] > 0: # cross_pdt[2] is the z-component; > 0 => clockwise => -ve dihedral angle, < 0 => anticlockwise => +ve dihedral angle
        dihedral_angle = -dihedral_angle
    return math.degrees(dihedral_angle)

print("Hello!")
file_path = input("Enter the file path: ").strip()
if not os.path.exists(file_path):
    print("ERROR IN INPUT! PLEASE ENTER A VALID FILE PATH..")
    file_path = input("Enter the file path: ").strip()
coordinates = extract_coordinates(file_path)
print(f"Coordinates of the conformer: {coordinates}")
convert_to_xyz(file_path, coordinates)
pdb_file = file_path.replace(".log", ".pdb")
connectivity = extract_connectivity(pdb_file)
print(f"Connectivity of the conformer: {connectivity}")
answer = int(input("Enter 1 to continue and find the properties or 0 to exit: "))
while answer == 1:
    property = int(input("Enter 1 for finding bond length, 2 for bond angle, 3 for dihedral angle and 4 to compare between two conformers: "))
    if property == 1: #bond length
        atom1, atom2 = int(input("Enter the first atom: ")), int(input("Enter the second atom: "))
        if atom1 > len(coordinates) or atom2 > len(coordinates) or len(set([atom1, atom2])) != 2:
            print(f"ERROR IN INPUT! PLEASE TRY AGAIN..")
        elif check_length_connectivity(str(atom1), str(atom2), connectivity):
            bl = bond_length(atom1, atom2, coordinates)
            print(f"The bond length between {coordinates[atom1 - 1][0]}[{atom1}] and {coordinates[atom2 - 1][0]}[{atom2}] is {round(bl, 2)}Å.")
        else:
            print(f"{coordinates[atom1 - 1][0]}[{atom1}] and {coordinates[atom2 - 2][0]}[{atom2}] are not connected.")
    elif property == 2: #bond angle
        atom1, atom2, atom3 = int(input("Enter the first atom: ")), int(input("Enter the second atom: ")), int(input("Enter the third atom: "))
        if atom1 > len(coordinates) or atom2 > len(coordinates) or atom3 > len(coordinates) or len(set([atom1, atom2, atom3])) != 3:
            print(f"ERROR IN INPUT! PLEASE TRY AGAIN..")
        elif check_angle_connectivity(str(atom2), str(atom1), str(atom3), connectivity):
            ba = bond_angle(atom2, atom1, atom3, coordinates)
            print(f"The bond angle formed by {coordinates[atom1 - 1][0]}[{atom1}], {coordinates[atom2 - 1][0]}[{atom2}] and {coordinates[atom3 - 1][0]}[{atom3}] is {round(ba, 1)}°.")
        else:
            print(f"{coordinates[atom1 - 1][0]}[{atom1}] or/and {coordinates[atom3 - 1][0]}[{atom2}] is/are not connected to {coordinates[atom2 - 1][0]}[{atom3}].")
    elif property == 3: #dihedral angle
        atom1, atom2, atom3, atom4 = int(input("Enter the first atom: ")), int(input("Enter the second atom: ")), int(input("Enter the third atom: ")), int(input("Enter the fourth atom: "))
        if atom1 > len(coordinates) or atom2 > len(coordinates) or atom3 > len(coordinates) or atom4 > len(coordinates) or len(set([atom1, atom2, atom3, atom4])) != 4:
            print(f"ERROR IN INPUT! PLEASE TRY AGAIN..")
        else: 
            da = dihedral_angle(atom1, atom2, atom3, atom4, coordinates)
            print(f"The dihedral angle formed by {coordinates[atom1 - 1][0]}[{atom1}], {coordinates[atom2 - 1][0]}[{atom2}], {coordinates[atom3 - 1][0]}[{atom3}] and {coordinates[atom4 - 1][0]}[{atom4}] is {round(da)}°.")
    elif property == 4: #comparison
        file_path2 = input("Enter the file path: ").strip()
        if not os.path.exists(file_path2):
            print("ERROR IN INPUT! PLEASE ENTER A VALID FILE PATH..")
            file_path2 = input("Enter the file path: ").strip()
        elif file_path == file_path2:
            print("YOU ENTERED THE SAME FILE PATH AS BEFORE!! PLEASE TRY AGAIN TO COMPARE..")
            file_path2 = input("Enter the file path: ").strip()
        coordinates2 = extract_coordinates(file_path2)
        print(f"COORDINATES OF THE CONFORMER: {coordinates2}")
        convert_to_xyz(file_path2, coordinates2)
        pdb_file2 = file_path2.replace(".log", ".pdb")
        connectivity2 = extract_connectivity(pdb_file2)
        print(f"CONNECTIVITY DATA OF THE CONFORMER: {connectivity2}")
        property2 = int(input("Enter 1 for finding bond length, 2 for bond angle and 3 for dihedral angle: "))
        if property2 == 1: #compare bond length
            atom1, atom2 = int(input("Enter the first atom: ")), int(input("Enter the second atom: "))
            if atom1 > len(coordinates) or atom2 > len(coordinates) or atom1 > len(coordinates2) or atom2 > len(coordinates2) or len(set([atom1, atom2])) !=2:
                print(f"ERROR IN INPUT! PLEASE TRY AGAIN..")
            elif check_length_connectivity(str(atom1), str(atom2), connectivity) and check_length_connectivity(str(atom1), str(atom2), connectivity2):
                bl = bond_length(atom1, atom2, coordinates)
                bl2 = bond_length(atom1, atom2, coordinates2)
                print(f"The bond length between {coordinates[atom1 - 1][0]}[{atom1}] and {coordinates[atom2 - 1][0]}[{atom2}] of conformer 1 is {round(bl, 2)}Å.")
                print(f"The bond length between {coordinates2[atom1 - 1][0]}[{atom1}] and {coordinates2[atom2 - 1][0]}[{atom2}] of conformer 2 is {round(bl2, 2)}Å.")
                print(f"Difference in bond length between the two conformers = {round(abs(bl - bl2), 2)}Å")
            else:
                print(f"{coordinates2[atom1 - 1][0]}[{atom1}] and {coordinates2[atom2 - 2][0]}[{atom2}] are not connected in one or both of the conformers.")
        elif property2 == 2: #compare bond angle
            atom1, atom2, atom3 = int(input("Enter the first atom: ")), int(input("Enter the second atom: ")), int(input("Enter the third atom: "))
            if atom1 > len(coordinates) or atom2 > len(coordinates) or atom3 > len(coordinates) or atom1 > len(coordinates2) or atom2 > len(coordinates2) or atom3 > len(coordinates2) or len(set([atom1, atom2, atom3])) != 3:
                print(f"ERROR IN INPUT! Atom {atom1} or atom {atom2} or atom {atom3} or a few of them not in one or both of the conformer. PLEASE TRY AGAIN..")
            elif check_angle_connectivity(str(atom2), str(atom1), str(atom3), connectivity) and check_angle_connectivity(str(atom2), str(atom1), str(atom3), connectivity2):
                ba = bond_angle(atom2, atom1, atom3, coordinates)
                ba2 = bond_angle(atom2, atom1, atom3, coordinates2)
                print(f"The bond angle formed by {coordinates[atom1 - 1][0]}[{atom1}], {coordinates[atom2 - 1][0]}[{atom2}] and {coordinates[atom3 - 1][0]}[{atom3}] of conformer 1 is {round(ba, 1)}°.")
                print(f"The bond angle formed by {coordinates2[atom1 - 1][0]}[{atom1}], {coordinates2[atom2 - 1][0]}[{atom2}] and {coordinates2[atom3 - 1][0]}[{atom3}] of conformer 2 is {round(ba2, 1)}°.")
                print(f"Difference in bond angle between the two conformers = {round(abs(ba - ba2), 1)}°")
            else:
                print(f"{coordinates2[atom1 - 1][0]}[{atom1}] and {coordinates2[atom3 - 1][0]}[{atom2}] are not connected to {coordinates2[atom2 - 1][0]}[{atom3}] in one or both of the conformers.")
        elif property2 == 3: #compare dihedral angle
            atom1, atom2, atom3, atom4 = int(input("Enter the first atom: ")), int(input("Enter the second atom: ")), int(input("Enter the third atom: ")), int(input("Enter the fourth atom: "))
            if atom1 > len(coordinates) or atom2 > len(coordinates) or atom3 > len(coordinates) or atom4 > len(coordinates) or atom1 > len(coordinates2) or atom2 > len(coordinates) or atom3 > len(coordinates) or atom4 > len(coordinates2) or len(set([atom1, atom2, atom3, atom4])) !=4:
                print(f"ERROR IN INPUT! Atom {atom1} or atom {atom2} or atom {atom3} or atom {atom4} or a few of them not in one or both of the conformer. PLEASE TRY AGAIN..")
            else: 
                da = dihedral_angle(atom1, atom2, atom3, atom4, coordinates)
                da2 = dihedral_angle(atom1, atom2, atom3, atom4, coordinates2)
                print(f"The dihedral angle formed by {coordinates[atom1 - 1][0]}[{atom1}], {coordinates[atom2 - 1][0]}[{atom2}], {coordinates[atom3 - 1][0]}[{atom3}] and {coordinates[atom4 - 1][0]}[{atom4}] of conformer 1 is {round(da)}°.")
                print(f"The dihedral angle formed by {coordinates2[atom1 - 1][0]}[{atom1}], {coordinates2[atom2 - 1][0]}[{atom2}], {coordinates2[atom3 - 1][0]}[{atom3}] and {coordinates2[atom4 - 1][0]}[{atom4}] of conformer 2 is {round(da2)}°.")
                print(f"Difference in dihedral angle between the two conformers = {round(abs(da - da2))}°")
        else:
            print("ERROR IN INPUT! DO YOU WANT TO EXIT?")
    else:
        print("ERROR IN INPUT! DO YOU WANT TO EXIT??")
    answer = int(input("Enter 1 to continue and find the properties or 0 to exit: "))
print("Thankyou for using this tool! Have a nice day..")