import requests
import csv
import os
import sys
from datetime import datetime

# 設定資料源與檔名
URL = "https://www.taipower.com.tw/d006/loadGraph/loadGraph/data/genary.json"
FILE_NAME = "power_history.csv"

def scrape():
    # 偽裝成瀏覽器，避免被擋
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
        'Referer': 'https://www.taipower.com.tw/d006/loadGraph/loadGraph/genshx_.html'
    }
    
    try:
        print("🚀 開始抓取台電資料...")
        response = requests.get(URL, headers=headers, timeout=30)
        response.raise_for_status()
        data = response.json()
        
        # 取得發電資料列表
        gens = data.get("genary", [])
        if not gens:
            print("❌ 錯誤：抓到的資料中沒有發電機組清單！")
            sys.exit(1) # 強制結束並報錯

        # 取得更新時間
        update_time = data.get("curr_load_step", datetime.now().strftime("%Y-%m-%d %H:%M"))
        
        file_exists = os.path.isfile(FILE_NAME)
        
        # 寫入檔案
        with open(FILE_NAME, "a", newline="", encoding="utf-8-sig") as f:
            writer = csv.writer(f)
            # 如果是新檔案，寫入標題
            if not file_exists:
                writer.writerow(["紀錄時間", "類別", "機組", "發電量(MW)", "狀態"])
            
            for item in gens:
                if len(item) >= 3:
                    # 台電格式：[類別, 名稱, 發電量, 狀態...]
                    writer.writerow([update_time, item[0], item[1], item[2], item[3] if len(item)>3 else ""])
        
        print(f"✅ 成功！已將 {len(gens)} 筆資料寫入 {FILE_NAME}")

    except Exception as e:
        print(f"❌ 發生致命錯誤: {str(e)}")
        sys.exit(1)

if __name__ == "__main__":
    scrape()
