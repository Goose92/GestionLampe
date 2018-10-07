# Fonction pour verifier si acces internet ok
def InternetOk():
    try :
        url = "https://www.google.com"
        urllib.urlopen(url)
        status = "Connected"
        return True
    except :
        status = "Not connect"
        return False
    # print status
