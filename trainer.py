import keyboard
import time
from colorama import init, Fore, Style

# This is just a translation of the program all rights to this are to the original creator who wrote the inven post
# https://www.inven.co.kr/board/maple/2294/402040

# Initialize colorama
init()

def main():
    print("Enter the key to use for Twin Blades of Time: ", end='', flush=True)
    while True:
        event = keyboard.read_event()  # Wait for a key event
        if event.event_type == 'down':
            button_a = event.name
            print(f"{button_a}")
            break

    print("Enter the key to use as a canceller (ex. Origin, Shadow rain, etc.): ", end='', flush=True)
    while True:
        event = keyboard.read_event()
        if event.event_type == 'down':
            button_b = event.name
            print(f"{button_b}")
            break

    # 기본 성공 기준 초
    success_threshold = 0.03

    # 성공 기준 변경 여부 확인
    print("\nThe current success standard time is {:.3f}seconds.".format(success_threshold))
    print("Press 'y' to change the success criteria time, or 'n' to keep it.")
    while True:
        event = keyboard.read_event()
        if event.event_type == 'down':
            if event.name == 'y':
                print("Enter the new success criterion time (in seconds, confirm with Enter key):")
                input_time = ""
                while True:
                    input_event = keyboard.read_event()
                    if input_event.event_type == 'down':
                        if input_event.name == 'enter':
                            try:
                                new_threshold = float(input_time)
                                if new_threshold > 0:
                                    success_threshold = new_threshold
                                    print(Fore.GREEN + f"success standard time changed to {success_threshold:.3f} seconds." + Style.RESET_ALL)
                                    break
                                else:
                                    print(Fore.RED + "Please enter a larger value." + Style.RESET_ALL)
                            except ValueError:
                                print(Fore.RED + "Please enter a valid number." + Style.RESET_ALL)
                            break
                        elif input_event.name == 'backspace':
                            input_time = input_time[:-1]
                            print(f"\rTyping: {input_time}{' ' * 10}", end='', flush=True)
                        else:
                            input_time += input_event.name
                            print(f"\rTyping: {input_time}{' ' * 10}", end='', flush=True)
                break
            elif event.name == 'n':
                print(Fore.YELLOW + "Maintaining the default success criteria time." + Style.RESET_ALL)
                break

    test_start_message_shown = False

    while True:
        try:
            if not test_start_message_shown:
                print("\nClick Twinblades to start the test. (End test: Esc)")
                test_start_message_shown = True

            # Wait for button A press
            event = keyboard.read_event()
            if event.event_type == 'down' and event.name == button_a:
                print("Casting Twinblades. Release the key when you want...")
                test_start_message_shown = False
                
                # Wait for A release
                while True:
                    release_event = keyboard.read_event()
                    if release_event.event_type == 'down' and release_event.name != button_a:
                        print(Fore.RED + f"failure! Before releasing Twinblades {release_event.name} Pressed!" + Style.RESET_ALL)
                        break
                    elif release_event.event_type == 'up' and release_event.name == button_a:
                        print("Twinblade casting completed. Waiting for cancellation...")
                        start_time = time.time()

                        # Wait for B press
                        while True:
                            b_event = keyboard.read_event()
                            if b_event.event_type == 'down':
                                if b_event.name == button_b:
                                    interval = time.time() - start_time
                                    if interval <= success_threshold:
                                        print(Fore.GREEN + f"Success! Time taken to cast {interval:.3f} seconds." + Style.RESET_ALL)
                                    else:
                                        print(Fore.RED + f"Failure! Time taken to cast {interval:.3f} seconds." + Style.RESET_ALL)
                                    break
                                else:
                                    print(Fore.RED + f"Failure! Another key pressed: {b_event.name}" + Style.RESET_ALL)
                                    break
                        break

            elif event.event_type == 'down' and event.name != button_a:
                print(Fore.RED + f"failure! Another key pressed {event.name}" + Style.RESET_ALL)

            # Allow quitting with ESC
            if event.name == 'esc':
                print("End the test by pressing Esc.")
                break

        except KeyboardInterrupt:
            print("Program interrupted. Exiting.")
            break

if __name__ == "__main__":
    main()
