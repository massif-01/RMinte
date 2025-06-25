# Configuration files for model pull-ups in vLLM

---

### Enter folder & Start conda-vllm

```
cd Downloads/Qwen

conda activate vllm066p1
```

---

## Speculative Decoding with vLLM  [ Speculative token : 5 ]

### "Qwen2.5-72B-Instruct-AWQ" + "Qwen2.5-7B-Instruct-AWQ" | "memory-utilization=0.9" | "max-model-len=9000"

`vllm serve "/home/rm01/Downloads/Qwen/Qwen2.5-72B-Instruct-AWQ" --gpu-memory-utilization=0.9 --max-model-len=9000 --served-model-name "Qwen2.5-72B-Instruct-AWQ-Speculative-7B-9K" --enable-prefix-caching --use-v2-block-manager --enable-chunked-prefill --speculative-model "/home/rm01/Downloads/Qwen/Qwen2.5-7B-Instruct-AWQ" --num-speculative-token 5 --speculative-draft-tensor-parallel-size 1`

---

### "Qwen2.5-72B-Instruct-AWQ" + "Qwen2.5-3B-Instruct-AWQ" | "memory-utilization=0.9" | "max-model-len=24000"

`vllm serve "/home/rm01/Downloads/Qwen/Qwen2.5-72B-Instruct-AWQ" --gpu-memory-utilization=0.9 --max-model-len=24000 --served-model-name "Qwen2.5-72B-Instruct-AWQ-Speculative-3B-24K" --enable-prefix-caching --use-v2-block-manager --enable-chunked-prefill --speculative-model "/home/rm01/Downloads/Qwen/Qwen/Qwen2.5-3B-Instruct-AWQ" --num-speculative-token 5 --speculative-draft-tensor-parallel-size 1 --max_num_batched_tokens 256`

---

### "Qwen2.5-72B-Instruct-AWQ" + "Qwen2.5-1.5B-Instruct-AWQ" | "memory-utilization=0.82" | "max-model-len=24000"

`vllm serve "/home/rm01/Downloads/Qwen/Qwen2.5-72B-Instruct-AWQ" --gpu-memory-utilization=0.82 --max-model-len=24000 --served-model-name "Qwen2.5-72B-Instruct-AWQ-Speculative-1.5B-24K" --enable-prefix-caching --use-v2-block-manager --enable-chunked-prefill --speculative-model "/home/rm01/Downloads/Qwen/Qwen2.5-1.5B-Instruct-AWQ" --num-speculative-token 5 --speculative-draft-tensor-parallel-size 1 --max_num_batched_tokens 256`

---

### "Qwen2.5-72B-Instruct-AWQ" + "Qwen2.5-0.5B-Instruct-AWQ" | "memory-utilization=0.82" | "max-model-len=24000"

`vllm serve "/home/rm01/Downloads/Qwen/Qwen2.5-72B-Instruct-AWQ" --gpu-memory-utilization=0.82 --max-model-len=24000 --served-model-name "Qwen2.5-72B-AWQ-Spec-24K" --enable-prefix-caching --use-v2-block-manager --enable-chunked-prefill --speculative-model "/home/rm01/Downloads/Qwen/Qwen2.5-0.5B-Instruct-AWQ" --num-speculative-token 5 --speculative-draft-tensor-parallel-size 1 --max_num_batched_tokens 256`

---

### "Qwen2.5-32B-Instruct-AWQ" + "Qwen2.5-3B-Instruct-AWQ" | "memory-utilization=0.85" | "max-model-len=32000"

`vllm serve "/home/rm01/Downloads/Qwen/Qwen2.5-32B-Instruct-AWQ" --gpu-memory-utilization=0.85 --max-model-len=32000 --served-model-name "Qwen2.5-32B-Instruct-AWQ-Speculative-3B-32K"  --enable-prefix-caching --use-v2-block-manager --enable-chunked-prefill --speculative-model "/home/rm01/Downloads/Qwen/Qwen/Qwen2.5-3B-Instruct-AWQ" --num-speculative-token 5 --speculative-draft-tensor-parallel-size 1 --max_num_batched_tokens 256`

---

### "DeepSeek-R1-Distill-Qwen-32B-GPTQ-Int8" + "DeepSeek-R1-Distill-Qwen-1.5B" | "memory-utilization=0.88" | "max-model-len=32000"

`vllm serve "/home/rm01/Downloads/deepseek-ai/DeepSeek-R1-Distill-Qwen-32B-GPTQ-Int8" --gpu-memory-utilization=0.9 --max-model-len=32000 --served-model-name "DeepSeek-R1-Distill-Qwen-32B-Speculative-1.5B-32K" --enable-prefix-caching --use-v2-block-manager --enable-chunked-prefill --speculative-model "/home/rm01/Downloads/deepseek-ai/DeepSeek-R1-Distill-Qwen-1.5B" --num-speculative-token 5 --speculative-draft-tensor-parallel-size 1 --max_num_batched_tokens 256 --max-parallel-loading-workers=4 `

---

### "DeepSeek-R1-Distill-Qwen-32B-GPTQ-Int8" + "DeepSeek-R1-Distill-Qwen-1.5B-GTPQ-Int4" | "memory-utilization=0.8" | "max-model-len=32000"

`vllm serve "/home/rm01/Downloads/deepseek-ai/DeepSeek-R1-Distill-Qwen-32B-GPTQ-Int8" --gpu-memory-utilization=0.8 --max-model-len=32000 --served-model-name "DeepSeek-R1-Distill-Qwen-32B-Speculative-1.5B-36K" --enable-prefix-caching --use-v2-block-manager --enable-chunked-prefill --speculative-model "/home/rm01/Downloads/deepseek-ai/DeepSeek-R1-Distill-Qwen-1.5B-GTPQ-Int4" --num-speculative-token 5 --speculative-draft-tensor-parallel-size 1 --max_num_batched_tokens 256 `

---

### "DeepSeek-R1-Distill-Qwen-32B-FP8" + "DeepSeek-R1-Distill-Qwen-1.5B" | "memory-utilization=0.85" | "max-model-len=28000"

`vllm serve "/home/rm01/Downloads/deepseek-ai/DeepSeek-R1-Distill-Qwen-32B-FP8" --gpu-memory-utilization=0.85 --max-model-len=28000 --served-model-name "DeepSeek-R1-Distill-Qwen-32B-FP8-Speculative-28K" --enable-prefix-caching --use-v2-block-manager --enable-chunked-prefill --speculative-model "/home/rm01/Downloads/deepseek-ai/DeepSeek-R1-Distill-Qwen-1.5B" --num-speculative-token 3 --speculative-draft-tensor-parallel-size 1 --max_num_batched_tokens 256`

---

### "DeepSeek-R1-Distill-Qwen-32B-FP8" + "DeepSeek-R1-Distill-Qwen-1.5B-FP8" | "memory-utilization=0.76" | "max-model-len=32000"

`vllm serve "/home/rm01/Downloads/deepseek-ai/DeepSeek-R1-Distill-Qwen-32B-FP8" --gpu-memory-utilization=0.76 --max-model-len=32000 --served-model-name "DeepSeek-R1-Distill-Qwen-32B-FP8-Speculative-32K" --enable-prefix-caching --use-v2-block-manager --enable-chunked-prefill --speculative-model "/home/rm01/Downloads/deepseek-ai/DeepSeek-R1-Distill-Qwen-1.5B-FP8" --num-speculative-token 3 --speculative-draft-tensor-parallel-size 1 --max_num_batched_tokens 256`

---

## Speculative in Ngram

### "Qwen2.5-72B-Instruct-AWQ" with Ngram | "memory-utilization=0.9" | "max-model-len=10000"

`vllm serve "/home/rm01/Downloads/Qwen/Qwen2.5-72B-Instruct-AWQ" --gpu-memory-utilization=0.9 --max-model-len=10000 --served-model-name "Qwen2.5-72B-Instruct-AWQ-Speculative-Ngram-10K" --speculative-model [ngram] --num-speculative-token 5 --enable-prefix-caching --use-v2-block-manager --enable-chunked-prefill --speculative-draft-tensor-parallel-size 1 --speculative-disable-mqa-scorer --ngram-prompt-lookup-max=4 --ngram-prompt-lookup-min=3 --max_num_batched_tokens 256 --max-parallel-loading-workers=4`

---

### "QwQ-32B-FP8-dynamic" with Ngram | "memory-utilization=0.78" | "max-model-len=32000"

`vllm serve "/home/rm01/Downloads/Qwen/QwQ-32B-FP8-dynamic" --gpu-memory-utilization=0.78 --max-model-len=32000 --served-model-name "QwQ-32B-FP8-dynamic" --enable-prefix-caching --use-v2-block-manager --enable-chunked-prefill --speculative-model [ngram] --num-speculative-token 5 --speculative-draft-tensor-parallel-size 1 --speculative-disable-mqa-scorer --ngram-prompt-lookup-max=5 --ngram-prompt-lookup-min=2 --max_num_batched_tokens 256`

---

### "QwQ-32B-AWQ" with Ngram | "memory-utilization=0.5" | "max-model-len=32768"

`vllm serve "/home/rm01/Downloads/Qwen/QwQ-32B-AWQ" --gpu-memory-utilization=0.5 --max-model-len=32768 --served-model-name "QwQ-32B-AWQ" --enable-prefix-caching --use-v2-block-manager --enable-chunked-prefill --speculative-model [ngram] --num-speculative-token 5 --speculative-draft-tensor-parallel-size 1 --speculative-disable-mqa-scorer --ngram-prompt-lookup-max=3 --ngram-prompt-lookup-min=2 --max_num_batched_tokens 256`

---

### "QwQ-32B-FP8-dynamic" with Ngram | "memory-utilization=0.78" | "max-model-len=32768"

`vllm serve "/home/rm01/Downloads/Qwen/QwQ-32B-FP8-dynamic" --gpu-memory-utilization=0.74 --max-model-len=32768 --served-model-name "QwQ-32B-FP8-dynamic" --enable-prefix-caching --use-v2-block-manager --enable-chunked-prefill --speculative-model [ngram] --num-speculative-token 5 --speculative-draft-tensor-parallel-size 1 --speculative-disable-mqa-scorer --ngram-prompt-lookup-max=5 --ngram-prompt-lookup-min=2 --max_num_batched_tokens 256`

---

### "QwQ-32B-FP8" with Ngram | "memory-utilization=0.78" | "max-model-len=32768"

`vllm serve "/home/rm01/Downloads/Qwen/QwQ-32B-FP8" --gpu-memory-utilization=0.74 --max-model-len=32768 --served-model-name "QwQ-32B-FP8" --enable-prefix-caching --use-v2-block-manager --enable-chunked-prefill --speculative-model [ngram] --num-speculative-token 5 --speculative-draft-tensor-parallel-size 1 --speculative-disable-mqa-scorer --ngram-prompt-lookup-max=5 --ngram-prompt-lookup-min=2 --max_num_batched_tokens 256`

---

## Normal inference with vLLM

### "Qwen2.5-72B-Instruct-AWQ" | "memory-utilization=0.93" | "max-model-len=16000"

`vllm serve "/home/rm01/Downloads/Qwen/Qwen2.5-72B-Instruct-AWQ" --gpu-memory-utilization=0.93 --max-model-len=16000 --served-model-name "Qwen2.5-72B-Instruct-AWQ-16K" --enable-prefix-caching --use-v2-block-manager --enable-chunked-prefill`

---
### "Qwen2.5-32B-Instruct-AWQ" | "memory-utilization=0.93" | "max-model-len=32000"

`vllm serve "/home/rm01/Downloads/Qwen/Qwen2.5-32B-Instruct-AWQ" --gpu-memory-utilization=0.93 --max-model-len=32000 --served-model-name "Qwen2.5-72B-Instruct-AWQ-16K" --enable-prefix-caching --use-v2-block-manager --enable-chunked-prefill`

---

### "Qwen2.5-32B-Instruct-GPTQ-Int8" | "memory-utilization=0.90" | "max-model-len=16000"

`vllm serve "/home/rm01/Downloads/Qwen/Qwen2.5-32B-Instruct-GPTQ-Int8" --gpu-memory-utilization=0.90 --max-model-len=16000 --served-model-name "Qwen2.5-32B-Instruct-GPTQ-Int8-16K" --enable-prefix-caching --use-v2-block-manager --enable-chunked-prefill`

---

### "Qwen2.5-14B-Instruct-1M" | "memory-utilization=0.95" | "max-model-len=123000"

`vllm serve "/home/rm01/Downloads/Qwen/Qwen2.5-14B-Instruct-1M" --gpu-memory-utilization=0.95 --max-model-len=1230000 --served-model-name "Qwen2.5-14B-Instruct-123K" --enable-prefix-caching --use-v2-block-manager --enable-chunked-prefill`

---

### "DeepSeek-R1-Distill-Qwen-32B-GPTQ-Int8" | "memory-utilization=0.93" | "max-model-len=16000"

`vllm serve "/home/rm01/Downloads/deepseek-ai/DeepSeek-R1-Distill-Qwen-32B-GPTQ-Int8" --gpu-memory-utilization=0.93 --max-model-len=16000 --served-model-name "DeepSeek-R1-Distill-Qwen-32B-GPTQ-Int8" --enable-prefix-caching --use-v2-block-manager --enable-chunked-prefill`

---

### "Deepseek-R1-Distill-Qwen-32B-GPTQ-Int4" | "memory-utilization=0.90" | "max-model-len=32000"

`vllm serve "/home/rm01/Downloads/deepseek-ai/DeepSeek-R1-Distill-Qwen-32B-GPTQ-Int4" --gpu-memory-utilization=0.90 --max-model-len=32000 --served-model-name "DeepSeek-R1-Distill-Qwen-32B-GPTQ-Int4-32K" --enable-prefix-caching --use-v2-block-manager --enable-chunked-prefill`

---

### "DeepSeek-R1-Distill-Qwen-32B-FP8" | "memory-utilization=0.90" | "max-model-len=12000"

`vllm serve "/home/rm01/Downloads/deepseek-ai/DeepSeek-R1-Distill-Qwen-32B-FP8" --gpu-memory-utilization=0.90 --max-model-len=12000 --served-model-name "DeepSeek-R1-Distill-Qwen-32B-FP8" --enable-prefix-caching --use-v2-block-manager --enable-chunked-prefill`

---

### "DeepSeek-R1-Distill-Qwen-14B" | "memory-utilization=0.95" | "max-model-len=95000"

`vllm serve "/home/rm01/Downloads/deepseek-ai/DeepSeek-R1-Distill-Qwen-14B" --gpu-memory-utilization=0.95 --max-model-len=95000 --served-model-name "DeepSeek-R1-Distill-Qwen-14B-95K" --enable-prefix-caching --use-v2-block-manager --enable-chunked-prefill`

---

### "Qwen2.5-14B-Instruct-1M-GPTQ-int8" | "memory-utilization=0.95" | "max-model-len=100000"

`vllm serve "/home/rm01/Downloads/Qwen/qwen2.5-14b-instruct-1m-gptq-int8" --gpu-memory-utilization=0.95 --max-model-len=100000 --served-model-name "Qwen2.5-14B-Instruct-GPTQ-int8-1M" --enable-prefix-caching --use-v2-block-manager --enable-chunked-prefill`

---

### "Qwen2.5-14B-Instruct" | "memory-utilization=0.95" | "max-model-len=32000"

`vllm serve "/home/rm01/Downloads/Qwen/Qwen2.5-14B-Instruct" --gpu-memory-utilization=0.95 --max-model-len=32000 --served-model-name "Qwen2.5-14B-Instruct-32K" --enable-prefix-caching --use-v2-block-manager --enable-chunked-prefill`

---

### "Qwen2.5-14B-Instruct-AWQ" | "memory-utilization=0.95" | "max-model-len=32000"

`vllm serve "/home/rm01/Downloads/Qwen/Qwen2.5-14B-Instruct-AWQ" --gpu-memory-utilization=0.95 --max-model-len=32000 --served-model-name "Qwen2.5-14B-Instruct-AWQ-32K" --enable-prefix-caching --use-v2-block-manager --enable-chunked-prefill`

---

### "Qwen2.5-7B-Instruct" | "memory-utilization=0.90" | "max-model-len=32000"

`vllm serve "/home/rm01/Downloads/Qwen/Qwen2.5-7B-Instruct" --gpu-memory-utilization=0.90 --max-model-len=32000 --served-model-name "Qwen2.5-7B-Instruct-32K" --enable-prefix-caching --use-v2-block-manager --enable-chunked-prefill`

---

### "Qwen2.5-7B-Instruct-AWQ" | "memory-utilization=0.80" | "max-model-len=32000"

`vllm serve "/home/rm01/Downloads/Qwen/Qwen2.5-7B-Instruct-AWQ" --gpu-memory-utilization=0.8 --max-model-len=32000 --served-model-name "Qwen2.5-7B-Instruct-AWQ-32K" --enable-prefix-caching --use-v2-block-manager --enable-chunked-prefill`

---

### "Qwen2.5-3B-Instruct" | "memory-utilization=0.90" | "max-model-len=32000"

`vllm serve "/home/rm01/Downloads/Qwen/Qwen/Qwen2.5-3B-Instruct" --gpu-memory-utilization=0.85 --max-model-len=32000 --served-model-name "Qwen2.5-3B-Instruct-32K" --enable-prefix-caching --use-v2-block-manager --enable-chunked-prefill`

---

### "Qwen2.5-3B-Instruct-AWQ" | "memory-utilization=0.85" | "max-model-len=32000"

`vllm serve "/home/rm01/Downloads/Qwen/Qwen2.5-3B-Instruct-AWQ" --gpu-memory-utilization=0.85 --max-model-len=32000 --served-model-name "Qwen2.5-3B-Instruct-AWQ-32K" --enable-prefix-caching --use-v2-block-manager --enable-chunked-prefill`

---


### "Qwen2.5-1.5B-Instruct" | "memory-utilization=0.85" | "max-model-len=32000"

`vllm serve "/home/rm01/Downloads/Qwen/Qwen2.5-1.5B-Instruct" --gpu-memory-utilization=0.85 --max-model-len=32000 --served-model-name "Qwen2.5-1.5B-Instruct-32K" --enable-prefix-caching --use-v2-block-manager --enable-chunked-prefill`

---

### "Qwen2.5-1.5B-Instruct-AWQ" | "memory-utilization=0.85" | "max-model-len=32000"

`vllm serve "/home/rm01/Downloads/Qwen/Qwen2.5-1.5B-Instruct-AWQ" --gpu-memory-utilization=0.85 --max-model-len=32000 --served-model-name "Qwen2.5-1.5B-Instruct-AWQ-32K" --enable-prefix-caching --use-v2-block-manager --enable-chunked-prefill`

---

### "DeepSeek-R1-Distill-Qwen-1.5B" | "memory-utilization=0.85" | "max-model-len=32000"

`vllm serve "/home/rm01/Downloads/deepseek-ai/DeepSeek-R1-Distill-Qwen-1.5B" --gpu-memory-utilization=0.85 --max-model-len=32000 --served-model-name "DeepSeek-R1-Distill-Qwen-1.5B" --enable-prefix-caching --use-v2-block-manager --enable-chunked-prefill`

---

### "Qwen2.5-0.5B-Instruct" | "memory-utilization=0.80" | "max-model-len=32000"

`vllm serve "/home/rm01/Downloads/Qwen/Qwen/Qwen2.5-0.5B-Instruct" --gpu-memory-utilization=0.80 --max-model-len=32000 --served-model-name "Qwen2.5-0.5B-Instruct-32K" --enable-prefix-caching --use-v2-block-manager --enable-chunked-prefill`

---

### "Qwen2.5-0.5B-Instruct-AWQ" | "memory-utilization=0.80" | "max-model-len=32000"

`vllm serve "/home/rm01/Downloads/Qwen/Qwen2.5-0.5B-Instruct-AWQ" --gpu-memory-utilization=0.80 --max-model-len=32000 --served-model-name "Qwen2.5-0.5B-Instruct-AWQ-32K" --enable-prefix-caching --use-v2-block-manager --enable-chunked-prefill`

---

# 【GaoYang】Model Pull Up on Jetson Gaoyang

---

Upload SSD  Enter folder  Start conda-vllm

```
sudo mount /dev/nvme0n1p1 ~/ssd

cd ssd/Qwen

conda activate vllm
```
---

# Clear memory

```
sudo sysctl -w vm.drop_caches=3
```

---

