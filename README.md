# mado

> 基于 mirai, Graia 的 QQ 机器人

### 特点

+ 可以执行 python3 和 Mathematica 代码（通过调用 python 和 wolframscript）
+ 可以给出错误提示，有执行时间限制
+ 支持好友访问和群访问

### 不足

- 权限管理部分较为薄弱


## 指令

### (1)

  | 指令                      | 含义                             |
  |:--------------------------|:---------------------------------|
  | **epy** *opts*  \n *code* | ExecutePython3                   |
  | **ema** *opts*  \n *code* | ExecuteMathematica               |
  | **esh** *opts*  \n *code* | ExecuteBash（需要权限，存在漏洞）|
  | **pip install** *opts*    | Python 库安装                    |
  | **help**                  | 帮助                             |

### (2)

  |选项              |含义                                    |
  |:-----------------|:---------------------------------------|
  | **-p**           |以图片格式返回（**ema** 专用）          |
  | **-t** *seconds* |修改时间限制（默认 15 秒，需要权限）    |
  | **-o**           |不对输出字符数及行数进行限制（需要权限）|

## 示例

1. **epy** 的使用
```
epy
for i in range(5):
 if i%3==1:
  print(i)
```

结果为：
```
1
4
```


2. **ema** 的使用

+ (1) 文本格式输出
```
ema
f[1]=f[2]=1;
f[n_]:=f[n]=f[n-1]+f[n-2];
Array[f,10]
f[100]
```

结果为：
```
{1, 1, 2, 3, 5, 8, 13, 21, 34, 55}
354224848179261915075
```

+ (2) 图像格式输出
```
ema -p
PolarPlot[Cos[5t/3],{t,0,6Pi}]
```
结果为：![](./PolarPlot.png)


## 作出贡献

> 欢迎提出建议，欢迎 pull request

> 项目地址：<https://github.com/GWDx/mado>


## 关于协议
本仓库基于的项目 [mirai](https://github.com/mamoe/mirai) 和 [graia](https://github.com/GraiaProject/Application) 均使用 AGPL 协议


## 鸣谢

+ [mirai](https://github.com/mamoe/mirai)
+ [mirai-console](https://github.com/mamoe/mirai-console)
+ [mirai-console-loader](https://github.com/iTXTech/mirai-console-loader)
+ [mirai-login-solver-selenium](https://github.com/project-mirai/mirai-login-solver-selenium)
+ [mirai-api-http](https://github.com/project-mirai/mirai-api-http)
+ [graia](https://github.com/GraiaProject/Application)
