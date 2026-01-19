import requests
import csv
import os
from datetime import datetime

# 設定資料源
URL = "https://www.taipower.com.tw/d006/loadGraph/loadGraph/data/genary.json"
FILE_NAME = "power_history.csv"

def scrape():
    # 加入 Header 偽裝成瀏覽器，避免被 403 阻擋
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
        'Referer': 'https://www.taipower.com.tw/d006/loadGraph/loadGraph/genshx_.html'
    }
    
    try:
        print(f"正在嘗試抓取資料...")
        response = requests.get(URL, headers=headers, timeout=30)
        response.raise_for_status() 
        data = response.json()
        
        # 取得更新時間
        update_time = data.get("curr_load_step", datetime.now().strftime("%Y-%m-%d %H:%M"))
        gens = data.get("genary", [])
        
        if not gens:
            print("警告：抓取到的機組資料為空！")
            return

        file_exists = os.path.isfile(FILE_NAME)
        
        with open(FILE_NAME, "a", newline="", encoding="utf-8-sig") as f:
            writer = csv.writer(f)
            if not file_exists:
                writer.writerow(["紀錄時間", "類別", "機組名稱", "發電量(MW)", "狀態"])
            
            for item in gens:
                if len(item) >= 3:
                    # 台電資料結構調整：item[0]類別, item[1]名稱, item[2]數值
                    writer.writerow([update_time, item[0], item[1], item[2], item[3] if len(item)>3 else ""])
                
        print(f"✅ 成功更新：{update_time}，共 {len(gens)} 筆。")
        
    except Exception as e:
        print(f"❌ 發生錯誤: {str(e)}")
        raise e

if __name__ == "__main__":
    scrape()
