from graia.application.message.elements.internal import Plain, Image

import time

from functions import *
from initialize import help


def kernel(fullCommand, id):
    command = fullCommand.strip('\n')
    firstLine = command.split('\n')[0].lower()
    result = 1
    ans = ''

    try:
        # ExecutePython (epy)
        if regularQ(firstLine, "python3", "py"):
            fileName = writeFile(id, ".py", code(command))
            ans = runCMD('python3 "' + fileName + '"', id, options(firstLine))

        # ExecuteMathematica (ema)
        # 好友仅 '-p' 也可输出图片
        elif (regularQ(firstLine, "mathematica", "ma") or
              regularQ2(firstLine, "mma") or regularQ2(firstLine, "wl") or
              (not '-' in id) and ('-p' in firstLine or '-g' in firstLine)):
            fileName = writeFile(id, ".wl", code(command))

            if '-p' in firstLine:
                result = exportPicture(fileName, 'PNG', firstLine, id)
            elif '-g' in firstLine:
                result = exportPicture(fileName, 'GIF', firstLine, id)
            else:
                ans = runCMD(mathematicaCMD(fileName), id, options(firstLine))

        # ecpp
        elif regularQ(firstLine, "cpp", "cp") or regularQ(firstLine, "c++", "c+"):
            fileName = writeFile(id, ".cpp", code(command))
            outName = fileName.split('.')[0] + '.out'
            cppCMD = 'g++ -o ' + outName + ' ' + fileName + ' && ./' + outName
            ans = runCMD(cppCMD, id, options(firstLine))

        # pip install
        elif firstLine.startswith("pip install"):
            ans = runCMD('pip3 ' + options(firstLine), id, '')

        # ExecuteBash (esh)
        elif regularQ2(firstLine, "bash") or regularQ2(firstLine, "sh"):
            if permissionQ(id):
                fileName = writeFile(id, ".sh", code(command))
                ans = runCMD('bash "' + fileName + '"', id, options(firstLine))

        # help
        elif firstLine == "help":
            ans = help.strip('\n')

        # 好友默认执行 Mathematica
        elif not '-' in id:
            fileName = writeFile(id, ".wl", command)
            ans = runCMD(mathematicaCMD(fileName), id, options(firstLine))

        else:
            return 0

        if len(ans) > 1000:
            if not ('-o' in firstLine and permissionQ(id)):
                raise RuntimeError('Length > 1000')

        if len(ans.split('\n')) > 40:
            if not ('-o' in firstLine and permissionQ(id)):
                raise RuntimeError('Rows > 40')

    except Exception as ex:
        ans = str(ex)
        print('>> ', ex)

    # print(ans)
    if result == 1:
        result = Plain(ans)
    return result


def code(command):
    return command[(command + '\n').find('\n'):].strip('\n')


def options(firstLine):
    return firstLine[(firstLine + ' ').find(' '):].strip(' ')


def mathematicaCMD(fileName):
    return 'wolframscript -print all -charset None -f "' + fileName + '"'


def exportPicture(fileName, suffix, firstLine, id):
    imgName = fileName.split('.')[0] + '.' + suffix.lower()
    CMD = mathematicaCMD(fileName) + ' -format ' + \
        suffix + ' > "' + imgName + '"'
    runCMD(CMD, id, options(firstLine))
    print('>> ', imgName)
    time.sleep(2)
    result = Image.fromLocalFile(imgName)
    return result


if __name__ == '__main__':
    kernel('help', 'test')

    pyCommand = 'epy\nimport time\ntime.sleep(20)\nprint(20)'
    pyCommand = 'epy\na=1/0'
    print(kernel(pyCommand, 'test'))

    # mmaCommand = 'ema\nTable[i^2,{i,10}]'
    # mmaCommand = 'ema -p\nPolarPlot[Sin[5t/3],{t,0,6Pi}]'
    # print(kernel(mmaCommand, 'test'))

    # bashCommand = 'esh\npip install numpy'
    # print(kernel(bashCommand, 'test'))
