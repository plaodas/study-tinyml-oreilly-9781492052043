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


## ノートブックでモデル作成
- /content にデータを作成するので作業ディレクトリ作成
```bash
mkdir -p ~/work/Oreilly_TinyML/content
sudo ln -s ~/work/Oreilly_TinyML/content /content
```

- TesorFlow<=1.15が必要なので、python3.7の環境をdockerで作成、作業ディレクトリをマウントしてコンテナで作業
```bash
docker run -it --rm -v "$PWD":/workspace -w /workspace tensorflow/tensorflow:1.15.5-py3 bash
```

- dockerコンテナの環境でnotebookwp実行する
ホストOSで
```bash
cd /home/agake/work/Oreilly_TinyML

docker run -it --rm -p 8888:8888 \
-v "/home/agake/work/Oreilly_TinyML":/workspace \
-v "/home/agake/work/src/tensorflow":/workspace/tensorflow \
-w /workspace \
tensorflow/tensorflow:1.15.5-py3
bash -c "apt-get update -qq && apt-get install -y -qq xxd && \
pip install -q notebook tf-estimator-nightly==1.14.0.dev2019072901 && \
mkdir -p /workspace/content && (ln -s /workspace/content /content || true) && \
jupyter notebook --ip=0.0.0.0 --no-browser --allow-root --notebook-dir=/workspace"
```
ブラウザでアクセス
http://127.0.0.1:8888/?token=<tokennnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnn>

`!python tensorflow/tensorflow/examples/speech_commands/...`
を
`!python /workspace/tensorflow/tensorflow/examples/speech_commands/...`
に修正して実行
