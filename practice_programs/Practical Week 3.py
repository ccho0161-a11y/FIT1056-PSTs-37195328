def greet(part_day, salutation, last_name):
    part_day = input("What time of day is it (morning, afternoon, evening)? ")
    salutation = input("What title do you have? ")
    last_name = input("What is your surname? ")
    print(f"Good {part_day}, {salutation} {last_name}!")

def exercise2(num1, num2):
    """Determines whether a number is divisible by the second number"""
    if num1 % num2 == 0:
        print(str(num1) + " is divisible by " + str(num2) + "!")
        return True
    else:
        print(str(num1) + " is not divisible by " + str(num2) + " :(")
        return False
def convert_celsius_to_farenheit(celsius):
    """Converts celsius input to farenheit"""
    farenheit = (celsius * 9/5) + 32 
    print(f"{celsius}°C is {farenheit}°F")
temp = int(input("What temperature in celcius would you like to convert? "))
convert_celsius_to_farenheit(temp)