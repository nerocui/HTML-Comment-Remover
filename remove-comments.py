import os
import glob
import sys

def remove_comments_from_file(filename, dirpath=''):
    filename = os.path.join(dirpath, filename)
    temp_path = os.path.join(dirpath, 'temp.html')
    cstart = "<!--"
    cend = "-->"
    copyright_start = "<!--/*"
    copyright_end = "*/-->"
    incomment = False
    with open(filename, 'r') as f_read, open(temp_path, 'w') as temp:
        for line in f_read:
            if incomment and cend not in line:
                continue
            if cstart in line and cend not in line and copyright_start not in line:
                if line.strip().startswith(cstart):
                    incomment = True
                    continue
                else:
                    temp.write(line.split(cstart)[0])
                    incomment = True
                    continue
            elif cend in line and cstart not in line and copyright_end not in line:
                if line.strip().endswith(cend):
                    incomment = False
                    continue
                else:
                    temp.write(line.split(cend)[-1])
                    incomment = False
                    continue
            elif line.strip().startswith(cstart) and line.strip().endswith(cend) and copyright_start not in line and copyright_end not in line:
                continue
            elif cstart in line.strip() and cend in line.strip() and copyright_start not in line and copyright_end not in line:
                new_line_head = ""
                new_line_tail = ""
                if not line.strip().startswith(cstart):
                    new_line_head = line.strip().split(cstart)[0]
                if not line.strip().endswith(cend):
                    new_line_tail = line.strip().split(cend)[-1]
                new_line = new_line_head + new_line_tail
                temp.write(new_line)
                continue
            temp.write(line)

    os.remove(filename)
    os.rename(temp_path, filename)


def main():
    walk_dir = sys.argv[1]
    count = 0
    for filename in glob.iglob(walk_dir + '**/**/*.html', recursive=True):
        remove_comments_from_file(filename)
        count += 1
    print('modified ' + str(count) + ' files')

if __name__ == '__main__':
    main()