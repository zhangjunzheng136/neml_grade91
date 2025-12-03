# Application of NEML for Grade 91 Steel

This repository serves to showcase and backup my application of the [NEML (Nuclear Engineering Material Model Library)](https://github.com/Argonne-National-Laboratory/neml). Currently, it implements the constitutive model for **Grade 91 steel** based on the following reference: https://www.osti.gov/biblio/1480525.

This constitutive model accounts for the interaction between plasticity and viscoplasticity, as well as isotropic and kinematic hardening. It is recommended by **ASME BPVC III.5 HBB-Z**.

*Acknowledgements: Special thanks to the authors of the NEML library and the constitutive model for their work.*

## 💻 Environment

This library runs best in a **Linux** environment. I have successfully run and debugged it using **Windows Subsystem for Linux 2 (WSL 2)**.

For the full NEML installation guide, please refer to: https://neml.readthedocs.io/en/main/started.html.

## 🚀 Quick Start (Python Bindings Only)

If you only wish to test this Python script, installing the Python bindings is sufficient and the process is simpler. Follow the steps below:

### 1. Prepare Linux Environment
If you are on Windows, use **WSL 2**.
* Installation guide: https://learn.microsoft.com/en-us/windows/wsl/install
* *Note: By default, this will install to the C drive.*
* The following example uses a fresh install of **WSL 2 Ubuntu 24.04**.

### 2. Update Environment & Install Dependencies
Update the system and install basic tools (wget, pip):

sudo apt-get update
sudo apt-get install wget ca-certificates
sudo apt install python3-pip

Install Miniconda: Please refer to the official guide: Miniconda Installation for Linux

Accept Conda terms:

conda tos accept --override-channels --channel [https://repo.anaconda.com/pkgs/main](https://repo.anaconda.com/pkgs/main)
conda tos accept --override-channels --channel [https://repo.anaconda.com/pkgs/r](https://repo.anaconda.com/pkgs/r)
Install BLAS and LAPACK in your desired Conda environment:


conda install conda-forge::blas
conda install conda-forge::lapack
### 3. Install NEML Python Bindings
Install system dependencies and the neml package:


sudo apt-get install python3-dev python3-pip cmake libboost-dev libblas-dev liblapack-dev
pip install neml
✅ Validation
Once the environment is set up, the Grade 91 implementation should work. The validation source is based on the examples provided by the model author: https://www.osti.gov/biblio/1601806.

⚠️ Important Configuration Note: To perform the validation correctly, you must adjust the solver configuration in the NEML library source code. Locate the drivers.py file in the neml library and change: solvers = [s1,s3] to solvers = [s1,s3,s2]

Results Interpretation: In the output images:

Black line: Calculated values from this Python script.

Red line: Reference values provided by the model (and NEML) author (see strain.txt, stress.txt, temperature.txt, time.txt).

📝 Future Usage
Before applying this to Finite Element Analysis (FEA) problems, consideration is needed regarding how the FEA software invokes this model.

----------------------------------------------------------------------------------------------------------

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
