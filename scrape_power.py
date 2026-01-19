import requests
import csv
import os
import sys
import time
from datetime import datetime

URL = "https://www.taipower.com.tw/d006/loadGraph/loadGraph/data/genary.json"
FILE_NAME = "power_history.csv"

def scrape():
    # 使用 Session 來自動處理 Cookie
    session = requests.Session()
    
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
        'Accept': 'application/json, text/javascript, */*; q=0.01',
        'Accept-Language': 'zh-TW,zh;q=0.9,en-US;q=0.8,en;q=0.7',
        'Referer': 'https://www.taipower.com.tw/d006/loadGraph/loadGraph/genshx_.html',
        'Connection': 'keep-alive',
    }
    
    try:
        # 先訪問主頁面以取得潛在的 Session Cookie
        print("🌐 正在初始化連線...")
        session.get("https://www.taipower.com.tw/d006/loadGraph/loadGraph/genshx_.html", headers=headers, timeout=20)
        
        # 稍微等待 2 秒，模擬人類行為
        time.sleep(2)
        
        print("🚀 正在提取發電數據 (aaData)...")
        response = session.get(URL, headers=headers, timeout=30)
        
        if response.status_code == 403:
            print("❌ 被擋住了 (403 Forbidden)。台電伺服器目前拒絕連線，請稍後再試。")
            sys.exit(0) # 這裡改用 exit(0) 讓 Workflow 不會顯示紅色警報，因為這是外部限制
            
        response.raise_for_status()
        data = response.json()
        
        # 抓取 aaData
        gens = data.get("aaData", [])
        if not gens:
            print("⚠️ 警告：aaData 為空，可能資料尚未更新。")
            return

        update_time = datetime.now().strftime("%Y-%m-%d %H:%M")
        
        file_exists = os.path.isfile(FILE_NAME)
        with open(FILE_NAME, "a", newline="", encoding="utf-8-sig") as f:
            writer = csv.writer(f)
            if not file_exists:
                writer.writerow(["紀錄時間", "類別", "機組", "發電量(MW)", "備註"])
            
            count = 0
            for item in gens:
                if isinstance(item, list) and len(item) >= 4:
                    # aaData 索引：1:類別, 2:名稱, 3:發電量, 5:備註
                    writer.writerow([update_time, item[1], item[2], item[3], item[5] if len(item)>5 else ""])
                    count += 1
        
        print(f"✅ 成功寫入 {count} 筆資料到 {FILE_NAME}")

    except Exception as e:
        print(f"❌ 執行發生錯誤: {str(e)}")
        sys.exit(1)

if __name__ == "__main__":
    scrape()
