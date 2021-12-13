from gpiozero import Button


def register_button(n_gpio, func):
    button = Button(n_gpio)
    button.when_pressed = func
    return button


if __name__ == "__main__":
    from signal import pause


    def test_button(n):
        print("Button " + str(n) + " pressed!")


    button12 = register_button(12, lambda: test_button(12))
    button16 = register_button(16, lambda: test_button(16))

    pause()