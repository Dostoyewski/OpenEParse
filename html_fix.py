marker_string = "&amp;lt;div class=&amp;#34;notification warning notification-gentle-alert"
delta = 65


def clear_problems(filename):
    """
    Removes bad sectors from html
    :param filename:
    :return:
    """
    lines = []
    with open(filename, 'r') as f:
        lines = f.readlines()
        for i in range(len(lines)):
            if marker_string in lines[i]:
                for j in range(i, i + delta):
                    lines[j] = ""
        f.close()
    f = open("FIX" + filename, 'w')
    f.writelines(lines)
    f.close()


if __name__ == "__main__":
    clear_problems("1.html")
