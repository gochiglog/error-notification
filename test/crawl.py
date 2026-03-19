from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
import tkinter
from tkinter import messagebox
import os
import time

root = tkinter.Tk()
root.withdraw()

# メルカリの検索結果のHTMLを保存するディレクトリ
html_directory = r'C:\Users\perry\Documents\Dev\03_error_notification\test\html'

# ドライバーのセットアップ (PhantomJSやChromeDriverが正しくインストールされている前提)
driver_path = r'C:\Users\perry\Documents\Dev\03_error_notification\lib\chromedriver-win64\chromedriver-win64\chromedriver.exe'
service = Service(driver_path)
driver = webdriver.Chrome(service=service)

#対象ホームページを開く
driver.get('https://gochi-blog.com/')
print("対象のページを開きました")
# messagebox.showinfo("対象のページを開きました")
time.sleep(1)  # ページが完全に読み込まれるまで待機

try:
    wait = WebDriverWait(driver, 10)  # 最大10秒待機
    all_sites_button = wait.until(EC.element_to_be_clickable((By.CLASS_NAME, 'c-bannerLink')))
    all_sites_button.click()
    print("「留学」ページに移動しました")
    # messagebox.showinfo("「留学」ページに移動しました")
    time.sleep(1)
except TimeoutException:
    print(f"「留学」ページに移動できませんでした")
    # messagebox.showinfo("「留学」ページに移動できませんでした")

# 初期ページ番号を1に設定
page_number = 1  



# # 各ページのHTMLを保存
# while True:
#     # 保存するページのディレクトリを作成
#     item_dir_inpage = os.path.join(html_directory, study_abroad)
#     if not os.path.exists(item_dir_inpage):
#         os.makedirs(item_dir_inpage)
#     # 現在のページのHTMLを保存
#     search_html_path = os.path.join(item_dir_inpage, f'mercari_search_{i+1}_page_{page_number}.html')
#     with open(search_html_path, 'w', encoding='utf-8') as file:
#         file.write(driver.page_source)


#     for item_counter, item in enumerate(items):
#         # キーワード除外: タイトルに除外キーワードが含まれていないか確認
#         title_element = item.find('span', class_='hdTxt')
#         item_title = title_element.text.strip() if title_element else ''
#         if any(exclude_word in item_title for exclude_word in exclude_keywords):
#             continue  # 除外キーワードが含まれていたら次のアイテムへ

#         # プラットフォーム確認: サイト名が「メルカリ」であるか確認
#         platform_element = item.find('div', class_='searchShowcaseSiteName')
#         platform_name = platform_element.text.strip() if platform_element else ''
#         if "メルカリ" not in platform_name:
#             continue  # メルカリでない場合、次のアイテムへ

#         # 各商品のURLを取得してHTMLを保存
#         item_link_element = item.find('a', href=True)
#         if item_link_element:
#             item_url = item_link_element['href']
#             # 商品のディレクトリを作成
#             item_dir_initems = os.path.join(item_html_directory, f'mercari_name_{i+1}')
#             if not os.path.exists(item_dir_initems):
#                 os.makedirs(item_dir_initems)
#             print(f"商品 {i+1} の {page_number} ページ目の商品にアクセス中")
#             driver.get(item_url)
#             time.sleep(1)  # 商品ページが完全に読み込まれるまで待機
            
#             # 各商品のHTMLを取得
#             item_html_content = driver.page_source

#             # 商品ページのHTMLを保存
#             item_file_path = os.path.join(item_dir_initems, f'mercari_item_{i+1}_item_{valid_item_counter}.html')
#             with open(item_file_path, 'w', encoding='utf-8') as file:
#                 file.write(item_html_content)
                
#             print(f"商品 {i+1} の {valid_item_counter} 番目の商品HTMLを保存しました")
            
#             valid_item_counter += 1  # 保存対象の商品だけカウント

#     # 次の検索結果ページに進む
#     try:
#         next_page_element = soup.find('li', class_='next')
#         if next_page_element:
#             next_page_link = next_page_element.find('a')['href']
#             driver.get(next_page_link)
#             time.sleep(2)
#             page_number += 1  # ページ番号を進める
#         else:
#             break  # 次のページがない場合はループを抜ける
#     except Exception as e:
#         print(f"Error navigating to next page: {e}")
#         break  # 次のページがない場合はループを抜ける

# ブラウザを終了
driver.quit()
