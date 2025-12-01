#include <TensorFlowLite.h>
// TODO: 実際のボードやライブラリに合わせて include を調整する
// #include "model.h"  // Python 側で生成した C 配列形式のモデルをインクルード

void setup() {
  Serial.begin(115200);
  while (!Serial) { ; }

  Serial.println("TinyML inference demo (O'Reilly TinyML book)");
  // TODO: tflite マイクロインタプリタの初期化コードをここに書く
}

void loop() {
  // TODO: センサ値を読む → 入力テンソルにセット → 推論 → 結果をシリアル出力
  delay(1000);
  Serial.println("Loop...");
}