# ppg接口使用方法
- 发送格式

```json
{
    "datas":[...],
    "freq": int,
    "age": int,
    "gender": "F"/"M"

} 
```

- API格式
121.41.3.58:8090/mental-connect/algorithm/api/ppg/<指标名称>
- 接口共有三个
1. 获取心理学指标
121.41.3.58:8090/mental-connect/algorithm/api/ppg/pyscho-index  
返回数据：  

```json
        {
        "code": 0,
        "message": "",
        "data": {
                "depression": false,
                "anxiety": false
                }
        } 
```
    
2. 获取HRV指标
121.41.3.58:8090/mental-connect/algorithm/api/ppg/hrv-index  
返回数据：
- hrv_index中储存各项心理学指标
- hrv_quality中储存指标质量，0最差，1最好(用于前端显示)

```json
{
"code": 0,
"message": "",
"data": {
        "hrv_index": {
        "HRV_SDNN": 147.027,
        "HRV_RMSSD": 185.9774,
        "HRV_pNN50": 41.4057,
        "HRV_HF": 0.0592,
        "HRV_LF": 0.045,
        "HRV_LFHF": 0.7493
        },
        "hrv_quality": {
        "q_SDNN": 0.9005,
        "q_RMSSD": 0.9062,
        "q_pNN50": 0.8859,
        "q_LHF": 0.1191
        }
    }
}
 ```

3. 获取处理后波形数据  
121.41.3.58:8090/mental-connect/algorithm/api/ppg/wave  
返回数据：
- 数据等长
```json
    {
        "code": 0,
        "message": "",
        "data": {
            "raw_wave":[...],
            "processed_wave": [...]
        }
    }
```
    