with open('input.bmp', 'rb') as input_file:
    header = input_file.read(54)
    pixels = [255 - x for x in input_file.read()]
with open('res.bmp', 'wb') as output_file:
    output_file.write(header)
    output_file.write(bytes(pixels))
