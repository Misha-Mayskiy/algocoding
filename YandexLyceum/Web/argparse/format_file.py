import argparse


def format_text_block(frame_height, frame_width, file_name):
    try:
        with open(file_name, 'r', encoding='utf-8') as file:
            content = file.read()

        lines = content.split('\n')

        formatted_lines = []

        for line in lines:
            if not line:
                formatted_lines.append(line)
                continue

            if len(line) <= frame_width:
                formatted_lines.append(line)
                continue

            current_position = 0
            while current_position < len(line):
                chunk = line[current_position:current_position + frame_width]
                formatted_lines.append(chunk)
                current_position += frame_width

        formatted_lines = formatted_lines[:frame_height]

        formatted_text = '\n'.join(formatted_lines)

        return formatted_text

    except Exception as e:
        return str(e)


def main():
    parser = argparse.ArgumentParser(description='Format text from file to fit in a frame')
    parser.add_argument('--frame-height', type=int, required=True, help='Height of the frame in characters')
    parser.add_argument('--frame-width', type=int, required=True, help='Width of the frame in characters')
    parser.add_argument('file_name', help='Name of the file to format')

    args = parser.parse_args()

    formatted_text = format_text_block(args.frame_height, args.frame_width, args.file_name)
    print(formatted_text)


if __name__ == '__main__':
    main()
