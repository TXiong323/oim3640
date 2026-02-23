# score = int(input("Enter your score: "))

# if score >= 60:
    # print("Congratulations! You passed the exam.")
# elif score >= 90:
    # print("Congratulations! You got an A grade.")
# else:
    # print("Sorry, you failed the exam. Better luck next time!")

# if score >= 90:
#     print("Congratulations! You got an A grade.")
# elif score >= 60:
#     print("Congratulations! You passed the exam.")
# else:
#     print("Sorry, you failed the exam. Better luck next time!")

# def evaluate_score(score):
#     if score >= 90:
#         return "Congratulations! You got an A grade."
#     elif score >= 60:
#         return "Congratulations! You passed the exam."
#     else:
#         return "Sorry, you failed the exam. Better luck next time!"

# score = int(input("Enter your score: "))
# result = evaluate_score(score)
# print(result)

# def mystery(x):
#     if x > 0:
#         print("done")
#         return "positive"
#     else:
#         print("done")
#         return "non-positive"

# result = mystery(5)
# print(result)

x = 15
y = x > 10 or x< 2
print(type(y))
print(y)

def is_leap_year(year):
    return (year % 4 == 0 and year % 100 != 0) or (year % 400 == 0)
year = int(input("Enter a year: "))
if is_leap_year(year):
    print(f"{year} is a leap year.")
else:    print(f"{year} is not a leap year.")  

is_leap_year(2020)

def check(n):
    if n % 2 == 0:
        if n % 3 == 0:
            print("A")
        else:
            print("B")
    else:
        print("C")

check(8)
check(6)



