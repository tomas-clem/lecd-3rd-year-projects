# Facial Emotion Recognition — Feature Engineering

Classifies the emotion expressed by actors in video (8 classes: neutral, calm, happy, sad, angry, fearful, disgust, surprised) from the 68 facial landmarks tracked in each frame. The focus is the feature engineering pipeline: exploring the data, finding outliers, testing which features separate the emotions, extracting time and frequency features, and selecting or transforming them before classification.

*Developed with Afonso Cordeiro. Course: Feature Engineering, University of Coimbra, 2023/24.*

## Dataset

Facial landmark tracking of the 24 actors of the [RAVDESS](https://zenodo.org/records/1188976) dataset, provided by the course. It is not included in this repository. The data loading code at the top of the notebook was provided by the instructor (Marco Simões).

## Pipeline

The notebook [emotion_recognition.ipynb](emotion_recognition.ipynb) keeps all its outputs and follows the assignment's numbering.

1. **Exploration:** landmark trajectories and statistics per emotion.
2. **Outliers:** z-score thresholds, k-means and DBSCAN on landmark positions.
3. **Statistical tests:** Shapiro–Wilk and Kolmogorov–Smirnov for normality, then ANOVA or Kruskal–Wallis to find features that differ between emotions.
4. **Feature extraction:**
   - geometric features (eye and mouth opening, mouth angles);
   - frequency features with the FFT, the STFT (Hann window, 50 samples, 80% overlap) and the DFT.
5. **Feature reduction:** PCA (2 components explain 75% of the variance), plus selection with the Fisher score and ReliefF.
6. **Classification:** SVM, evaluated with 30 random 70/30 splits and with leave-one-subject-out (LOSO).

## Results

Mean F1-score over 8 emotions. Random guessing gives about 0.125.

| Features | 70/30 splits | Leave-one-subject-out |
|---|---:|---:|
| Time-domain, full set | 0.36 | 0.35 |
| Time-domain, PCA | 0.56 | see limitations |
| Time-domain, ReliefF selection | 0.32 | see limitations |
| Frequency (STFT), full set | 0.36 | 0.23 |
| Frequency, PCA | 0.56 | see limitations |
| Frequency, ReliefF selection | 0.21 | see limitations |

## Known limitations

These issues were found in a later review. The code is kept as submitted.

- `SVMloso()` ignores its feature argument and uses the global feature matrix, so the leave-one-subject-out results for PCA and ReliefF do not correspond to those feature sets.
- In the 70/30 splits, frames from the same actor land in both training and test sets, which makes those scores optimistic. The LOSO scores are the realistic ones.
- The z-score normalisation for PCA is computed on the whole dataset before splitting.
