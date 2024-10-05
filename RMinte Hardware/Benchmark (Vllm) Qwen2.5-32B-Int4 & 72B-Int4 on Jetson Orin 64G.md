## 测试报告 - Benchmark (Vllm) Qwen2.5-32B-Int4 & 72B-Int4 on Jetson Orin 64G

### Benchmark Qwen2.5-32B-Int4

Benchmarking summary: 
 Time taken for tests: 46.050 seconds
 Expected number of requests: 1
 Number of concurrency: 1
 Total requests: 1
 Succeed requests: 1
 Failed requests: 0
 Average QPS: 0.022
 Average latency: 45.798
 Throughput(average output tokens per second): 8.057
 Average time to first token: 45.798
 Average input tokens per request: 44.000
 Average output tokens per request: 371.000
 Average time per output token: 0.12412
 Average package per request: 1.000
 Average package latency: 45.798
 Max output tokens per second: 8.3
 
 Benchmarking summary: 
 Time taken for tests: 50.150 seconds
 Expected number of requests: 10
 Number of concurrency: 10
 Total requests: 10
 Succeed requests: 10
 Failed requests: 0
 Average QPS: 0.199
 Average latency: 37.731
 Throughput(average output tokens per second): 47.597
 Average time to first token: 37.731
 Average input tokens per request: 49.900
 Average output tokens per request: 238.700
 Average time per output token: 0.02101
 Average package per request: 1.000
 Average package latency: 37.731
 Percentile of time to first token: 
     p50: 39.6797
     p66: 40.9543
     p75: 45.0028
     p80: 45.2550
     p90: 50.0459
     p95: 50.0459
     p98: 50.0459
     p99: 50.0459
 Percentile of request latency: 
     p50: 39.6797
     p66: 40.9543
     p75: 45.0028
     p80: 45.2550
     p90: 50.0459
     p95: 50.0459
     p98: 50.0459
     p99: 50.0459
 Max output tokens per second: 75.4


Benchmarking summary: 
 Time taken for tests: 119.832 seconds
 Expected number of requests: 100
 Number of concurrency: 100
 Total requests: 100
 Succeed requests: 100
 Failed requests: 0
 Average QPS: 0.835
 Average latency: 81.185
 Throughput(average output tokens per second): 193.571
 Average time to first token: 81.185
 Average input tokens per request: 49.890
 Average output tokens per request: 231.960
 Average time per output token: 0.00517
 Average package per request: 1.000
 Average package latency: 81.185
 Percentile of time to first token: 
     p50: 89.5692
     p66: 94.2450
     p75: 95.7965
     p80: 97.7155
     p90: 103.2936
     p95: 105.6626
     p98: 111.9956
     p99: 119.1592
 Percentile of request latency: 
     p50: 89.5692
     p66: 94.2450
     p75: 95.7965
     p80: 97.7155
     p90: 103.2936
     p95: 105.6626
     p98: 111.9956
     p99: 119.1592
 Max output tokens per second: 303
 
 ---
 
 ##¥ Benchmark Qwen2.5-72B-Int4
 
 Benchmarking summary: 
 Time taken for tests: 133.136 seconds
 Expected number of requests: 1
 Number of concurrency: 1
 Total requests: 1
 Succeed requests: 1
 Failed requests: 0
 Average QPS: 0.008
 Average latency: 132.985
 Throughput(average output tokens per second): 3.831
 Average time to first token: 132.985
 Average input tokens per request: 44.000
 Average output tokens per request: 510.000
 Average time per output token: 0.26105
 Average package per request: 1.000
 Average package latency: 132.985
 Max output tokens per second: 4
 
 Benchmarking summary: 
 Time taken for tests: 136.245 seconds
 Expected number of requests: 10
 Number of concurrency: 10
 Total requests: 10
 Succeed requests: 10
 Failed requests: 0
 Average QPS: 0.073
 Average latency: 89.541
 Throughput(average output tokens per second): 24.067
 Average time to first token: 89.541
 Average input tokens per request: 49.900
 Average output tokens per request: 327.900
 Average time per output token: 0.04155
 Average package per request: 1.000
 Average package latency: 89.541
 Percentile of time to first token: 
     p50: 93.4758
     p66: 99.4343
     p75: 104.0851
     p80: 108.4075
     p90: 135.8489
     p95: 135.8489
     p98: 135.8489
     p99: 135.8489
 Percentile of request latency: 
     p50: 93.4758
     p66: 99.4343
     p75: 104.0851
     p80: 108.4075
     p90: 135.8489
     p95: 135.8489
     p98: 135.8489
     p99: 135.8489
 Max output tokens per second: 38
 
 Benchmarking summary: 
 Time taken for tests: 424.544 seconds
 Expected number of requests: 100
 Number of concurrency: 100
 Total requests: 100
 Succeed requests: 100
 Failed requests: 0
 Average QPS: 0.236
 Average latency: 221.434
 Throughput(average output tokens per second): 70.683
 Average time to first token: 221.434
 Average input tokens per request: 49.890
 Average output tokens per request: 300.080
 Average time per output token: 0.01415
 Average package per request: 1.000
 Average package latency: 221.434
 Percentile of time to first token: 
     p50: 234.2268
     p66: 265.4298
     p75: 282.1408
     p80: 291.9766
     p90: 317.7026
     p95: 334.7111
     p98: 371.4026
     p99: 423.9677
 Percentile of request latency: 
     p50: 234.2268
     p66: 265.4298
     p75: 282.1408
     p80: 291.9766
     p90: 317.7026
     p95: 334.7111
     p98: 371.4026
     p99: 423.9677
 Max output tokens per second: 152.7
