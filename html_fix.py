import os

marker_string = "&amp;lt;div class=&amp;#34;notification warning notification-gentle-alert"
merge_string1 = 'class="seq_contents tex2jax_ignore asciimath2jax_ignore">'
merge_string2 = '(function (require) {'

delta = 65
DATA_PATH = "./data/"
RES_PATH = "./result/"


def clear_problems(filename):
    """
    Removes bad sectors from html
    :param filename:
    :return:
    """
    lines = []
    with open(DATA_PATH + filename, 'r') as f:
        try:
            lines = f.readlines()
            for i in range(len(lines)):
                if marker_string in lines[i]:
                    for j in range(i, i + delta):
                        lines[j] = ""
        except UnicodeDecodeError:
            print(filename)
            return None
    f = open(RES_PATH + "FIX" + filename, 'w')
    f.writelines(lines)
    f.close()


def merge_fixed():
    files = os.listdir(RES_PATH)
    init_f = files[0]
    del files[0]
    f = open(RES_PATH + init_f, 'r')
    lines = f.readlines()
    start_i = get_line_index(lines, merge_string2)[-2] - 2
    f_begin = lines[:start_i]
    f_end = lines[start_i:]
    for en in files:
        with open(RES_PATH + en, 'r') as ff:
            lines = ff.readlines()
        s_ind = get_line_index(lines, merge_string1)[0] + 1
        e_ind = get_line_index(lines, merge_string2)[-2] - 1
        lines = lines[s_ind:e_ind]
        f_begin += lines
    f.close()
    f = open(RES_PATH + 'sum.html', 'w')
    f.writelines(f_begin + f_end)
    f.close()


def get_line_index(lines, pattern):
    ind = []
    for i, line in enumerate(lines):
        if pattern in line:
            ind.append(i)
    return ind


if __name__ == "__main__":
    files = os.listdir(DATA_PATH)
    for en in files:
        clear_problems(en)
    merge_fixed()
