# Pull up models with vLLM_085p1 Date:250620

`conda activate vllm085p1`
`export TORCH_CUDA_ARCH_LIST="8.7"`

## Qwen3-30B-A3B-AWQ

1. Normal mode:

`vllm serve "/home/rm01/cfe/models/llm/Qwen3-30B-A3B-AWQ" --port=58000 --gpu-memory-utilization=0.4 --max-model-len=32768 --served-model-name "RM-01 LLM" --enable-prefix-caching --enable-chunked-prefill --max_num_batched_tokens=512 --block-size=16`

2. N-gram (Speculative) *Not recommended for use at present, it is only for testing*:

`vllm serve "/home/rm01/cfe/models/llm/Qwen3-30B-A3B-AWQ" --port=58000 --gpu-memory-utilization=0.4 --max-model-len=32768 --served-model-name "RM-01 LLM" --enable-prefix-caching --enable-chunked-prefill --max_num_batched_tokens=512 --block-size=16 --speculative_config '{"method": "ngram", "num_speculative_tokens": 12, "prompt_lookup_max": 4, "prompt_lookup_min": 2}'`

---

## Qwen3-32B-AWQ 

1. Normal mode:

`vllm serve "/home/rm01/cfe/models/llm/Qwen3-32B-AWQ" --port=58000 --gpu-memory-utilization=0.52 --max-model-len=32768 --served-model-name "RM-01 LLM" --enable-prefix-caching --enable-chunked-prefill --max_num_batched_tokens=512 --block-size=16`

2. N-gram (Speculative):

`vllm serve "/home/rm01/cfe/models/llm/Qwen3-32B-AWQ" --port=58000 --gpu-memory-utilization=0.52 --max-model-len=32768 --served-model-name "RM-01 LLM" --enable-prefix-caching --enable-chunked-prefill --max_num_batched_tokens=512 --block-size=16 --speculative_config '{"method": "ngram", "num_speculative_tokens": 12, "prompt_lookup_max": 4, "prompt_lookup_min": 2}'`


3. Draft mode (Speculative)*The current parameters cannot deliver optimal performance*:

`vllm serve "/home/rm01/cfe/models/llm/Qwen3-32B-AWQ" --port=58000 --gpu-memory-utilization=0.55 --max-model-len=32768 --served-model-name "RM-01 LLM" --enable-prefix-caching --enable-chunked-prefill --max_num_batched_tokens=512 --block-size=16 --speculative_config '{"model": "/home/rm01/cfe/models/llm/Qwen/Qwen3-0.6B", "num_speculative_tokens": 12}'`

---

## MiniCPM4-8B

1. Normal mode:

`vllm serve "/home/rm01/cfe/models/llm/MiniCPM4-8B" --port=58000 --gpu-memory-utilization=0.5 --max-model-len=32768 --served-model-name "RM-01 LLM" --enable-prefix-caching --enable-chunked-prefill --max_num_batched_tokens=512 --block-size=16 --trust-remote-code`

2. Eagle (Speculative) *Not recommended for use at present, it is only for testing*:

`vllm serve "/home/rm01/cfe/models/llm/MiniCPM4-8B" --port=58000 --gpu-memory-utilization=0.5 --max-model-len=32768 --served-model-name "RM-01 LLM" --enable-prefix-caching --enable-chunked-prefill --max_num_batched_tokens=512 --block-size=16 --trust-remote-code --speculative_config '{"model": "/home/rm01/cfe/models/llm/MiniCPM4-8B-Eagle-vLLM"}'`

3. N-gram (Speculative) *Not recommended for use at present, it is only for testing*:

`vllm serve "/home/rm01/cfe/models/llm/MiniCPM4-8B" --port=58000 --gpu-memory-utilization=0.5 --max-model-len=32768 --served-model-name "RM-01 LLM" --enable-prefix-caching --enable-chunked-prefill --max_num_batched_tokens=512 --block-size=16 --trust-remote-code --speculative_config '{"method": "ngram", "num_speculative_tokens": 12, "prompt_lookup_max": 4, "prompt_lookup_min": 2}'`

---

## Evalscope test:

```
evalscope perf \
  --parallel 128 \
  --number 128 \
  --model 'RM-01 LLM' \
  --url http://10.10.99.98:58000/v1/chat/completions \
  --api openai \
  --dataset random \
  --max-tokens 128 \
  --min-tokens 128 \
  --prefix-length 0 \
  --min-prompt-length 64 \
  --max-prompt-length 512 \
  --tokenizer-path /Users/massif/Desktop/models/Qwen3-32B-AWQ \
  --extra-args '{"ignore_eos": true}' \
  --outputs-dir /Users/massif/Desktop/modeltest 
```
