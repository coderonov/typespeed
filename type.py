import sys
import time
from pynput import keyboard
from pynput.keyboard import Controller, Key

controller = Controller()
pressed = set()
start_flag = False
abort_flag = False

def read_text():
    print("Вставьте текст, затем на новой строке введите END и нажмите Enter:")
    lines = []
    while True:
        line = sys.stdin.readline()
        if not line or line.rstrip("\n") == "END":
            break
        lines.append(line)
    return "".join(lines)

def get_speed():
    while True:
        try:
            cps = float(input("Символов в секунду: ").strip().replace(",", "."))
            if cps > 0:
                return cps
        except ValueError:
            pass
        print("Введите положительное число")

def countdown(seconds):
    for i in range(seconds, 0, -1):
        print(f"Начало через {i}...", end="\r")
        time.sleep(1)
    print(" " * 30, end="\r")

def type_text(text, delay):
    global abort_flag
    for ch in text:
        if abort_flag:
            print("\nОстановлено")
            return
        if ch == "\n":
            controller.press(Key.enter)
            controller.release(Key.enter)
        elif ch == "\t":
            controller.press(Key.tab)
            controller.release(Key.tab)
        else:
            controller.type(ch)
        time.sleep(delay)
    print("\nГотово")

def on_press(key):
    global start_flag, abort_flag
    pressed.add(key)
    if Key.up in pressed and Key.left in pressed:
        start_flag = True
    if key == Key.esc:
        abort_flag = True

def on_release(key):
    pressed.discard(key)

def main():
    global start_flag
    text = read_text()
    if not text:
        print("Пустой текст, выход")
        return
    cps = get_speed()
    delay = 1 / cps
    print(f"\nТекст готов ({len(text)} символов).")
    print("Нажмите одновременно стрелку вверх и стрелку влево, чтобы начать печать")
    print("(Esc — остановить во время печати)\n")

    listener = keyboard.Listener(on_press=on_press, on_release=on_release)
    listener.start()

    while not start_flag:
        time.sleep(0.05)

    countdown(3)
    type_text(text, delay)
    listener.stop()

if __name__ == "__main__":
    main()
