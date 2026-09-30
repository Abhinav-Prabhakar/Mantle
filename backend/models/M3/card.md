# M3 dyno card classifier
1-D CNN, 174,092 parameters, 12 classes, temperature-scaled (T=0.63), exported to ONNX (`model.onnx`).
**Source: physics_synthetic** (S4 cards from the Gibbs wave-equation synthesiser, 54,000 training cards, 12 epochs on CPU).
No real dynamometer cards were available; the test sets are also synthetic, so scores measure separability of the generator's classes.
- Input: 8 x 128 (surface pos/load, computed downhole pos/load with default damping 0.1, log load range, mean/range, position range, spm).
- Metrics: {"macro_f1_cnn": 0.9390647495092574, "macro_f1_fourier_knn": 0.5866238814811896, "macro_f1_perturbed_cnn": 0.8532990153221509, "macro_f1_perturbed_fourier_knn": 0.4317669180237494, "ece_after_temperature": 0.011599113682905853, "temperature": 0.6345338821411133, "params": 174092, "n_train": 54000, "n_test": 12000, "epochs": 12}. "Perturbed" = independent draws with time warp, position non-linearity, load ripple and gain the training set never saw (stand-in for the hand-labelled set, which does not exist).
- Baseline: 16 Fourier-descriptor magnitudes + log load range, 5-NN (20k cards).
- Impact index: `impact_index(pos, load)` = steepest 3-sample downstroke load drop (index, x, drop kN, severity) used by M5.
- Limits: classes are physics-generated and idealised; real cards with unmodelled faults will be over-confident despite temperature scaling.
