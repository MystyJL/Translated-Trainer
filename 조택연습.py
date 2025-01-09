import keyboard
import time
from colorama import init, Fore, Style

# Initialize colorama
init()

def main():
    print("조인트 어택에 사용할 키 입력: ", end='', flush=True)
    while True:
        event = keyboard.read_event()  # Wait for a key event
        if event.event_type == 'down':
            button_a = event.name
            print(f"{button_a}")
            break

    print("캔슬기로 사용할 키 입력 (ex. 오리진, 쉐레 등): ", end='', flush=True)
    while True:
        event = keyboard.read_event()
        if event.event_type == 'down':
            button_b = event.name
            print(f"{button_b}")
            break

    # 기본 성공 기준 초
    success_threshold = 0.03

    # 성공 기준 변경 여부 확인
    print("\n현재 성공 기준 시간은 {:.3f}초입니다.".format(success_threshold))
    print("성공 기준 시간을 변경하려면 'y', 유지하려면 'n'을 눌러주세요.")
    while True:
        event = keyboard.read_event()
        if event.event_type == 'down':
            if event.name == 'y':
                print("새로운 성공 기준 시간을 입력하세요 (초 단위, 엔터키로 확인):")
                input_time = ""
                while True:
                    input_event = keyboard.read_event()
                    if input_event.event_type == 'down':
                        if input_event.name == 'enter':
                            try:
                                new_threshold = float(input_time)
                                if new_threshold > 0:
                                    success_threshold = new_threshold
                                    print(Fore.GREEN + f"성공 기준 시간이 {success_threshold:.3f}초로 변경되었습니다." + Style.RESET_ALL)
                                    break
                                else:
                                    print(Fore.RED + "0보다 큰 값을 입력하세요." + Style.RESET_ALL)
                            except ValueError:
                                print(Fore.RED + "유효한 숫자를 입력하세요." + Style.RESET_ALL)
                            break
                        elif input_event.name == 'backspace':
                            input_time = input_time[:-1]
                            print(f"\r입력 중: {input_time}{' ' * 10}", end='', flush=True)
                        else:
                            input_time += input_event.name
                            print(f"\r입력 중: {input_time}{' ' * 10}", end='', flush=True)
                break
            elif event.name == 'n':
                print(Fore.YELLOW + "기본 성공 기준 시간을 유지합니다." + Style.RESET_ALL)
                break

    test_start_message_shown = False

    while True:
        try:
            if not test_start_message_shown:
                print("\n조인트 어택을 눌러 테스트 시작. (테스트 종료: Esc)")
                test_start_message_shown = True

            # Wait for button A press
            event = keyboard.read_event()
            if event.event_type == 'down' and event.name == button_a:
                print("조택 시전중. 원할 때 키를 떼세요...")
                test_start_message_shown = False
                
                # Wait for A release
                while True:
                    release_event = keyboard.read_event()
                    if release_event.event_type == 'down' and release_event.name != button_a:
                        print(Fore.RED + f"실패! 조택을 떼기 전에 {release_event.name}가 눌림!" + Style.RESET_ALL)
                        break
                    elif release_event.event_type == 'up' and release_event.name == button_a:
                        print("조택 시전 완료. 캔슬기 기다리는중...")
                        start_time = time.time()

                        # Wait for B press
                        while True:
                            b_event = keyboard.read_event()
                            if b_event.event_type == 'down':
                                if b_event.name == button_b:
                                    interval = time.time() - start_time
                                    if interval <= success_threshold:
                                        print(Fore.GREEN + f"성공! 시전에 걸린 시간 {interval:.3f}초." + Style.RESET_ALL)
                                    else:
                                        print(Fore.RED + f"실패! 시전에 걸린 시간 {interval:.3f}초." + Style.RESET_ALL)
                                    break
                                else:
                                    print(Fore.RED + f"실패! 다른 키가 눌림: {b_event.name}" + Style.RESET_ALL)
                                    break
                        break

            elif event.event_type == 'down' and event.name != button_a:
                print(Fore.RED + f"실패! 다른 키가 눌림 {event.name}" + Style.RESET_ALL)

            # Allow quitting with ESC
            if event.name == 'esc':
                print("Esc 입력으로 테스트 종료.")
                break

        except KeyboardInterrupt:
            print("Program interrupted. Exiting.")
            break

if __name__ == "__main__":
    main()
