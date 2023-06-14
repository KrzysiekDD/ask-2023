from PIL import Image

a = Image.open("microprocessor.png")

b = a.resize((146+100, int(176*2.5)))
b.save("microprocessor_resized.png")


c = Image.open("background.png")

d = c.resize((1081, 659))

d.save("background_resized.png")
