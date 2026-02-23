# for i in range(5):
    # print(i)
    # i += 1

# break - exit the loop immediately
# words = ["hello", "world", "target", "python"]
# for word in words:
    # print('checking:', word)
    # if word == "target":
        # print("Found it!")
        # break
    
# words = ["hello", "world", "target", "python"]
# for word in words:
    # print('checking:', word)
    # if word == "target":
    #     print("Found it!\n")
    #     continue
    # print("Not the target.\n")

    # continue - skip to the next iteration
# for num in range(10):
        # if num % 2 == 0:
            # continue
        # print(num)

for line in open("data/words.txt"):
    print(line.strip())