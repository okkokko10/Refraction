def AsINT(argument):
    try:
        return int(argument)
    except:
        return


a=AsINT('1.2')
print(a)