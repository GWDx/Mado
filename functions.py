import os
import time
import random
import subprocess


def writeFile(id, suffix, code):
    path = 'temp/' + id + '/'
    if not os.path.exists(path):
        os.makedirs(path)

    ymd = time.strftime('%Y-%m-%d', time.localtime(time.time()))
    hms = time.strftime('%H-%M-%S', time.localtime(time.time()))
    path2 = path + ymd + '/'
    if not os.path.exists(path2):
        os.makedirs(path2)

    fileName = path2 + hms + suffix
    minuteFileNumber = [i[:5] for i in os.listdir(path2)].count(hms[:5])
    if os.path.exists(fileName) or minuteFileNumber >= 6:
        raise RuntimeError('Too Frequent')

    with open(fileName, 'w') as file:
        file.write(code + '\n')
    return fileName


def runCMD(cmd, id, options):
    timeLimit = 15
    if cmd.startswith('pip'):
        timeLimit = 45
    if '-t' in options and permissionQ(id):
        timeLimit = int(options.split('-t')[1].strip(' ').split(' ')[0])

    ret = subprocess.run(cmd, timeout=timeLimit, encoding='utf-8', shell=True, capture_output=True)
    ans = ret.stdout.strip('\n')
    if ret.stderr != '':
        ans = '####\n' + ret.stderr.strip('\n') + '\n####\n' + ret.stdout
    if ret.returncode != 0 or ans == '' or random.randint(1, 100) == 1:
        ans = f'>> returncode = {ret.returncode}\n' + ans
    return ans.strip('\n')


def regularQ(firstLine, full, kernel=None):
    if kernel == None:
        kernel = full
    if firstLine.find(kernel) <= 0:
        return False
    left = firstLine.split(kernel)[0]
    right = firstLine[len(left):].split(' ')[0]
    return 'execute'.startswith(left) and full.startswith(right)


def permissionQ(id):
    with open('temp/permission.txt', 'r') as file:
        friends = file.read().split('\n')

    if id.split('-')[-1] in friends:
        return True
    elif not '-' in id:
        with open('temp/permission.txt', 'a') as file:
            file.write(id + '\n')
        return True

    raise RuntimeError('Permission Denied')


if __name__ == '__main__':
    # print(regularQ('ebash','bash','sh'))

    ans = runCMD('python testPython.txt', 'test', '')
    print(ans)

    # ans = runCMD('bash testBash.txt', 'test', '')
    # print(ans)
