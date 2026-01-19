import requests
import csv
import os
import sys
from datetime import datetime

# 更換為台電官方行動版 API，通常較不擋 GitHub IP
URL = "https://www.taipower.com.tw/d006/loadGraph/loadGraph/data/genary.json"
FILE_NAME = "power_history.csv"

def scrape():
    headers = {
        'User-Agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 14_6 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.0.3 Mobile/15E148 Safari/604.1',
        'Accept': 'application/json'
    }
    
    try:
        print("🌐 嘗試存取行動版 API...")
        response = requests.get(URL, headers=headers, timeout=30)
        
        if response.status_code == 403:
            print("❌ 依舊觸發 403。台電伺服器暫時封鎖了 GitHub 區段，請勿手動狂點，讓它整點自動執行即可。")
            return

        response.raise_for_status()
        data = response.json()
        
        # 提取資料（優先找 aaData）
        gens = data.get("aaData", [])
        if not gens:
            print("⚠️ 抓取成功但資料夾內無數據。")
            return

        update_time = datetime.now().strftime("%Y-%m-%d %H:%M")
        file_exists = os.path.isfile(FILE_NAME)
        
        with open(FILE_NAME, "a", newline="", encoding="utf-8-sig") as f:
            writer = csv.writer(f)
            if not file_exists or os.path.getsize(FILE_NAME) < 10:
                writer.writerow(["紀錄時間", "類別", "機組", "發電量(MW)", "備註"])
            
            count = 0
            for item in gens:
                if len(item) >= 4:
                    # 索引對應：1:類別, 2:名稱, 3:數值
                    writer.writerow([update_time, item[1], item[2], item[3], item[5] if len(item)>5 else ""])
                    count += 1
        
        print(f"✅ 數據更新成功！本次寫入 {count} 筆。")

    except Exception as e:
        print(f"❌ 連線異常: {str(e)}")

if __name__ == "__main__":
    scrape()
