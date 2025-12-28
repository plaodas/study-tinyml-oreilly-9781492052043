# 第 8 章 Wake-Word Detection メモ

## この章の目的

- ウェイクワード（音声トリガー）のモデルを理解する
- 音声コマンドを学習させる

## キーアイデア



## やってみたこと

- [] 本のサンプルコードを PC 上で動かす

## 疑問・メモ

- 環境再構築：
1. 必要パッケージをインストール（Ubuntu/Debian）
```bash
sudo apt update
sudo apt install -y make build-essential libssl-dev zlib1g-dev \
  libbz2-dev libreadline-dev libsqlite3-dev wget curl llvm \
  libncurses5-dev libncursesw5-dev xz-utils tk-dev libffi-dev \
  liblzma-dev git
```

2. pyenv をインストール
```bash
curl https://pyenv.run | bash
# シェル初期化（bash の例）
echo 'export PYENV_ROOT="$HOME/.pyenv"' >> ~/.bashrc
echo 'export PATH="$PYENV_ROOT/bin:$PATH"' >> ~/.bashrc
echo 'eval "$(pyenv init --path)"' >> ~/.bashrc
echo 'eval "$(pyenv init -)"' >> ~/.bashrc
# 新しいシェルを読み込むか以下を実行
source ~/.bashrc
```

3. Python 3.10 をインストールしてこのリポジトリで使う
```bash
pyenv install 3.10.16      # または好きな 3.10.x
cd /home/agake/work/Oreilly_TinyML
pyenv local 3.10.16        # このフォルダ内で Python 3.10 を使う
```

4. 仮想環境作成・有効化・依存インストール
```bash
python -m venv .venv
source .venv/bin/activate
pip install --upgrade pip setuptools
pip install -r requirements.txt
```
