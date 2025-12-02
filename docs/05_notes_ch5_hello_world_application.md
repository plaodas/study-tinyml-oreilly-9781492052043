# 第 5 章 Hello World メモ

## この章の目的

- TensorFlow LiteのC++でのTestについて

## キーアイデア

- （読み進めながら箇条書きで）

## やってみたこと

- [ ] TensorFlow Liteのコードをclone

## 疑問・メモ

- 疑問:
  - 
- メモ:
  - 最新のmasterは構造が異なるのでworkingTreeを復元
    ```bash
    $ git clone https://github.com/tensorflow/tensorflow.git
    $ cd tensorflow
    $ git rev-parse --verify --quiet be4f6874533d78f662d9777b66abe3cdde98f901
    $ git checkout be4f6874533d78f662d9777b66abe3cdde98f901 
    ```