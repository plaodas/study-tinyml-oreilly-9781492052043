from pathlib import Path
import numpy as np
import tensorflow as tf

ROOT = Path(__file__).resolve().parents[2]
DATA_PROCESSED = ROOT / "data" / "processed"
MODELS_SAVED = ROOT / "models" / "saved"

def load_npz(name: str):
    data = np.load(DATA_PROCESSED / f"{name}.npz")
    return data["x_train"], data["y_train"], data["x_test"], data["y_test"]

def build_simple_mlp(input_shape, num_classes):
    model = tf.keras.Sequential(
        [
            tf.keras.layers.InputLayer(input_shape=input_shape),
            tf.keras.layers.Dense(32, activation="relu"),
            tf.keras.layers.Dense(16, activation="relu"),
            tf.keras.layers.Dense(num_classes, activation="softmax"),
        ]
    )
    model.compile(
        optimizer="adam",
        loss="sparse_categorical_crossentropy",
        metrics=["accuracy"],
    )
    return model

def main(dataset_name: str, epochs: int = 20, batch_size: int = 32):
    x_train, y_train, x_test, y_test = load_npz(dataset_name)
    model = build_simple_mlp(input_shape=x_train.shape[1:], num_classes=len(np.unique(y_train)))

    model.fit(
        x_train,
        y_train,
        validation_data=(x_test, y_test),
        epochs=epochs,
        batch_size=batch_size,
    )

    MODELS_SAVED.mkdir(parents=True, exist_ok=True)
    model_path = MODELS_SAVED / f"{dataset_name}_model.h5"
    model.save(model_path)
    print(f"Saved model to {model_path}")

if __name__ == "__main__":
    # 例: python -m src.training.train_model --dataset_name wake_word
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument("--dataset_name", type=str, required=True)
    parser.add_argument("--epochs", type=int, default=20)
    parser.add_argument("--batch_size", type=int, default=32)
    args = parser.parse_args()

    main(args.dataset_name, args.epochs, args.batch_size)