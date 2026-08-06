#workshop 4/8/2026
requests = [
    ["Aisha", "Vegetarian hamper, prefers rice and lentils."],
    ["Ben", "Needs gluten-free items and baby formula."],
    ["Mira", "Halal food preferred, pickup after 4 pm."],
    ["Noah", "Low-sugar items requested; nut allergy."]
]
person = -2
print(f"{requests[person][0]}'s request says: {requests[person][1]}") #first brackets call the general list then goes into sub list items

"""
Alternate solution
second_last = requests[-2]
print(f"{second_last[0]}'s request says: {second_lasst[1]}) 
"""

requests[1] = ["Ravi", "Needs dairy-free hamper and baby formula."]
person2 = 1
print(f"{requests[person2][0]}'s request says: {requests[person2][1]}")

for request in requests:
    print(f"Foodshare pickup ready for {request[0]}!")

answer = ""
comments = []

while True:
    answer = input("Please enter any dietary or other comments, type x to quit: ")
    if answer != "x" and answer != "X":
        comments.append(answer)
    else:
        print(f"You have provided these conditions: {comments}")
        break

found = False
while True:
    name = input("Type your name here or press ctrl+c to exit program: ")
    for name_find, request in requests:
        if name_find.lower() == name.lower():
            print(f"{name}'s request says: {request}")
            found = True
            break
    if not found:
        print("Client request not found in the system")