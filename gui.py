#!/usr/bin/python3
#
#



## THIS IS DESCRIPTOR FILE OF SYNTHESIZER
## Will be divided into several sections



################# SECTION 1 #################
######## To get how many virtual machines and the scenario ########

def secone():
        vms = input("Input how many vms: ")
        for each in range(int(vms)):
            print ("")


################# SECTION 2 #################
######## To set the first value of delay ########

def sectwo():
        print ("Input 4 values of delay: ")



################# MAIN FUNCTION #################
######## To get what function/section user has input to finish first ########

def get_input(inp):
	func = options.get(inp, "nothing")
	return func()

options = {"a":secone, "b":sectwo}

print ("This application can do: \n a. Define how much vm \n b. Define the first delay value")
inp = input('Your option: ')
get_input(inp)



