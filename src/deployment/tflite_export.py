from pathlib import Path
import tensorflow as tf

ROOT = Path(__file__).resolve().parents[2]
MODELS_SAVED = ROOT / "models" / "saved"

def convert_to_tflite(model_name: str, quantize: bool = True):
    model_path = MODELS_SAVED / f"{model_name}_model.h5"
    model = tf.keras.models.load_model(model_path)

    converter = tf.lite.TFLiteConverter.from_keras_model(model)
    if quantize:
        converter.optimizations = [tf.lite.Optimize.DEFAULT]

    tflite_model = converter.convert()

    tflite_path = MODELS_SAVED / f"{model_name}.tflite"
    with open(tflite_path, "wb") as f:
        f.write(tflite_model)
    print(f"Saved TFLite model to {tflite_path}")

if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument("--model_name", type=str, required=True)
    parser.add_argument("--no_quantize", action="store_true")
    args = parser.parse_args()

    convert_to_tflite(args.model_name, quantize=not args.no_quantize)