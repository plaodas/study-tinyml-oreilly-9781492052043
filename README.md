# TinyML (O'Reilly, ISBN: 978-1-492-05204-3) Playground

O'Reilly 本 『TinyML: Machine Learning with TensorFlow Lite on Arduino and Ultra-Low-Power Microcontrollers』
(ISBN: 978-1-492-05204-3) を使って学習するための実験用リポジトリです。

## ゴール

- 本の内容を一通り手を動かして追体験する
- センサデータの収集 → 前処理 → 学習 → 量子化 → マイコンへのデプロイを一通り体験する
- 実験コードやノートを残し、あとから振り返れるようにする

## ディレクトリ構成

```text
.
├── notebooks/      # 各章に対応したノートブック
├── data/           # データ (raw: 生データ, processed: 前処理後)
├── models/         # 学習済みモデルや実験ログ
├── src/            # 再利用しやすいスクリプト群
└── docs/           # 読書ノートやメモ
```

## セットアップ

Conda を使う場合:

```bash
conda env create -f environment.yml
conda activate tinyml
```

pip のみの場合:

```bash
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\\Scripts\\activate
pip install -r requirements.txt
```

## 学習の進め方

1. `docs/00_study_plan.md` に自分用の学習計画を書く
2. 本を読み進めつつ、各章に対応したノートブック例を開く  
   - 例: 第 3 章 → `notebooks/03_ch3_speech_wake_word.ipynb`
3. 各章の理解・気づき・疑問は `docs/0X_notes_chX_*.md` にメモ
4. 実験コードは可能な限り `src/` に切り出し、ノートブックから呼び出すだけにする
5. 実機ボード (Arduino / ほか) 向けのコードや設定は `src/deployment/` 以下にまとめる

## ブランチ運用の例

- `main`: 本のベースに忠実な実装
- `exp/*`: 色々試してみる実験ブランチ
  - 例: `exp/try-different-architecture`, `exp/quantization-aware-training`

---