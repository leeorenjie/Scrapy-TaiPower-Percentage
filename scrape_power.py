import requests
import csv
import os
from datetime import datetime

# 台電資料源
URL = "https://www.taipower.com.tw/d006/loadGraph/loadGraph/data/genary.json"
FILE_NAME = "power_history.csv"

def scrape():
    try:
        response = requests.get(URL)
        data = response.json()
        
        # 取得更新時間與機組資料
        update_time = data.get("curr_load_step", datetime.now().strftime("%Y-%m-%d %H:%M"))
        gens = data.get("genary", [])
        
        # 檢查 CSV 是否已存在，決定是否寫入標題
        file_exists = os.path.isfile(FILE_NAME)
        
        with open(FILE_NAME, "a", newline="", encoding="utf-8-sig") as f:
            writer = csv.writer(f)
            if not file_exists:
                writer.writerow(["紀錄時間", "機組名稱", "發電量(MW)", "備註"])
            
            for item in gens:
                # 假設 JSON 結構中：item[0]是類別, item[1]是名稱, item[2]是發電量
                # 我們把時間也存進去
                writer.writerow([update_time, item[1], item[2], item[4] if len(item)>4 else ""])
                
        print(f"成功更新資料：{update_time}")
    except Exception as e:
        print(f"發生錯誤: {e}")

if __name__ == "__main__":
    scrape()
