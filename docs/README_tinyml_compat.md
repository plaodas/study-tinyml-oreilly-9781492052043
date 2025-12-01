TFLite Support example (tinyml-compat)

This folder contains a lightweight example notebook `tflite_support_example.ipynb` that demonstrates safe usage of `tensorflow_lite_support`.

Quick steps to run the notebook in JupyterLab:

1. Activate the environment (or open a terminal where conda is initialized):

```bash
# If you installed Miniforge to $HOME/miniforge as done earlier
source $HOME/miniforge/etc/profile.d/conda.sh
conda activate tinyml-compat
```

2. Start JupyterLab (or open VS Code and select the notebook):

```bash
jupyter lab
# or
code .  # then open the notebook and select the kernel
```

3. In the notebook UI, select the kernel named `Python (tinyml-compat)` (this kernel was created when `ipykernel` was installed into the `tinyml-compat` environment).

4. Run the cells. The notebook will:
   - Import `tensorflow_lite_support` and list its top-level modules (safe).\n   - Run a tiny numeric demo (no model file required).\n   - Provide instructions to run metadata examples if you set a `.tflite` model path.

Notes and troubleshooting:
- If `tensorflow_lite_support` fails to import, re-check that you're using the `tinyml-compat` kernel and that the environment is activated.
- `tflite_support` (a different top-level package) may still conflict with TensorFlow in the same interpreter due to binary-level pybind registration collisions (StatusCode). If you need `tflite_support`, run it in a separate process or container and exchange data via files or IPC.

If you'd like, I can:
- Add a short wrapper script that runs `tflite_support` in a subprocess and returns JSON results.
- Add a sample `.tflite` model and a metadata demo cell that reads and prints model metadata.

