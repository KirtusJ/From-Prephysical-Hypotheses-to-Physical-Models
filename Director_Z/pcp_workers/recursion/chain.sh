#!/bin/bash
# chain.sh K N TOKEN : level K of a chain of N headless workers. Each level logs, calls the next, and relays the answer upward.
K=$1; N=$2; T=$3; D=$(dirname "$0")
echo "$K down $(date +%s.%N)" >> $D/log.txt
if [ "$K" -ge "$N" ]; then
  P="You are level $K, the deepest. Run this shell command and reply with exactly its output and nothing else: printf %s $T | sha256sum | cut -c1-12"
else
  NEXT=$((K+1)); TO=$(( (N-K)*150 ))
  P="You are level $K of $N in a relay test. Run this exact shell command once, wait for it to finish: timeout $TO bash $D/chain.sh $NEXT $N $T . Then reply with exactly the last line it printed and nothing else. If it fails or prints nothing, reply with the single word FAILED-AT-$NEXT."
fi
OUT=$(timeout $(( (N-K+1)*150 )) claude -p "$P" --allowedTools Bash 2>&1 | tail -1)
echo "$K up $(date +%s.%N) $OUT" >> $D/log.txt
echo "$OUT"
