# 第 7 章 Wake-Word Detection メモ

## この章の目的

- ウェイクワード（音声トリガー）検出のパイプラインを理解する
- オーディオ特徴量（MFCC など）の扱いに慣れる
- 低リソース環境での音声モデルを体験する

## キーアイデア

- （読み進めながら箇条書きで）

## やってみたこと

- [ ] 本のサンプルコードを PC 上で動かす
- [ ] 学習済みモデルを TFLite に変換する
- [ ] Arduino へデプロイして、実機でテストする

## 疑問・メモ

- memo:
  - testのコンパイルと実行
  ```bash
  make -f src/tensorflow/lite/experimental/micro/tools/make/Makefile audio_provider_mock_test feature_provider_test audio_provider_test micro_speech_test command_responder_test recognize_commands_test feature_provider_mock_test

  ./tensorflow/lite/experimental/micro/tools/make/gen/linux_x86_64/bin/audio_provider_mock_test
  ./tensorflow/lite/experimental/micro/tools/make/gen/linux_x86_64/bin/feature_provider_test
  ./tensorflow/lite/experimental/micro/tools/make/gen/linux_x86_64/bin/audio_provider_test
  ./tensorflow/lite/experimental/micro/tools/make/gen/linux_x86_64/bin/micro_speech_test
  ./tensorflow/lite/experimental/micro/tools/make/gen/linux_x86_64/bin/command_responder_test
  ./tensorflow/lite/experimental/micro/tools/make/gen/linux_x86_64/bin/recognize_commands_test
  ./tensorflow/lite/experimental/micro/tools/make/gen/linux_x86_64/bin/feature_provider_mock_test
  ```
- 応用アイデア:
  -
