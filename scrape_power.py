import requests
import csv
import os
import sys
import time
from datetime import datetime

URL = "https://www.taipower.com.tw/d006/loadGraph/loadGraph/data/genary.json"
FILE_NAME = "power_history.csv"

def scrape():
    # 使用 Session 模擬完整瀏覽行為
    session = requests.Session()
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36',
        'Accept': 'application/json, text/javascript, */*; q=0.01',
        'Referer': 'https://www.taipower.com.tw/d006/loadGraph/loadGraph/genshx_.html',
        'X-Requested-With': 'XMLHttpRequest'
    }
    
    try:
        print("🌐 嘗試建立連線...")
        # 先造訪首頁
        session.get("https://www.taipower.com.tw/d006/loadGraph/loadGraph/genshx_.html", headers=headers, timeout=20)
        time.sleep(3) # 停頓一下，比較像真人
        
        print("🚀 請求 JSON 資料...")
        response = session.get(URL, headers=headers, timeout=30)
        
        if response.status_code == 403:
            print("❌ 觸發 403 Forbidden。台電伺服器拒絕連線，我們下次整點再試。")
            # 建立一個空檔案防止 GitHub Action 報錯找不到檔案
            if not os.path.exists(FILE_NAME):
                with open(FILE_NAME, "w", encoding="utf-8-sig") as f:
                    writer = csv.writer(f)
                    writer.writerow(["紀錄時間", "類別", "機組", "發電量(MW)", "備註"])
            return

        response.raise_for_status()
        data = response.json()
        
        # 針對 aaData 結構抓取
        gens = data.get("aaData", [])
        if not gens:
            print("⚠️ 找不到 aaData 內容。")
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
                    # item[1]:類別, item[2]:機組, item[3]:數值
                    writer.writerow([update_time, item[1], item[2], item[3], item[5] if len(item)>5 else ""])
                    count += 1
        
        print(f"✅ 成功！寫入 {count} 筆資料。")

    except Exception as e:
        print(f"❌ 發生錯誤: {str(e)}")
        # 即使報錯也建立一個檔案，確保 Git 動作不會失敗
        if not os.path.exists(FILE_NAME):
            open(FILE_NAME, 'a').close()

if __name__ == "__main__":
    scrape()
