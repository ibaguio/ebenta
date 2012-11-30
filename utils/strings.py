#static data here

dormitory = ['None','Centennial','International Center','Ilang-ilang','Ipil','Kalayaan','Kamagong','Kamia','Molave','Sampaguita','Sanggumay','Yakal']
categories = [None , 'economics', 'engineering', 'english', 'filipino', 'finance', 'history', 'mathematics', 'science','other']
colleges = [None,'ncpag','cssp','arki','ait','cmc','fa','tmc','music','surp','upis','stat','asp','iis','econ','issi','educ','che','chk','slis','cs','cswcd','kal','cba','solair','law','engg','asian']


#returns the ordinal of a number
def ordinalth(n):
    if type(n) != long: return
    t = ['th','st','nd','rd','th','th','th','th','th','th']
    if n in (11, 12, 13):
        return '%dth' % n
    return str(n) + t[n % 10]