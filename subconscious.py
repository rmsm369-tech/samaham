import threading
import time
from pi_engine import ramanujan_pi, save_pi_digits

def subconscious_loop():
    while True:
        # FIX: Everything inside the loop is now indented by 4 spaces
        print("Subconscious: reviewing memories...")
        pi = ramanujan_pi(10)
        save_pi_digits(pi)
        print("Pi state updated ✓")
        
        # Sleeps for 1 hour (3600 seconds) before running again
        time.sleep(3600)

def start():
    thread = threading.Thread(target=subconscious_loop)
    # A daemon thread runs in the background and dies when the main program closes
    thread.daemon = True 
    thread.start()
    print("Subconscious running silently.")

if __name__ == "__main__":
    start()
    # Keeps the main program alive just long enough to see the first print statement
    time.sleep(5)