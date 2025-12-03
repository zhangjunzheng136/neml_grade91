这个库是为了展示和备份我对于neml库的应用。目前实现了91钢的本构模型https://www.osti.gov/biblio/1480525。
这个本构模型考虑了塑性和粘塑性的转变、各向同性硬化和运动硬化，被ASME BPVC III.5 HBB-Z推荐。
在此感谢该库和本构模型作者的工作。

该库在linux环境下运行较好，我实际在Windows Subsystem for Linux 2（WSL 2）下运行并调试成功。
neml安装见https://neml.readthedocs.io/en/main/started.html。
如果只是为了测试我的这个Python文件，可仅使用Python绑定，过程要简单一些，步骤如下：
1. 准备linux环境。Windows系统下可使用WSL2，见https://learn.microsoft.com/en-us/windows/wsl/install，注意它会默认安装在C盘。下面我是用空白的的WSL2 Ubuntu 24.04为例运行的。
2. 更新各环境并安装BLAS和LAPACK。具体命令：
更新：
sudo apt-get update
安装wget：
sudo apt-get install wget ca-certificates
安装pip：
sudo apt install python3-pip
安装conda：
见：https://www.anaconda.com/docs/getting-started/miniconda/install#linux-2
同意conda条款：
conda tos accept --override-channels --channel https://repo.anaconda.com/pkgs/main
conda tos accept --override-channels --channel https://repo.anaconda.com/pkgs/r
在想要的的conda环境下安装BLAS和LAPACK：
conda install conda-forge::blas
conda install conda-forge::lapack
3. 安装neml的python绑定：
sudo apt-get install python3-dev python3-pip cmake libboost-dev libblas-dev liblapack-dev
pip install neml

此时我的91钢的实现在该环境下可以运行。验证源为该本构模型作者给出的算例：https://www.osti.gov/biblio/1601806。
注意验证需调整求解器配置，即该neml库下drivers.py文件中，solvers = [s1,s3]改为solvers = [s1,s3,s2]
输出图片中黑线为本python脚本计算值，红线为该本构模型（也是neml库）作者给出的值，见strain.txt, stress.txt, temperature.txt, time.txt。
实际应用于有限元问题前，还需考虑有限元软件如何调用。