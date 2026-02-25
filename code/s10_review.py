# count = 0
# for letter in 'mississippi':
#     if letter == 's':
#         count += 1
# print(count)



# count = 0
# for letter in 'babson college':
#     count += 1
# print(count)

# print(len('babson college'))

# n = 6
# while n > 0:
#     print(n)
#     n = n - 2

# n = 5
# while n != 0:
#     print(n)
#     n -= 2

# print('after while loop, n is', n)

# def uses_any(word, letters):
#     for letter in word:
#         if letter in letters:
#             return True
#     return False

# print(uses_any('hello', 'xyz'))

# print(uses_any('hello', 'aeiou'))

# def version_a(word):
#     for letter in word:
#         if letter in 'aeiou':
#             print(letter)
#     print('Done')

# def version_b(word):
#     for letter in word:
#         if letter in 'aeiou':
#             return letter
#     return 'None found'

# version_a('hello')
# print('---')
# print(version_b('hello'))

# version_a('nbc')
# print('---')
# print(version_b('nbc'))

import random

roll = 0
while roll != 6:
    roll = random.randint(1, 6)
    print('Rolled:', roll)
    if roll