import json
import requests
import concurrent.futures

# 配置
TXT_FILE = "vip_sites.txt"
OUTPUT_FILE = "index.json"
# 使用 FongMi 维护的稳定爬虫包
JAR = "https://mirror.ghproxy.com/https://raw.githubusercontent.com/FongMi/TV/main/release/spider.jar"

def test_api(line):
    line = line.strip()
    if not line or line.startswith("#"): return None
    try:
        name, api = line.split(",")
        # 尝试访问接口，3秒超时。如果接口连通性差，会自动被跳过
        resp = requests.get(api.strip(), timeout=3)
        if resp.status_code == 200:
            return {
                "key": name.strip(),
                "name": f"💎 {name.strip()}",
                "type": 1,
                "api": api.strip(),
                "searchable": 1,
                "quickSearch": 1,
                "filterable": 1
            }
    except:
        pass
    return None

def build():
    print("开始检测精品源连通性...")
    with open(TXT_FILE, "r", encoding="utf-8") as f:
        lines = f.readlines()
    
    with concurrent.futures.ThreadPoolExecutor(max_workers=10) as executor:
        results = list(executor.map(test_api, lines))
        valid_sites = [r for r in results if r is not None]

    data = {
        "spider": JAR,
        "wallpaper": "https://picsum.photos/1920/1080",
        "sites": valid_sites,
        "lives": [],
        "parses": [
            {"name":"解析1","type":3,"url":"https://jx.jsonplayer.com/player/?url="},
            {"name":"解析2","type":3,"url":"https://jx.xmflv.com/?url="}
        ]
    }

    with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    print(f"成功！保留了 {len(valid_sites)} 个优质源。")

if __name__ == "__main__":
    build()
