import re
##################################################################
# reading trace from file
##################################################################


def traceParse(file_name):
    f = open(file_name, 'rU')
    instrList = re.findall(r'(\w+)\s(\w+)', f.read())
    f.close()
    return instrList
