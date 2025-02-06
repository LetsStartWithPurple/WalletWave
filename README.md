# WalletWave
WalletWave is a Python-based solana wallet scanner to boost your copy trade strategy! Designed to analyze transactions including, but not limited to PNL, trades, and account balances. Analyze at lighting speeds by scanning 1oo potentially winning wallets in 2 minutes or less! It is modular, which allows users to extend its functions with custom plugins. It's an additional tool to find Solana wallets that work well with your copy trading strategy. 

> **_DISCLAIMER_**  
> 
> Even though the wallets that WalletWave exports fit a criteria that may work for your strategy, it is best to still do your own research with additional solana tools such as Dex Screener, Birdeye.so, GMGN.ai, etc.

---
## Features
- Analyze SOLANA wallets
- View PNL (Profit and Loss), trades, and balances
- Modular plugin support
- CLI interface that works on both Windows and Linux
- Utilizes GMGN.ai to view winrate
- Exports to CSV or TXT file for additional analysis. 
---

## Installation

### Prerequisites
- **[Python 3.8+](https://www.python.org/)**
- **[pip](https://pip.pypa.io/en/stable/installation/)**
- **[Git](https://git-scm.com/book/en/v2/Getting-Started-Installing-Git)** (to clone repo)
- **Build Tools** (`pip install build`)
---

### Windows
#### Option 1: Using `make`
1. Install `make` via [Chocolatey](https://chocolatey.org/) or [GnuWin32](http://gnuwin32.sourceforge.net/).
2. Clone the repository
```bash
git clone  https://github.com/LetsStartWithPurple/WalletWave.git
```

3. Change Directory
```bash
cd WalletWave 
```

4. Install with make
```bash
make install
```

5. Activate virtual environment  
**Powershell**  ```.venv\Scripts\Activate.ps1```  
**Command Prompt** ```.venv\Scripts\activate.bat```  


6. Run WalletWave
```bash 
walletwave 
```
#### Option 2: Manual Installation (no make)  
1. Clone the repository
2. Navigate to project directory
3. Create virtual environment
```bash
python3 -m venv .venv
```

4. Activate virtual environment  
**Powershell**  ```.venv\Scripts\Activate.ps1```  
**Command Prompt** ```.venv\Scripts\activate.bat```
5. Install dependencies:
```bash
pip install --upgrade pip
```
```bash
pip install .
```

6. Run WalletWave:
```bash
walletwave 
```
---
### Linux
1. Clone the repository:
```bash
git clone https://github.com/LetsStartWithPurple/WalletWave.git
```

2. Navigate to directory
```bash
cd WalletWave 
```

3. Install with `make`:
```bash
make install  
```

4. Activate virtual environment
```bash
source .venv/bin/activate 
```

5. Run WalletWave
```bash
walletwave 
```

#### Preview Linux Install

![Linux Install](https://media2.giphy.com/media/v1.Y2lkPTc5MGI3NjExc3d2bXVyeHFjMXBnYTVhZ2RscTVqZWY4bm1kaG93cHh6eW5ndmY4MSZlcD12MV9pbnRlcm5hbF9naWZfYnlfaWQmY3Q9Zw/Bbw9TR9Ymo7cYDRcEL/giphy.gif)

# Plugin Development  
> See [Plugin Development Wiki](https://github.com/LetsStartWithPurple/WalletWave/wiki/2.-Plugin-Development) 
---

# Community
> - https://x.com/WalletWaveApp
> - [**Discord**](https://discord.gg/sunDQ8Xq)
> - [**GitHub Discussion**](https://github.com/LetsStartWithPurple/WalletWave/discussions)
> - **Program Issues:** [Report bugs](https://github.com/LetsStartWithPurple/WalletWave/issues)

---
# License
> This project is licensed under [CC0 1.0 Universal](https://github.com/LetsStartWithPurple/WalletWave/blob/main/LICENSE)

---
# Disclaimer
> WalletWave is for educational and informational purposes only. Always verify outputs using additional tools and your own research.

---
# Contributions
> We welcome code contributions! In fact we encourage it! If you'd like to help improve WalletWave, please see:
> - [Contributing Guidelines](https://github.com/LetsStartWithPurple/WalletWave/blob/main/CONTRIBUTING.md)
> - [Code of Conduct](https://github.com/LetsStartWithPurple/WalletWave/blob/main/CODE_OF_CONDUCT.md)
>
> We will never solicit money from our users, but if you would like to donate to the project, here is the Solana address.
> 
> Solana Wallet Address: 2NbHvVDjpNf8hG9aDjLom57Z1SwgH1G3wgih1amyLLzS
> 
> Thank you so much for your support! Just using WalletWave fills my heart with joy and is contribution enough!








