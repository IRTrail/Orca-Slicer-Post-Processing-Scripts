import re
import sys


def read_file(read_path) -> list:
    try:
        with open(read_path, 'r') as file:
            return file.readlines()

    except FileNotFoundError:
        print(f"The file {file_path} was not found.")

    except Exception as e:
        print(f"An error occurred: {e}")


def write_file(write_path, content):
    try:
        with open(write_path, 'w') as file:
            file.write(''.join(content))

    except FileNotFoundError:
        print(f"The file {file_path} was not found.")

    except Exception as e:
        print(f"An error occurred: {e}")


def find_corners(content) -> list:
    """
    find the first three corners of the wipe tower
    these are usually found in the end output of the gcode file
    """
    x1_string = '; wipe_tower_x = '
    y1_string = '; wipe_tower_y = '
    x2_string = '; prime_tower_width = '
    x1 = 0
    x2 = 0
    y1 = 0

    for line in content:
        if x1_string in line:
            x1 = round(float(line.rsplit(maxsplit=1)[-1]), 4)
        if y1_string in line:
            y1 = round(float(line.rsplit(maxsplit=1)[-1]), 4)
        if x2_string in line:
            x2 = round(float(line.rsplit(maxsplit=1)[-1]), 4)
        else:
            print("No prime tower found.")
            sys.exit(0)

    x2 = x1 + x2

    y2 = find_prime_tower_height(content)
    return [x1, x2, y1, y2]


def find_prime_tower_height(content) -> float:
    """
    Scan the file and look for the wipe tower code to find y2.
    This assumes that the first layer of the prime tower is full size.
    I.e. the tower doesn't taper outward as it goes up.
    """

    start_string = '; CP EMPTY GRID END'
    end_string = '; printing object'
    in_block = False
    y2 = 0

    for line in content:
        # turn on the search at the line with start_string
        if start_string in line:
            in_block = True
        # exit the search at the line with end_string
        if end_string in line and in_block is True:
            return round(y2, 4)
        for word in line.split():
            if in_block and re.search(r"Y\d+", word):
                y_temp = re.search(r"(\d+(?:\.\d*)?)", word)
                y_temp = float(y_temp.group(0))
                if abs(y_temp) > abs(y2):
                    y2 = y_temp


def create_exclude_polygon(content):
    corners = find_corners(content)
    center_x = round((corners[0] + corners[1]) / 2, 4)
    center_y = round((corners[2] + corners[3]) / 2, 4)

    # the exclude polygon, if square, follows this pattern: [[x,y],[X,y],[X,Y],[x,Y],[x,y]]
    # where lower case is the smaller value and upper case is the larger value.
    excl_obj = (f'EXCLUDE_OBJECT_DEFINE NAME=Prime_Tower '
                f'CENTER={center_x},{center_y}'
                f' POLYGON=[[{corners[0]},{corners[2]}],'
                f'[{corners[1]},{corners[2]}],'
                f'[{corners[1]},{corners[3]}],'
                f'[{corners[0]},{corners[3]}],'
                f'[{corners[0]},{corners[2]}]]\n'
                )

    # now add the excl_obj line to the content after "; EXECUTABLE_BLOCK_START".
    for idx, line in enumerate(content, 1):
        if '; EXECUTABLE_BLOCK_START' in line:
            idx = idx + 1
            content.insert(idx, excl_obj)
            return content


def process_file(input_f):
    content = read_file(input_f)
    modified_content = create_exclude_polygon(content)
    write_file(input_f, modified_content)


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    # Check if a file was provided as an argument
    if len(sys.argv) < 1:
        print("Usage: drag and drop a file onto this script.")
        sys.exit(1)

    # The file path is the first argument
    file_path = sys.argv[1]
    # Call the main processing function
    process_file(file_path)
