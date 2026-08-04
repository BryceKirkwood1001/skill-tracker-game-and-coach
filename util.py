def strInput(prompt): # Handles user string input
    while True:
        strIn = str(input(prompt)).strip()
        if strIn:
            return strIn
        else:
            print("Input cannot be empty")
        
def intInput(prompt, allowZero): # Handles user int input
    while True:
        try:
            intIn = int(input(prompt))
        except ValueError:
            print("Invalid input, please try again")
        else:
            if allowZero == False and intIn == 0:
                print("Invalid input, please try again")
            elif intIn < 0:
                print("Invalid input, please try again")
            else:
                return intIn