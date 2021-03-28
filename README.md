# Mado

基于 mirai, Graia 的 QQ 机器人

> 项目名称来源于《[魔法少女小圆](https://mzh.moegirl.org.cn/%E9%AD%94%E6%B3%95%E5%B0%91%E5%A5%B3%E5%B0%8F%E5%9C%86)》 [鹿目**圆**香](https://mzh.moegirl.org.cn/%E9%B9%BF%E7%9B%AE%E5%9C%86)（Kaname **Mado**ka）。
> **Ma**do**ka**与 **Mat**hemati**ca** 的最长公共子序列长度竟然达到了 4（**d** 与 **t**，**k** 与 **c** 各记为半个公共字符长度），这种事绝对很奇怪啊。
> 
> ~~圆：我被绑架到中国科大当 bot 样本。~~

### 特点

+ 可以执行 python3 和 Mathematica 代码（通过命令行调用 python 和 wolframscript）
+ 支持以图片格式输入 Mathematica 代码，支持以 PNG/GIF 格式输出 Mathematica 的计算结果
+ 可以给出错误提示，有执行时间限制
+ 支持好友访问和群访问

### 不足

- 权限管理部分薄弱

## 指令及选项

### 指令

| 指令                        | 含义                     |
|:------------------------- |:---------------------- |
| **epy** *opts*  \n *code* | ExecutePython3         |
| **ema** *opts*  \n *code* | ExecuteMathematica     |
| **esh** *opts*  \n *code* | ExecuteBash（需要权限，存在漏洞） |
| **pip install** *opts*    | Python 库安装             |
| **help**                  | 帮助                     |

### 选项

| 选项               | 含义                     |
|:---------------- |:---------------------- |
| **-p**           | 以 PNG 格式返回（**ema** 专用） |
| **-g**           | 以 GIF 格式返回（**ema** 专用） |
| **-t** *seconds* | 修改时间限制（默认 15 秒，需要权限）   |
| **-o**           | 不对输出字符数及行数进行限制（需要权限）   |

## 示例

### **epy** 的使用

```python
epy
for i in range(5):
 if i%3==1:
  print(i)
```

结果为：

> 1
> 4

### **ema** 的使用

#### 文本格式输出

```wolfram
ema
f[1]=f[2]=1;
f[n_]:=f[n]=f[n-1]+f[n-2];
Array[f,10]
f[100]
```

结果为：

> {1, 1, 2, 3, 5, 8, 13, 21, 34, 55}
> 354224848179261915075

#### 图像格式输出

```wolfram
ema -p
PolarPlot[Sin[5t/3],{t,0,3Pi},ColorFunction->(Hue[#3]&),ImageSize->{900,900}]
```

结果为：   

> <img title="" src="image/ema%20-p.png" alt="" width="300">

## 作出贡献

欢迎提出建议，欢迎 pull request  
项目地址：<https://github.com/GWDx/mado>

## 关于协议

本仓库基于的项目 [mirai](https://github.com/mamoe/mirai) 和 [graia](https://github.com/GraiaProject/Application) 均使用 AGPL 协议。

## 鸣谢

感谢以下开源项目：

+ [mirai](https://github.com/mamoe/mirai)
+ [mirai-console](https://github.com/mamoe/mirai-console)
+ [mirai-console-loader](https://github.com/iTXTech/mirai-console-loader)
+ [mirai-login-solver-selenium](https://github.com/project-mirai/mirai-login-solver-selenium)
+ [mirai-api-http](https://github.com/project-mirai/mirai-api-http)
+ [graia](https://github.com/GraiaProject/Application)

同时感谢 [中国科学技术大学 Vlab 实验平台](https://vlab.ustc.edu.cn/) 提供运行环境