import csv

with open(
    "example.csv",  
    "w",                # Creates or overwrites the file
    newline="",         # Allows the CSV module to manage line endings correctly
    encoding="utf-8"    # Specifies the text encoding
) as file:

    writer = csv.writer(file)

    writer.writerow(["id", "name", "course"])

    writer.writerow([1, "Amy Jones", "Computing"])
    writer.writerow([2, "John Smith", "Media"])