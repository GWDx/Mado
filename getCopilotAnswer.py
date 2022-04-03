from multiprocessing import Lock
from neovim import attach
import nest_asyncio
import time

nvimLock = Lock()
nest_asyncio.apply()


def getCopilotAnswer(code, fileName):
    nvimLock.acquire()
    try:
        nvim = attach('socket', path='/tmp/nvim')

        with open(fileName, 'w') as f:
            f.write(code + ' ')
        nvim.command(f'e! {fileName}')

        # move to file end
        nvim.command('normal! G')
        nvim.command('normal! $')

        # insert mode
        nvim.command('startinsert')

        # nvim.feedkeys(' ')
        # nvim.call('copilot#Schedule')

        waitTime = 0.5
        tryCount = 20

        for i in range(tryCount):
            time.sleep(waitTime)
            ans = nvim.call('copilot#GetDisplayedSuggestion')
            ansText = ans['text']
            if ansText != '':
                result = code.split('\n')[-1] + ansText
                nvim.call('copilot#Accept')
                nvim.command('w')
                break
        else:
            result = '# Failed'

    except Exception as ex:
        result = str(ex)
        print('>> ', ex)

    nvimLock.release()
    return result


allExampleCode = [
    'def readFile(',
    '# 打印 1 到 5 的整数，每个数前加上一个 0\nfor',
    'ans=[1,2,3]\n# write file\n',
    'import requests\n\ndef getBilibiliUserInfo(uid):',
]

if __name__ == '__main__':
    for exampleCode in allExampleCode:
        answer = getCopilotAnswer(exampleCode, 'temp/test1.py')
        print(answer)
