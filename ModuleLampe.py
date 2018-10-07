# Une fonction pour allumer la lampe
def AllumerLampe(NumPort):
	GPIO.output(NumPort, True)

# Une fonction pour éteindre la lampe
def EteindreLampe(NumPort):
        GPIO.output(NumPort, False)
