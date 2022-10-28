import re

import pyodbc

# We had this argument in class that you can't use surnames to accurately tell what children does one
# parent have from just the names of the parents (parents table in access) and the names of the children (children table in access)
# So I decided to try to solve it on my own
# There are exceptions but this script will filter around 95% names correctly (It is definitely possible to reach 100%)

conn = pyodbc.connect(
    r"Driver={Microsoft Access Driver (*.mdb, *.accdb)};DBQ=C:\\Users\\vojta\\OneDrive\\Plocha\\pyprojects\\check_children_of_parent_by_surname\\Children_parents.accdb"  # path to the access database
)
cursor = conn.cursor()
cursor.execute("select surname, name from parents")
parents = cursor.fetchall()

cursor.execute("select surname, name from children")
children = cursor.fetchall()
children_lst = []

for child in children:
    # output of the fetch all is a list of tuples so you have to use double for loop
    for ch in child:
        if ch is not None:
            children_lst.append(ch)
dict_children = {
    children_lst[i]: children_lst[i + 1] for i in range(0, len(children_lst), 2)
}
print(dict_children)
for parent_row in parents:
    if parent_row[0] is not None:
        rare_exception = parent_row[0].find("e")
        men_to_women_surname = re.compile(
            rf"{parent_row[0][:-1]}(ová|á)|{parent_row[0][:rare_exception]}{parent_row[0][rare_exception + 1:]}(ová)"
        )
        res = re.search(men_to_women_surname, " ".join(children_lst))
        if res is None:
            if parent_row[0][-4] == "k" and "ová" in parent_row[0]:
                rare_exception = parent_row[0][:-4] + "e" + parent_row[0][-4]
            women_to_men_surname = re.compile(
                rf"{parent_row[0][:-3]}a|{parent_row[0][:-1]}ý|{parent_row}|{rare_exception}"
            )
            res = re.search(women_to_men_surname, " ".join(children_lst))
            if res is None:
                print(parent_row)
            else:
                print(
                    parent_row[1]
                    + " "
                    + parent_row[0]
                    + " is parent to "
                    + dict_children[res.group(0)]
                    + " "
                    + res.group(0)
                )
        else:
            print(
                parent_row[1]
                + " "
                + parent_row[0]
                + " is parent to "
                + dict_children[res.group(0)]
                + " "
                + res.group(0)
            )
