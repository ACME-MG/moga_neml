# Libraries
import os

# Get CSV files and iterate through them
csv_files = [file for file in os.listdir() if file.endswith(".csv")]
for csv_file in csv_files:
    with open(csv_file, "r") as file:
        headers = file.readline().replace("\n","") + ",youngs,poissons\n"
        first_line = file.readline().replace("\n","") + ",157000,0.3\n"
        other_lines = [line.replace("\n","") + ",,,\n" for line in file.readlines()]
    with open(csv_file, "w+") as file:
        file.write(headers)
        file.write(first_line)
        for line in other_lines:
            file.write(line)