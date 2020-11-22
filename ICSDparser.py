###
# Required Packages:
# pip install pandas
# pip install PyCifRW
####
import pandas as pd
import CifFile
import os

# set directories (map to file location)
os.chdir("C://Users/kmart/Desktop/Database Project")
file_list = os.listdir("./ICSD_111")

# define columns for dictionary (serves as a temp storage before csv dump)
# change properties here as "name of property": "corresponding .cif file term")
DATA_TYPE = {
    "systematic name": "_chemical_name_systematic",
    "structural formula": "_chemical_name_structure_type",
    "name structure type": "_chemical_formula_structural",
    "crystal density": "_exptl_crystal_density_diffrn",
    "cell length a": "_cell_length_a",
    "cell length b": "_cell_length_b",
    "cell length c": "_cell_length_c",
    "cell angle alpha": "_cell_angle_alpha",
    "cell angle beta": "_cell_angle_beta",
    "cell angle gamma": "_cell_angle_gamma",
    "cell volume": "_cell_volume",
    "cell formula units": "_cell_formula_units_Z",
    "symmetry space group name": "_symmetry_space_group_name_H-M",
    "symmetry equiv space id": "_symmetry_equiv_pos_site_id"}


# read file function
#will need to map to file once more in try portion
def read_file(file):
    try:
        readable = CifFile.ReadCif("./ICSD_111/" + file)
    except:
        readable = False
        print("Error reading" + file)
    return readable


# obtain and store data function

def main():
    df = pd.DataFrame(columns=DATA_TYPE)
    df["file number"] = ''
    for file in file_list:
        temp_dict = DATA_TYPE.copy()
        if read_file(file):

            i = read_file(file)
            cb = (i.first_block())

            for key in DATA_TYPE:
                try:
                    x = (cb[DATA_TYPE[key]])
                    temp_dict.update({key: x})
                except:
                    pass
            temp_dict.update({"file number": file})
            df = df.append(temp_dict, ignore_index=True)
        else:
            # update file with blank value
            df = df.append({'file number': file}, ignore_index=True)
            print("Error parsing data" + file)
    df.to_csv("./ICSDdata.csv")  # export to csv function


main()
