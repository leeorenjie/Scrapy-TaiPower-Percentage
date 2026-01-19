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
        'Referer': 'https://www.taipower.com.tw/d006/loadGraph/loadGraph/genshx_.html'
    }
    
    try:
        print("🚀 偵測到資料結構，正在提取 aaData...")
        response = requests.get(URL, headers=headers, timeout=30)
        response.raise_for_status()
        data = response.json()
        
        # 根據 image_a77da6.png 的報錯，資料藏在 aaData 裡
        gens = data.get("aaData", [])
        
        if not gens:
            print("❌ 錯誤：aaData 為空，請檢查伺服器狀態")
            sys.exit(1)

        # 嘗試抓取時間戳記 (如果沒有就用系統時間)
        update_time = datetime.now().strftime("%Y-%m-%d %H:%M")
        
        file_exists = os.path.isfile(FILE_NAME)
        with open(FILE_NAME, "a", newline="", encoding="utf-8-sig") as f:
            writer = csv.writer(f)
            if not file_exists:
                writer.writerow(["紀錄時間", "類別", "機組", "發電量(MW)", "備註"])
            
            count = 0
            for item in gens:
                # 確保 item 是列表且有足夠長度
                if isinstance(item, list) and len(item) >= 3:
                    # 台電 aaData 結構通常為：[狀態圖, 類別, 名稱, 發電量, 淨尖峰, 備註...]
                    # 這裡我們略過第一項狀態圖，從類別開始抓
                    writer.writerow([update_time, item[1], item[2], item[3], item[5] if len(item)>5 else ""])
                    count += 1
        
        print(f"✅ 大功告成！成功寫入 {count} 筆資料到 {FILE_NAME}")

    except Exception as e:
        print(f"❌ 執行失敗: {str(e)}")
        sys.exit(1)

if __name__ == "__main__":
    scrape()
