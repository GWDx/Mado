from PIL import Image as PILImage
from graia.ariadne.message.element import Plain, Image

from functions import *
from initialize import help

from getCopilotAnswer import getCopilotAnswer


def kernel(fullCommand, id):
    command = fullCommand
    firstLine = command.split('\n')[0].lower()
    code = command[len(firstLine) + 1:]
    task = firstLine.split(' ')[0]
    options = firstLine[(firstLine + ' ').find(' '):].strip(' ')
    result = None
    ans = ''

    try:
        if task == 'cpy':
            fileName = writeFile(id, '.py', code)
            ans = getCopilotAnswer(code, fileName)

        elif task == 'co':
            suffix = options.split(' ')[0]
            fileName = writeFile(id, f'.{suffix}', code)
            ans = getCopilotAnswer(code, fileName)

        # ExecutePython (epy)
        elif regularQ(firstLine, 'python3', 'py'):
            fileName = writeFile(id, '.py', code)
            ans = runCMD(f'python3 {fileName}', id, options)

        # erb
        elif regularQ(firstLine, 'rb') or regularQ(firstLine, 'ruby'):
            fileName = writeFile(id, '.rb', code)
            ans = runCMD(f'ruby {fileName}', id, options)

        # ejs
        elif regularQ(firstLine, 'js'):
            fileName = writeFile(id, '.js', code)
            ans = runCMD(f'node {fileName}', id, options)

        # ExecuteMathematica (ema)
        # 好友仅 '-p' 也可输出图片
        elif (regularQ(firstLine, 'mathematica', 'ma') or regularQ(firstLine, 'mma') or regularQ(firstLine, 'wl')
              or (not '-' in id) and ('-p' in firstLine or '-g' in firstLine)):
            fileName = writeFile(id, '.wl', code)

            if '-p' in firstLine:
                result = exportPicture(fileName, 'PNG', options, id)
            elif '-g' in firstLine:
                result = exportPicture(fileName, 'GIF', options, id)
            else:
                ans = runCMD(mathematicaCMD(fileName), id, options)

        # ecpp
        elif regularQ(firstLine, 'cpp', 'cp') or regularQ(firstLine, 'c++', 'c+'):
            fileName = writeFile(id, '.cpp', code)
            outName = fileName.split('.')[0] + '.out'
            cppCMD = f'g++ -o {outName} {fileName} && ./{outName}'
            ans = runCMD(cppCMD, id, options)

        # pip install
        elif firstLine.startswith('pip install'):
            ans = runCMD('pip3 ' + options, id, '')

        # ExecuteBash (esh)
        elif regularQ(firstLine, 'bash') or regularQ(firstLine, 'sh'):
            if permissionQ(id):
                fileName = writeFile(id, '.sh', code)
                ans = runCMD(f'bash {fileName}', id, options)

        # help
        elif firstLine == 'help':
            ans = help.strip('\n')

        # # 好友默认执行 Mathematica
        # elif not '-' in id:
        #     fileName = writeFile(id, '.wl', command)
        #     ans = runCMD(mathematicaCMD(fileName), id, options)

        else:
            return None

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
    if result == None:
        result = Plain(ans)
    return result


def mathematicaCMD(fileName):
    return f'wolframscript -print all -charset None -f {fileName}'


def exportPicture(fileName, suffix, options, id):
    imgName = fileName.split('.')[0] + '.' + suffix.lower()
    CMD = mathematicaCMD(fileName) + f' -format {suffix} > {imgName}'
    runCMD(CMD, id, options)
    currentDirectory = os.getcwd()
    imgPath = os.path.join(currentDirectory, imgName)
    print('>> ', imgPath)
    try:
        PILImage.open(imgPath)
        result = Image(url=f'file://{imgPath}')
    except Exception as ex:
        print('>> ', ex)
        with open(imgPath, 'r') as f:
            content = f.read()
        result = Plain(content)
    return result


if __name__ == '__main__':
    copilotCommand = 'cpy\nimport numpy\n# arr is random array, size 5\n'
    print(kernel(copilotCommand, 'test'))
    # kernel('help', 'test')

    # pyCommand = 'epy\nimport time\ntime.sleep(20)\nprint(20)'
    # pyCommand = 'epy\na=1/0'
    # print(kernel(pyCommand, 'test'))

    # mmaCommand = 'ema\nTable[i^2,{i,10}]'
    # mmaCommand = 'ema -p\nPolarPlot[Sin[5t/3],{t,0,6Pi}]'
    # print(kernel(mmaCommand, 'test'))

    # bashCommand = 'esh\npip install numpy'
    # print(kernel(bashCommand, 'test'))
