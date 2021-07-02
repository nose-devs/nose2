import time

# statement run at import time should be covered
foo = 1

with open("/tmp/showme", "a") as f:
    f.write("\n\nbeta" + str(time.time()))


raise SystemExit


# so should an ordinary function body
def func():
    return 2
