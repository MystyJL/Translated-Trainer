import keyboard
import time

def main():
    print("조인트 어택에 사용할 키 입력: ", end = '', flush = True)
    while True:
        event = keyboard.read_event()  # Wait for a key event
        if event.event_type == 'down':
            button_a = event.name
            print(f"{button_a}")
            break

    print("캔슬기로 사용할 키 입력 (ex. 오리진, 쉐레 등): ", end = '', flush = True)
    while True:
        event = keyboard.read_event()
        if event.event_type == 'down':
            button_b = event.name
            print(f"{button_b}")
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
                        print(f"실패! 조택을 떼기 전에 {release_event.name}가 눌림!")
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
                                    if interval <= 0.06:
                                        print(f"성공! 시전에 걸린 시간 {interval:.3f}초.")
                                    else:
                                        print(f"실패! 시전에 걸린 시간 {interval:.3f}초.")
                                    break
                                else:
                                    print(f"실패! 다른 키가 눌림: {b_event.name}")
                                    break
                        break

            elif event.event_type == 'down' and event.name != button_a:
                print(f"실패! 다른 키가 눌림 {event.name}")

            # Allow quitting with ESC
            if event.name == 'esc':
                print("Esc 입력으로 테스트 종료.")
                break

        except KeyboardInterrupt:
            print("Program interrupted. Exiting.")
            break

if __name__ == "__main__":
    main()
