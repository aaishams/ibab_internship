# TO IMPORT PACKAGES
import re
import math

# TO EXTRACT COORDINATES
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

# TO CONVERT .log TO .xyz FILE FORMAT
def generate_xyz(coordinates, output_file):
    with open(output_file, 'w') as xyz:
        xyz.write(f"{len(coordinates)}\n")
        xyz.write(f"{output_file}\n")
        for atom_data in coordinates:
            atom, x, y, z = atom_data
            xyz.write(f"{atom}       {x:.5f}       {y:.5f}       {z:.5f}\n")
        xyz.write("END\n")

# TO EXTRACT CONNECTIVITY DATA
def connectivity(file_path1):
    connectivity = []
    with open(file_path1, 'r') as file:
        content = file.readlines()
    for line in content:
        if "CONECT" in line:
            c = line.split()
            connectivity.append((c[1:]))
    return connectivity

# TO CALCULATE BOND LENGTHS FROM CONNECTIVITY DATA
def bond_length(conect, coordinates):
    bond_lengths = {}
    dont_repeat = []
    for i in conect:
        atom_number1 = int(i[0]) - 1
        atom_symbol1 = coordinates[atom_number1][0]
        x1, y1, z1 = coordinates[atom_number1][1:]
        for j in i[1:]:
            atom_number2 = int(j) - 1
            atom_symbol2 = coordinates[atom_number2][0]
            x2, y2, z2 = coordinates[atom_number2][1:]
            if sorted([atom_number1, atom_number2]) not in dont_repeat:
                bond_length = math.sqrt((x2 - x1)**2 + (y2 - y1)**2 + (z2 - z1)**2)
                bond_lengths[f"{atom_symbol1}[{atom_number1 + 1}]-{atom_symbol2}[{atom_number2 + 1}]"] = round(bond_length, 5)
                dont_repeat.append(sorted([atom_number1, atom_number2]))
    return bond_lengths

# TO CALCULATE BOND ANGLES FROM CONNECTIVITY DATA
def bond_angle(angle_conect, coordinates):
    bond_angles = {}
    for i in angle_conect:
        mid_atom_number = int(i[0]) - 1
        mid_atom_symbol = coordinates[mid_atom_number][0]
        x1, y1, z1 = coordinates[mid_atom_number][1:]
        dont_repeat = []
        for j in i[1:]:
            atom_number1 = int(j) - 1
            atom_symbol1 = coordinates[atom_number1][0]
            x2, y2, z2 = coordinates[atom_number1][1:]
            for k in i[1:]:
                atom_number2 = int(k) - 1
                atom_symbol2 = coordinates[atom_number2][0]
                x3, y3, z3 = coordinates[atom_number2][1:]
                if atom_number1 != atom_number2:
                    if sorted([atom_number1, atom_number2]) not in dont_repeat:
                        vec1 = (x2 - x1, y2 - y1, z2 - z1)
                        vec2 = (x3 - x1, y3 - y1, z3 - z1)
                        dot_product = vec1[0]*vec2[0] + vec1[1]*vec2[1] + vec1[2]*vec2[2]
                        mag1 = math.sqrt(vec1[0]**2 + vec1[1]**2 + vec1[2]**2)
                        mag2 = math.sqrt(vec2[0]**2 + vec2[1]**2 + vec2[2]**2)
                        cos_angle = dot_product / (mag1 * mag2)
                        bond_angle = math.degrees(math.acos(cos_angle))
                        bond_angles[f"{atom_symbol1}[{atom_number1 + 1}]-{mid_atom_symbol}[{mid_atom_number + 1}]-{atom_symbol2}[{atom_number2 + 1}]"] = round(bond_angle, 5)
                        dont_repeat.append(sorted([atom_number1, atom_number2]))
    return bond_angles

# TO CALCULATE DIHEDRAL ANGLES FROM CONNECTIVITY DATA
def dihedral_angle(plane_conect, coordinates):
    dont_repeat1 = []
    dihedral_angles = {}
    for atm in plane_conect:
        for i in atm:
            atom_number1 = int(i) - 1 
            x1, y1, z1 = map(float, coordinates[atom_number1][1:])
            atom_symbol1 = coordinates[atom_number1][0]
            for j in atm:
                atom_number2 = int(j) - 1
                x2, y2, z2 = map(float, coordinates[atom_number2][1:])
                atom_symbol2 = coordinates[atom_number2][0]
                for k in atm:
                    atom_number3 = int(k) - 1
                    x3, y3, z3 = map(float, coordinates[atom_number3][1:])
                    atom_symbol3 = coordinates[atom_number3][0]
                    for l in atm:
                        atom_number4 = int(l) - 1
                        x4, y4, z4 = map(float, coordinates[atom_number4][1:])
                        atom_symbol4 = coordinates[atom_number4][0]
                        if len(set([atom_number1, atom_number2, atom_number3, atom_number4])) == 4:
                            if f"{atom_symbol1}[{atom_number1+1}] - {atom_symbol2}[{atom_number2+1}] - {atom_symbol3}[{atom_number3+1}] - {atom_symbol4}[{atom_number4+1}]" and f"{atom_symbol4}[{atom_number4+1}] - {atom_symbol3}[{atom_number3+1}] - {atom_symbol2}[{atom_number2+1}] - {atom_symbol1}[{atom_number1+1}]" not in dont_repeat1:
                                vec12 = (x2 - x1, y2 - y1, z2 - z1)
                                vec23 = (x3 - x2, y3 - y2, z3 - z2)
                                vec34 = (x4 - x3, y4 - y3, z4 - z3)
                                n123 = [vec12[1]*vec23[2] - vec12[2]*vec23[1], vec12[2]*vec23[0] - vec12[0]*vec23[2], vec12[0]*vec23[1] - vec12[1]*vec23[0]]
                                n234 = [vec23[1]*vec34[2] - vec23[2]*vec34[1], vec23[2]*vec34[0] - vec23[0]*vec34[2], vec23[0]*vec34[1] - vec23[1]*vec34[0]]
                                dot_pdt = n123[0]*n234[0] + n123[1]*n234[1] + n123[2]*n234[2]
                                mag123 = math.sqrt(n123[0]**2 + n123[1]**2 + n123[2]**2)
                                mag234 = math.sqrt(n234[0]**2 + n234[1]**2 + n234[2]**2)
                                cos_phi = dot_pdt / (mag123 * mag234)
                                dihedral_angle = math.degrees(math.acos(cos_phi))
                                dont_repeat1.append(f"{atom_symbol1}[{atom_number1+1}] - {atom_symbol2}[{atom_number2+1}] - {atom_symbol3}[{atom_number3+1}] - {atom_symbol4}[{atom_number4+1}]")
                                dihedral_angles[f"{atom_symbol1}[{atom_number1+1}] - {atom_symbol2}[{atom_number2+1}] - {atom_symbol3}[{atom_number3+1}] - {atom_symbol4}[{atom_number4+1}]"] = round(dihedral_angle, 5)
    return dihedral_angles 

# TO COMPARE THE CONFORMERS
def compare(conformer1, conformer2, conformers):
    if conformer1 not in conformers or  conformer2 not in conformers:
        print("One or both conformers not available!!")
        return
    properties1 = conformers[conformer1]
    print(properties1)
    properties2 = conformers[conformer2]
    print(properties2)
    print("Differentiating between bond lengths:-")
    bl1 = properties1['BOND LENGTHS']
    bl2 = properties2['BOND LENGTHS']
    common_bonds = set(bl1.keys()).intersection(set(bl2.keys()))
    for bond in common_bonds:
        if bl1[bond] != bl2[bond]:
            print(f"{bl1[bond]} - {bl2[bond]} = {bl1[bond] - bl2[bond]}")
        else:
            print(f"{bl1[bond]} and {bl2[bond]} are equal in length!!")
    print("Differentiating between bond angles:-")
    ba1 = properties1['BOND ANGLES']
    ba2 = properties2['BOND ANGLES']
    common_angles = set(ba1.keys()).intersection(set(ba2.keys()))
    for angle in common_angles:
        if ba1[angle] != ba2[angle]:
            print(f"{ba1[angle]} - {ba2[angle]} = {ba1[angle] - ba2[angle]}")
        else:
            print(f"{ba1[angle]} and {ba2[angle]} have the same angle!!")

# BASE CODE
log_files = [r"\CN_N1.log", r"\CN_N2.log", r"\CN_P1.log", r"\CN_P2.log"]
for f in log_files:
    file_path = r"DATA_FROM_JN" + f
    coordinates = extract_coordinates(file_path)
    output_file = r"DATA_FROM_JN" + f.replace('.log', '.xyz')            
    generate_xyz(coordinates, output_file)
    print(f"Succesfully saved '{output_file}'")  
    pdb_files = [r"\CN_N1.pdb", r"\CN_N2.pdb", r"\CN_P1.pdb", r"\CN_P2.pdb"] #after converting XYZ files to PDB files on Open Babel
conformers = {}
for f1 in pdb_files:
    file_path1 = r"DATA_FROM_JN" + f1
    f1 = f1.replace(".pdb", "").replace("\\", "")
    print("Connectivity data of", f1)
    conect = connectivity(file_path1)
    angle_conect = []
    plane_conect = []
    for i in conect:
        if len(i) > 2:
            angle_conect.append(i)
            if len(i)>3:
                plane_conect.append(i)
    conformers[f1] = {}
    print(conformers)
    bond_lengths = bond_length(conect, coordinates)
    conformers[f1]['BOND LENGTHS'] = bond_lengths
    print(f"BOND LENGTHS in the conformer '{f1}':\n{bond_lengths}")
    print("---------------------------------------------------------------------")
    bond_angles = bond_angle(angle_conect, coordinates)
    conformers[f1]['BOND ANGLES'] = bond_angles
    print(f"BOND ANGLES in the conformer '{f1}':\n{bond_angles}")
    print("---------------------------------------------------------------------")
    dihedral_angles = dihedral_angle(plane_conect, coordinates)
    conformers[f1]['DIHEDRAL ANGLES'] = dihedral_angles
    print(f"DIHEDRAL ANGLES in the conformer '{f1}':\n{dihedral_angles}")
    print("---------------------------------------------------------------------")
    print("To differentiate between 2 conformers:-")

c1 = str(input("Enter the first conformer:"))
c2 = str(input("Enter the second conformer:"))
comparison = compare(c1, c2, conformers)