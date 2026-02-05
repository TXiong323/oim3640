# for i in range(4):
    # print("Iteration:", i)
    # print("Square:", i * i)
    # print()

# def double(number):
    # """Return double the input number."""
    # return number * 2


# print(double(5))
# print(double('5'))


# a = 5
# b = a 
# a = 10
# print(b)
# print(a)


# a = [1, 2, 3]
# b = a
# a.append(4)
# print(b)
# print(a)


# x = 10

# def f():
    # message = 'hello'
    # x = 5
    # return message + str(x)

# print(f())
# print(x)
# print(message)

# Draw a square

# def draw_square(size):
    # for _ in range(4):
        # print("*" * size)

# draw_square(5)

# Draw a triangle

# def draw_triangle(size):
    # for i in range(size):
        # print("*" * (i + 1))

# draw_triangle(5)

# Draw a backward triangle

# def draw_backward_triangle(size):
    # for i in range(size):
        # print(" " * (size - i) + "*" * (i + 1))

# draw_backward_triangle(5)

# Draw a pyramid

def draw_pyramid(size):
    for i in range(size):
        print(" " * (size - i) + "*" * (2 * i + 1) + " " * (size - i))

draw_pyramid(5)