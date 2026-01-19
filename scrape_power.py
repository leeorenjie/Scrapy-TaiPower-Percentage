import requests
import csv
import os
import sys
from datetime import datetime

URL = "https://www.taipower.com.tw/d006/loadGraph/loadGraph/data/genary.json"
FILE_NAME = "power_history.csv"

def scrape():
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
        'Accept': 'application/json, text/javascript, */*; q=0.01',
        'X-Requested-With': 'XMLHttpRequest',
        'Referer': 'https://www.taipower.com.tw/d006/loadGraph/loadGraph/genshx_.html'
    }
    
    try:
        print("🚀 正在連線至台電伺服器...")
        response = requests.get(URL, headers=headers, timeout=30)
        response.raise_for_status()
        
        # 嘗試解析 JSON
        try:
            data = response.json()
        except Exception:
            print(f"❌ 無法解析 JSON，原始內容前100字：{response.text[:100]}")
            sys.exit(1)

        # 自動尋找資料列表 (有些版本在 'genary'，有些在根目錄)
        gens = data.get("genary") if isinstance(data, dict) else data
        
        if not gens or not isinstance(gens, list):
            print(f"❌ 找不到機組清單。資料結構關鍵字：{list(data.keys()) if isinstance(data, dict) else '非字典格式'}")
            sys.exit(1)

        # 取得時間
        update_time = data.get("curr_load_step") if isinstance(data, dict) else datetime.now().strftime("%Y-%m-%d %H:%M")
        
        file_exists = os.path.isfile(FILE_NAME)
        with open(FILE_NAME, "a", newline="", encoding="utf-8-sig") as f:
            writer = csv.writer(f)
            if not file_exists:
                writer.writerow(["紀錄時間", "類別", "機組", "發電量(MW)", "備註"])
            
            count = 0
            for item in gens:
                if isinstance(item, list) and len(item) >= 3:
                    # 台電格式：[類別, 名稱, 數值, 狀態, 備註...]
                    writer.writerow([update_time, item[0], item[1], item[2], item[4] if len(item)>4 else ""])
                    count += 1
        
        print(f"✅ 成功寫入 {count} 筆資料到 {FILE_NAME}")

    except Exception as e:
        print(f"❌ 發生錯誤: {str(e)}")
        sys.exit(1)

if __name__ == "__main__":
    scrape()
