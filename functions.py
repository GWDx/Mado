import os
import time
import random
import subprocess


def writeFile(id, suffix, code):
    path = 'temp/' + id + '/'
    if not os.path.exists(path):
        os.makedirs(path)
    
    ymd = time.strftime('%Y-%m-%d', time.localtime(time.time()))
    hms = time.strftime('%H-%M-%S',time.localtime(time.time()))
    path2 = path + ymd + '/'
    if not os.path.exists(path2):
        os.makedirs(path2)

    fileName = path2 + hms + suffix
    minuteFileNumber = [i[:5] for i in os.listdir(path2)].count(hms[:5])
    if os.path.exists(fileName) or minuteFileNumber >= 6:
        raise RuntimeError('Too Frequent')

    f = open(fileName, 'w', encoding='utf-8')
    f.write(code + "\n")
    f.close()
    return(fileName)


def runCMD(cmd, id, options):
    timeLimit = 15
    if cmd.startswith('pip'):
        timeLimit = 45
    if options.find('-t') >= 0:
        if permissionQ(id):
            timeLimit = int(options.split('-t')[1].strip(' ').split(' ')[0])

    ret = subprocess.run(cmd, timeout = timeLimit, encoding = "utf-8", shell=True,
                        stdout = subprocess.PIPE, stderr = subprocess.PIPE)
    ans = ret.stdout.strip('\n')
    if ret.stderr != '':
        ans = '####\n' + ret.stderr.strip('\n') + '\n####\n' + ret.stdout
    if ret.returncode != 0 or random.randint(1,100) == 1:
        ans = '>> returncode = ' + str(ret.returncode) + '\n' + ans
    if ans == '':
        ans = '>> returncode = ' + str(ret.returncode)
    return(ans)


def regularQ2(firstLine, kernel):
    return regularQ(firstLine, kernel, kernel)

def regularQ(firstLine, full, kernel):
    if firstLine.find(kernel)<=0:
        return False
    left = firstLine.split(kernel)[0]
    right = firstLine[len(left):].split(' ')[0]
    return "execute".startswith(left) and full.startswith(right)


def permissionQ(id):
    f = open('temp/permission.txt', 'r', encoding='utf-8')
    friends = f.read().split('\n')
    f.close()

    if id.split('-')[-1] in friends:
        return True
    elif id.find('-')<0:
        f = open('temp/permission.txt', 'a', encoding='utf-8')
        f.write(id)
        f.close()
        return True
    
    raise RuntimeError('Permission Denied')


if __name__=='__main__':
    # print(regularQ('ebash','bash','sh'))

    ans = runCMD('python testPython.txt', 'test', '')
    print(ans)

    # ans = runCMD('bash testBash.txt', 'test', '')
    # print(ans)