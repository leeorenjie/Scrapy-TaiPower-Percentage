import requests
import csv
import os
from datetime import datetime

# 設定資料源
URL = "https://www.taipower.com.tw/d006/loadGraph/loadGraph/data/genary.json"
FILE_NAME = "power_history.csv"

def scrape():
    try:
        response = requests.get(URL, timeout=30)
        response.raise_for_status() # 確保網頁請求成功
        data = response.json()
        
        # 取得更新時間
        update_time = data.get("curr_load_step", datetime.now().strftime("%Y-%m-%d %H:%M"))
        gens = data.get("genary", [])
        
        if not gens:
            print("警告：抓取到的機組資料為空！")
            return

        file_exists = os.path.isfile(FILE_NAME)
        
        # 使用 utf-8-sig 確保 Excel 打開不亂碼
        with open(FILE_NAME, "a", newline="", encoding="utf-8-sig") as f:
            writer = csv.writer(f)
            if not file_exists:
                writer.writerow(["紀錄時間", "類別", "機組名稱", "發電量(MW)", "備註"])
            
            for item in gens:
                # 台電 JSON 結構：[類別, 名稱, 發電量, 狀態, 備註...]
                # 我們把有用的欄位抓出來
                if len(item) >= 3:
                    writer.writerow([update_time, item[0], item[1], item[2], item[4] if len(item)>4 else ""])
                
        print(f"✅ 成功寫入 {len(gens)} 筆資料到 {FILE_NAME}，時間：{update_time}")
        
    except Exception as e:
        print(f"❌ 發生錯誤: {str(e)}")
        # 這裡故意讓程式拋出錯誤，讓 GitHub Actions 知道失敗了
        raise e

if __name__ == "__main__":
    scrape()
