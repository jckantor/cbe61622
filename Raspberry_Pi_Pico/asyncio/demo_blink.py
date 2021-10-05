import time

def blink(delay):
    time.sleep(delay)
    elapsed_time = time.time() - start
    print(f"Blink at {elapsed_time:6.2f}")

start = time.time()
def main():
    for k in range(5):
        blink(2)

main()
