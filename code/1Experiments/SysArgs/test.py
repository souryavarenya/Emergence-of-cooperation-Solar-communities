import sys

try:
    print(sys.argv[1])
except:
    print("Some Trouble")
    sys.exit()


if __name__ == '__main__':
    print("hello")
    for i in range(int(sys.argv[1])):
        print(i)

print("hi")