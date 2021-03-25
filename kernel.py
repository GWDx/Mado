from config import *

def getFirstLine(command):
    return command.split('\n')[0].lower()

def code(command):
    return command[(command + '\n').find('\n'):].strip('\n')

def options(firstLine):
    return firstLine[(firstLine + ' ').find(' '):].strip(' ')


def kernel(command, id):
    firstLine = getFirstLine(command)
    ans = ''
    
    try:
        # ExecutePython
        if regularQ(firstLine, "python", "py"):
            fileName = writeFile(id, ".py", code(command))
            ans = runCMD('python3 "' + fileName + '"')

        # ExecuteMathematica
        elif regularQ(firstLine, "mathematica", "ma") or regularQ(firstLine, "mma", "mma"):
            fileName = writeFile(id, ".wl", code(command))
            exeFile = '/opt/vlab/mathematica-12/Executables/wolframscript'
            ans = runCMD(exeFile + ' -print all -f "' + fileName + '"')

        # help
        elif firstLine.startswith("help"):
            ans = help
        
        # pip install
        elif firstLine.startswith("pip install"):
            ans = (runCMD('pip3 ' + options(firstLine)) + "\nEnd").strip('\n')
    except Exception as ex:
        ans = 'Error'
        print(ex)
    
    # print(ans)
    return ans

if __name__=='__main__':
    kernel('help', 'test')

    pyCode = 'epy\nfor i in range(5):\n print(i)'
    print(code(pyCode))
    kernel(pyCode, 'test')

    mmaCode = 'ema\nTable[i^2,{i,10}]'
    kernel(mmaCode, 'test')