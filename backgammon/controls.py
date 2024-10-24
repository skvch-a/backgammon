def update_controls(bg_color, screen, field, dices, secret_flag, needed_color):
    if not secret_flag:
        screen.fill(bg_color)
        field.output(dices)
    else:
        current_color = needed_color.get_color()
        screen.fill(current_color)
        field.output(dices)
        needed_color.set_color(10, 5, 3)
