testdata = 'Group 1: Gondola Operator, Non-Gondola Operator, Operative, Gondolayan Marksman \n Group 2: Monorail Operator, Monorail Spotter'


def parser(data):
    datalist = data.split(" ")
    temp = ""
    grouplist = []
    roledict = {}
    for i in datalist:
        temp = temp + f'{i} '
        if ':' in i:
            temp = temp.rstrip(temp[-1])
            temp = temp.rstrip(temp[-1])
            grouplist.append(temp)
            temp = ""
        if ',' in i:
            temp = temp.rstrip(temp[-1])
            temp = temp.rstrip(temp[-1])
            roledict.update({temp : grouplist[len(grouplist) - 1]})
            temp = ""
        if '.' in i:
            temp = temp.rstrip(temp[-1])
            temp = temp.rstrip(temp[-1])
            roledict.update({temp : grouplist[len(grouplist) - 1]})
            temp = ""
        if '\n' in i:
            if temp != "":
                temp = temp.rstrip(temp[-1])
                temp = temp.rstrip(temp[-1])
                roledict.update({temp : grouplist[len(grouplist) - 1]})
                temp = ""
    if temp != "":
        temp = temp.rstrip(temp[-1])
        roledict.update({temp : grouplist[len(grouplist) - 1]})
        temp = ""
    return grouplist, roledict

print(parser(testdata))

