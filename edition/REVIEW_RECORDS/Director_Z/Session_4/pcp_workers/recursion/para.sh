#!/bin/bash
# para.sh K N TASKFILE : level K reads the task as given to it, must RESTATE it in its own words for the next level
# (no copying of the text), and relays the answer upward unchanged. The deepest level solves the task.
K=$1; N=$2; TF=$3; D=$(dirname "$0")
echo "$K down $(date +%s)" >> $D/log.txt
if [ "$K" -ge "$N" ]; then
  P="You are the last worker in a chain. Read the task in the file $TF, solve it exactly with a short Python program run in the shell, and reply with ONLY the answer line in the format the task asks for."
else
  NEXT=$((K+1)); NF=$D/task_level$NEXT.txt
  P="You are level $K of $N in a delegation chain. Read the task in the file $TF. Write a restatement of it IN YOUR OWN WORDS (do not copy sentences; a different person must be able to solve it from your text alone) to the file $NF . Then run this shell command once and wait: timeout $(( (N-K)*200 )) bash $D/para.sh $NEXT $N $NF . Reply with ONLY the last line it printed. If it fails reply FAILED-AT-$NEXT."
fi
OUT=$(timeout $(( (N-K+1)*200 )) claude -p "$P" --allowedTools Bash Write Read 2>&1 | tail -1)
echo "$K up $(date +%s) $OUT" >> $D/log.txt
echo "$OUT"
