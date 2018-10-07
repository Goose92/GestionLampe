# Une fonction pour indiquer le numero du jour dans l'année
def numjouran(d):
    """Donne le numéro du jour dans l'année de la date d=[j,m,a] (1er janvier = 1, ...)"""
    j, m, a = d
    if ((a%4==0 and a%100!=0) or a%400==0):  # bissextile?
        return (0,31,60,91,121,152,182,213,244,274,305,335,366)[m-1] + j
    else:
        return (0,31,59,90,120,151,181,212,243,273,304,334,365)[m-1] + j
