class ColorsSaver:
    def __init__(self):
        self.green = 255
        self.red = 255
        self.blue = 255

    def get_color(self):
        return self.red, self.green, self.blue

    def set_color(self, red, green, blue):
        self.red = (self.red - red) % 256
        self.green = (self.green - green) % 256
        self.blue = (self.blue - blue) % 256
