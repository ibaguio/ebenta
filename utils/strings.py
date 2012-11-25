#static data here

dormitory = ['None','Centennial','International Center','Ilang-ilang','Ipil','Kalayaan','Kamagong','Kamia','Molave','Sampaguita','Sanggumay','Yakal']

#returns the ordinal of a number
def ordinalth(n):
    if type(n) != long: return
    t = ['th','st','nd','rd','th','th','th','th','th','th']
    if n in (11, 12, 13):
        return '%dth' % n
    return str(n) + t[n % 10]