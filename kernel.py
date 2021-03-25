import time
from config import *
from graia.application.message.elements.internal import Plain, Image

def getFirstLine(command):
    return command.split('\n')[0].lower()

def code(command):
    return command[(command + '\n').find('\n'):].strip('\n')

def options(firstLine):
    return firstLine[(firstLine + ' ').find(' '):].strip(' ')


def kernel(command, id):
    firstLine = getFirstLine(command)
    result = 0
    ans = ''

    try:
        # ExecutePython
        if regularQ(firstLine, "python3", "py"):
            fileName = writeFile(id, ".py", code(command))
            ans = runCMD('python3 "' + fileName + '"')

        # ExecuteMathematica
        elif regularQ(firstLine, "mathematica", "ma") or regularQ(firstLine, "mma", "mma"):
            fileName = writeFile(id, ".wl", code(command))
            exeFile = '/opt/vlab/mathematica-12/Executables/wolframscript'
            coreCMD = exeFile + ' -print all -f "' + fileName + '"'

            option = options(firstLine + '..')[:2]
            if option == '-p':
                imgName = fileName[:-3] + '.png'
                runCMD(coreCMD + ' -format PNG > "' + imgName + '"')
                print('>> ', imgName)
                time.sleep(2)
                result = Image.fromLocalFile(imgName)
            else:
                ans = runCMD(coreCMD)
        
        # pip install
        elif firstLine.startswith("pip install"):
            ans = (runCMD('pip3 ' + options(firstLine)) + '\nEnd').strip('\n')

        # help
        elif firstLine.startswith("help"):
            ans = help

        if len(ans) > 2000 and options(firstLine).find('-o') < 0:
            raise NameError('Length > 2000\nappend -o to output unlimitedly')
    except Exception as ex:
        ans = str(ex)
        print('>> ', ex)
    
    # print(ans)
    if result == 0:
        result = Plain(ans)
    return result


if __name__=='__main__':
    kernel('help', 'test')

    # pyCommand = 'epy  -abc\nfor i in range(5):\n print(i)'
    # print(code(pyCommand))

    pyCommand = 'epy\nimport time\ntime.sleep(20)\nprint(20)'

    # pyCommand = 'epy\na=1/0'
    print(kernel(pyCommand, 'test'))

    # mmaCommand = 'ema\nTable[i^2,{i,10}]'
    # kernel(mmaCommand, 'test')
    # mmaCommand = 'ema -p\nPolarPlot[Sin[5t/3],{t,0,6Pi}]'

    # kernel(mmaCommand, 'test')