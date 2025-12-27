# 第 7 章 Wake-Word Detection メモ

## この章の目的

- ウェイクワード（音声トリガー）検出のパイプラインを理解する
- オーディオ特徴量（MFCC など）の扱いに慣れる
- 低リソース環境での音声モデルを体験する

## キーアイデア

- （読み進めながら箇条書きで）

## やってみたこと

- [x] 本のサンプルコードを PC 上で動かす
- [x] 学習済みモデルを TFLite に変換する
- [x] Arduino へデプロイして、実機でテストする

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

  - arduinoにデプロイ
  ```bash
  arduino-cli compile --fqbn arduino:mbed_nano:nano33ble ~/Arduino/libraries/Arduino_TensorFlowLite/examples/micro_speech
  arduino-cli upload --fqbn arduino:mbed_nano:nano33ble -p /dev/ttyACM0 ~/Arduino/libraries/Arduino_TensorFlowLite/examples/micro_speech
  ```
- 結果:
  ```bash
  (base) agake@yogi:~/work/Oreilly_TinyML$ arduino-cli monitor -p /dev/ttyACM0 --config 115200
  Monitor port settings:
    baudrate=115200
    bits=8
    dtr=on
    parity=none
    rts=on
    stop_bits=1

  Connecting to /dev/ttyACM0. Press CTRL-C to exit.
  Heard yes (215) @31872ms
  Heard unknown (217) @32960ms
  Heard yes (222) @34816ms
  Heard no (209) @43264ms
  Heard yes (244) @48064ms
  Heard yes (254) @71584ms
  Heard no (219) @85568ms
  Heard yes (213) @90720ms
  Heard unknown (217) @102112ms
  Heard no (228) @118304ms
  Heard no (210) @138528ms
  Heard unknown (202) @148096ms
  Heard no (207) @149920ms
  Heard no (214) @168320ms
  Heard no (228) @180832ms
  Heard yes (207) @189664ms
  Heard no (206) @231936ms
  Heard yes (240) @249600ms
  Heard yes (201) @252928ms
  Heard no (229) @254016ms
  Heard unknown (204) @258784ms
  Heard no (210) @274976ms
  Heard no (207) @293376ms
  Heard no (219) @297408ms
  Heard yes (207) @326080ms
  Heard no (211) @332352ms
  Heard yes (231) @342656ms
  Heard no (204) @344864ms
  Heard no (209) @347424ms
  Heard no (210) @363968ms
  Heard no (201) @371712ms
  Heard no (222) @386784ms
  Heard yes (210) @389344ms
  Heard no (210) @401856ms
  ```
