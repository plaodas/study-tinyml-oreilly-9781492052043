# 第 5 章 Hello World メモ

## この章の目的

- TensorFlow LiteのC++での使い方

## キーアイデア

- （読み進めながら箇条書きで）

## やってみたこと

- [x] TensorFlow Liteのコードをclone
- [x] hello_world_testのコードを確認
- [x] hello_world_testをmake
- [x] hello_worldをmake


## 疑問・メモ

- 疑問:
- メモ:
  - 最新のmasterは構造が異なるのでworkingTreeを復元
    ```bash
    $ git clone https://github.com/tensorflow/tensorflow.git
    $ cd tensorflow
    $ git rev-parse --verify --quiet be4f6874533d78f662d9777b66abe3cdde98f901
    $ git checkout be4f6874533d78f662d9777b66abe3cdde98f901 
    ```
  - hello_world_testのmake
    ```bash
    ~/work/src/tensorflow$ make -f tensorflow/lite/experimental/micro/tools/make/Makefile test_hello_world_test
    ```
  - hello_worldのmake
    ```bash
    ~/work/src/tensorflow$ make -f tensorflow/lite/experimental/micro/tools/make/Makefile hello_world
    ```
    - コアダンプ（core dumped）が発生するのでkTensorArenaSizeを2KBから4KBに変更
    ```diff
    # tensorflow/lite/experimental/micro/examples/hello_world/main_functions.cc
    - constexpr int kTensorArenaSize = 2 * 1024;
    + constexpr int kTensorArenaSize = 4 * 1024;
  
    ```