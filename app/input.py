from gpiozero import Button


def register_button(n_gpio, func):
    button = Button(n_gpio)
    button.when_pressed = func
    return button
