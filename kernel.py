import time
from graia.application.message.elements.internal import Plain, Image

from functions import *
from initialize import help


def code(command):
    return command[(command + '\n').find('\n'):].strip('\n')

def options(firstLine):
    return firstLine[(firstLine + ' ').find(' '):].strip(' ')


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
        elif (regularQ(firstLine, "mathematica", "ma") or 
              regularQ2(firstLine, "mma") or regularQ2(firstLine, "wl")):
            fileName = writeFile(id, ".wl", code(command))
            coreCMD = 'wolframscript -print all -f "' + fileName + '"'

            firstOption = options(firstLine + '..')[:2]
            if firstOption == '-p':
                imgName = fileName[:-3] + '.png'
                runCMD(coreCMD + ' -format PNG > "' + imgName + '"', id, options(firstLine))
                print('>> ', imgName)
                time.sleep(2)
                result = Image.fromLocalFile(imgName)
            else:
                ans = runCMD(coreCMD, id, options(firstLine))
        
        # ExecuteBash (esh)
        elif regularQ2(firstLine, "bash") or regularQ2(firstLine, "sh"):
            if permissionQ(id):
                fileName = writeFile(id, ".sh", code(command))
                ans = runCMD('bash "' + fileName + '"', id, options(firstLine))
                
        # pip install
        elif firstLine.startswith("pip install"):
            ans = runCMD('pip3 ' + options(firstLine), id, '')
        
        # help
        elif firstLine.startswith("help"):
            ans = help

        else:
            return 0

        if len(ans) > 2000 and options(firstLine).find('-o') < 0:
            if permissionQ(id):
                raise RuntimeError('Length > 2000')

        if len(ans.split('\n')) > 50 and options(firstLine).find('-o') < 0:
            if permissionQ(id):
                raise RuntimeError('Rows > 50')
        
    except Exception as ex:
        ans = str(ex)
        print('>> ', ex)
    
    # print(ans)
    if result == 1:
        result = Plain(ans)
    return result


if __name__=='__main__':
    kernel('help', 'test')

    pyCommand = 'epy\nimport time\ntime.sleep(20)\nprint(20)'
    pyCommand = 'epy\na=1/0'
    print(kernel(pyCommand, 'test'))

    # mmaCommand = 'ema\nTable[i^2,{i,10}]'
    # mmaCommand = 'ema -p\nPolarPlot[Sin[5t/3],{t,0,6Pi}]'
    # print(kernel(mmaCommand, 'test'))

    # bashCommand = 'esh\npip install numpy'
    # print(kernel(bashCommand, 'test'))