# Install EvalsScope and make a test

## 创建conda环境

## 建议使用 python 3.10
`conda create -n evalscope python=3.10`

## 激活conda环境
`conda activate evalscope`

## pip安装依赖

`pip install evalscope                # 安装 Native backend (默认)`

## 额外选项
```
pip install 'evalscope[opencompass]'   # 安装 OpenCompass backend
pip install 'evalscope[vlmeval]'       # 安装 VLMEvalKit backend
pip install 'evalscope[rag]'           # 安装 RAGEval backend
pip install 'evalscope[perf]'          # 安装 模型压测模块 依赖
pip install 'evalscope[app]'           # 安装 可视化 相关依赖
pip install 'evalscope[all]'           # 安装所有 backends (Native, OpenCompass, VLMEvalKit, RAGEval)
```

## 使用命令行

```
evalscope eval \
 --model Qwen/Qwen2.5-0.5B-Instruct \
 --datasets gsm8k arc \
 --limit 5
```

## 模型API服务评测

```
evalscope eval \
  --model RM01LLM \
  --api-url http://10.10.99.98:8000/v1/chat/completions \
  --api-key 12345 \
  --eval-type service \
  --datasets gsm8k \
  --limit 1024 \
  --timeout 120 \
  --work-dir /Users/massif/Desktop/modeltest 
```
  
## 压力测试

```
evalscope perf \
  --parallel 1 \
  --number 1 \
  --model RM-01 LLM \
  --url http://10.10.99.98:58000/v1/chat/completions \
  --api openai \
  --dataset random \
  --max-tokens 1024 \
  --min-tokens 1024 \
  --prefix-length 0 \
  --min-prompt-length 1024 \
  --max-prompt-length 1024 \
  --tokenizer-path /Users/massif/Desktop/models/Qwen3-32B-AWQ \
  --extra-args '{"ignore_eos": true}' \
  --outputs-dir /Users/massif/Desktop/modeltest 
```