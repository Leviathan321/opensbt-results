#!/bin/bash
set -euo pipefail

# ---------------- Configuration ----------------
BASE_DIR="../opensbt-results/judge-eval/request_response/navi-judge-analysis-25-10-25-two-runs"
GT_CSV="../opensbt-results/human-aggregated/equal_aggregated_mean/question/survey_results_aggregated.csv"
SAVE_DIR="./judge-eval/tmp"

mkdir -p "$SAVE_DIR"

# List of sample configurations and runs
SAMPLES=("sample-1-majority" "sample-3-majority")
RUNS=("run1" "run2" "run3" "run4" "run5" "run6" "run7")

echo "===================================================="
echo " Running evaluation for all samples and runs"
echo " Save directory : $SAVE_DIR"
echo " Ground truth   : $GT_CSV"
echo "===================================================="
echo

# ---------------- Main loop ----------------
for SAMPLE in "${SAMPLES[@]}"; do
  for RUN in "${RUNS[@]}"; do
    RUN_DIR="${BASE_DIR}/${SAMPLE}/${RUN}/${SAMPLE}-${RUN}"

    # Pick the CSV file containing 'validation-repeat' in its name
    CSV_PATH=$(find "$RUN_DIR" -maxdepth 1 -type f -name "*validation-repeat*.csv" | head -n 1)

    if [[ -f "$CSV_PATH" ]]; then
      OUT_DIR="${SAVE_DIR}/${SAMPLE}/${RUN}"
      mkdir -p "$OUT_DIR"

      echo "▶ Evaluating: ${SAMPLE} - ${RUN}"
      python -m scripts.evaluate_accuracy_judge_gt \
        --csv_path "$CSV_PATH" \
        --gt_csv_path "$GT_CSV" \
        --json_output_path "${OUT_DIR}/evaluation_results.json" \
        --plot_errors_file "${OUT_DIR}/prediction_errors.png" \
        --plot_efficiency_file "${OUT_DIR}/model_efficiency.png" \
        --plot_f1_file "${OUT_DIR}/model_f1_score.png" \
        > "${OUT_DIR}/run.log" 2>&1

      echo "   ✔ Done. Logs saved in ${OUT_DIR}/run.log"
    else
      echo "   ⚠ No validation-repeat CSV found in ${RUN_DIR}"
    fi
  done
done

echo
echo "===================================================="
echo "All evaluations completed. Results saved under:"
echo "→ ${SAVE_DIR}"
echo "===================================================="