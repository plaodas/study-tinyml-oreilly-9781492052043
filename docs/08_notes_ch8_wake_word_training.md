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

😲Convert the modelでAbortがおきる
チェックポイントの重みがNaN（および量子化用 min/max が 0/NaN）になっているため、freeze→toco の量子化で scale=0/NaN になり abort しています。
対処は「まず量子化をオフにして安定した float モデルを出す → 必要なら後処理量子化（代表データでキャリブレーション）」です。
1. 学習設定を変更して再学習（まず --quantize=0、学習率を下げる）
- ノートブックの env を変更（例）:
```
os.environ["TRAINING_STEPS"]="15000,3000"
os.environ["LEARNING_RATE"]="0.0005,0.0001"
```
- 再学習コマンド（コンテナ内で実行）:
```
python /workspace/tensorflow/tensorflow/examples/speech_commands/train.py \
  --model_architecture=tiny_conv --window_stride=20 --preprocess=micro \
  --wanted_words=${WANTED_WORDS} --silence_percentage=25 --unknown_percentage=25 \
  --quantize=0 --verbosity=WARN --how_many_training_steps=${TRAINING_STEPS} \
  --learning_rate=${LEARNING_RATE} --summaries_dir=/content/retrain_logs \
  --data_dir=/content/speech_dataset --train_dir=/content/speech_commands_train
```

2. 学習中に NaN が出ていないかログ/TensorBoard を確認（/content/retrain_logs をチェック）。
3. 学習後にチェックポイントを再検査（NaN が無いことを確認）:
```
python - <<'PY'
import os, numpy as np, tensorflow as tf
s=os.environ.get('TOTAL_STEPS','18000')
ckpt=f"/content/speech_commands_train/tiny_conv.ckpt-{s}"
r=tf.train.NewCheckpointReader(ckpt)
for n in sorted(r.get_variable_to_shape_map().keys()):
    v=r.get_tensor(n); print(n, np.nanmin(v), np.nanmax(v), np.isnan(v).sum())
PY
```

4. float で freeze → tflite に変換（まず動作確認）:
```
python /workspace/tensorflow/tensorflow/examples/speech_commands/freeze.py \
  --model_architecture=tiny_conv --window_stride=20 --preprocess=micro \
  --wanted_words=${WANTED_WORDS} --quantize=0 --output_file=/content/tiny_conv_float.pb \
  --start_checkpoint=/content/speech_commands_train/tiny_conv.ckpt-${TOTAL_STEPS}

!toco \
 --graph_def_file=/content/tiny_conv_float.pb --output_file=/content/tiny_conv_float.tflite \
 --input_shapes=1,49,40,1 --input_arrays=Reshape_2 --output_arrays=labels_softmax \
 --inference_type=FLOAT
```

5. 必要なら後処理量子化（代表データを使う、Python API 推奨）:
- Floatへ変換
```shell
python - <<'PY'
import tensorflow as tf
converter = tf.lite.TFLiteConverter.from_frozen_graph(
  '/content/tiny_conv_float.pb',
  input_arrays=['Reshape_2'],
  output_arrays=['labels_softmax'],
  input_shapes={'Reshape_2':[1,49,40,1]}
)
tflite_model = converter.convert()
open('/content/tiny_conv_float.tflite','wb').write(tflite_model)
print('wrote /content/tiny_conv_float.tflite')
PY
ls -lh /content/tiny_conv_float.tflite
```

- 量子化-1 代表データ作成
 AudioProcessor がノートブック／スクリプトで使っている「前処理」を提供します。代表データは学習時と同じ前処理を通した実データ（通常は validation/testing のサンプル）を使うのが最良です。下記はコンテナ内でそのまま動く、AudioProcessor.get_data() を使った代表データジェネレータ付きの例スクリプトです（micro / mfcc 等、学習時の model_settings に合わせて動きます）。

学習で使った前処理を必ず使う（ここでは AudioProcessor の処理）
代表データは augmentation を入れない（background_volume=0, time_shift=0）かつ mode='validation'/'testing' を使う
100〜500 サンプル程度で十分（100 推奨）
実行スクリプト（コンテナ内で実行）:
```shell
python - <<'PY'
import sys
sys.path.insert(0, '/workspace/tensorflow/tensorflow/examples/speech_commands')

import os, numpy as np, tensorflow as tf
from tensorflow.python.platform import gfile
import input_data, models

# 環境変数 / ノートブックと同じ設定を使ってください
WANTED_WORDS = os.environ.get('WANTED_WORDS','yes,no')
DATA_DIR = '/content/speech_dataset'
SUMMARIES_DIR = '/content/retrain_logs'
TRAIN_DIR = '/content/speech_commands_train'

# モデル設定を train と同じに作る
model_settings = models.prepare_model_settings(
    len(input_data.prepare_words_list(WANTED_WORDS.split(','))),
    sample_rate=16000, clip_duration_ms=1000,
    window_size_ms=30.0, window_stride_ms=20.0,  # ← ここを 20.0 に
    feature_bin_count=40, preprocess='micro'
)

# セッション作って AudioProcessor 初期化（data_dir が既にある想定）
sess = tf.compat.v1.InteractiveSession()
audio_processor = input_data.AudioProcessor(
    None, DATA_DIR, 25, 25, WANTED_WORDS.split(','), 10, 10,
    model_settings, SUMMARIES_DIR)

# helper: fingerprint shape
fingerprint_size = model_settings['fingerprint_size']
fingerprint_width = model_settings['fingerprint_width']
frames = fingerprint_size // fingerprint_width  # これが 49 になるはず

# 代表データジェネレータ（validation セットから先頭 N を使う）
N = 200
def representative_gen():
    for i in range(N):
        data, labels = audio_processor.get_data(
            1, i, model_settings, background_frequency=0.0,
            background_volume_range=0.0, time_shift=0, mode='validation', sess=sess)
        # data は (1, fingerprint_size) flattened
        # representative_gen の reshape も (1,49,40,1) に合わせる
        arr = data.reshape(1, frames, fingerprint_width, 1).astype(np.float32)
        yield [arr]

converter = tf.lite.TFLiteConverter.from_frozen_graph(
    '/content/tiny_conv_float.pb',
    input_arrays=['Reshape_2'],
    output_arrays=['labels_softmax'],
    input_shapes={'Reshape_2':[1,frames,fingerprint_width,1]}
)

converter.optimizations = [tf.lite.Optimize.DEFAULT]
converter.representative_dataset = representative_gen
converter.inference_input_type = tf.uint8
converter.inference_output_type = tf.uint8

tflite_quant = converter.convert()
open('/content/tiny_conv_quant_from_audio.tflite','wb').write(tflite_quant)
print('wrote /content/tiny_conv_quant_from_audio.tflite')
PY
ls -lh /content/tiny_conv_quant_from_audio.tflite
```


- 再学習実行
```shell
export WANTED_WORDS="yes,no"
export TRAINING_STEPS="15000,3000"
export LEARNING_RATE="0.0005,0.0001"
python /workspace/tensorflow/tensorflow/examples/speech_commands/train.py \
  --model_architecture=tiny_conv --window_stride=20 --preprocess=micro \
  --wanted_words=${WANTED_WORDS} --silence_percentage=25 --unknown_percentage=25 \
  --quantize=0 --verbosity=WARN --how_many_training_steps=${TRAINING_STEPS} \
  --learning_rate=${LEARNING_RATE} --summaries_dir='' \
  --data_dir=/content/speech_dataset --train_dir=/content/speech_commands_train \
  --check_nans=True
  ```

