from selenium import webdriver
from selenium.webdriver.common.by import By
from time import sleep
import datetime
import sqlalchemy as sa
import pandas as pd

# -------------------------------------------------------
# ส่วนที่ 1 : พิมพ์ Current Datetime ทาง stdout 

curr_datetime = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
print(curr_datetime)

# -------------------------------------------------------
# ส่วนที่ 2 : สร้างตัวแปร driver เพื่อควบคุม Chrome ผ่าน Webdriver
#
# เนื่องด้วยบน Docker Container คำสั่งต่าง ๆ จะถูก run ภายใต้สิทธิของ root
# Chrome บน Linux ไม่อนุญาตให้ run ใต้สิทธิ root โดยไม่ระบุ --no-sandbox
# ซึ่ง --no-sandbox เป็นการปิด important security mechanisms บางอย่างของ Chrome
# ท่านจึงควรมั่นใจว่า website ที่ท่านจะเปิดด้วย driver นี้มีความปลอดภัยน่าเชื่อถือ
# หาก website ที่จะเปิดด้วย driver มีความเสี่ยง ท่านควรสร้าง User อื่น
# เพื่อ run Chrome แทน root โดยไม่ต้องระบุ --no-sandbox

options = webdriver.ChromeOptions()
options.add_argument("--headless=new")
options.add_argument("--no-sandbox")
driver = webdriver.Chrome(options = options)

# -------------------------------------------------------
# ส่วนที่ 3 : ค้นหา block ทีเป็น Pantip Trend 
# 
# ในหน้าเว็บ https://pantip.com/forum/lumpini ประกอบด้วยหลาย block
# ซึ่งมีทั้ง Announce, กระทู้แนะนำโดยสมาชิก, Pantip Pick, กระทู้ล่าสุด และส่วนที่เราต้องการ Pantip Trend
# จึงใช้วิธีค้นหา elements ทั้งหมดที่มี class name เป็น pt-block (Pantip Block) 
# แล้ววน loop หาว่า block ใด ที่เป็น block ของ Pantib Trend
# โดย block ที่เป็นส่วนของ pantip Trend นั้นจะมี pt-block-header ที่เขียนว่า "Pantip Trend" 

driver.get("https://pantip.com/forum/lumpini")
blocks = driver.find_elements(By.CLASS_NAME, "pt-block")
pantip_trend_block = None
for block in blocks:
    header = block.find_element(By.CLASS_NAME, "pt-block-header").text
    if header == "Pantip Trend":
        pantip_trend_block = block
        break

# -------------------------------------------------------
# ส่วนที่ 4 : นำ items ทั้งหมดที่อยู่ภายใต้ "Pantip Trend" block มาสร้างเป็น Pandas Dataframe
#
# โดย items ที่เราต้องกันนั้นจะมี class name เป็น pt-list-item จึงค้นหา elements เหล่านั้นออกมา
# และภายใน pt-list-item นั้นก็จะมี tag ต่าง ๆ ที่เราต้องดังนี้
# a tag = url ของกระทู้
# h2 = title ของกระทู้
# h5 = username ของผู้ตั้งกระทู้
# จึงนำข้อมูลภายใต้ tag เหล่านี้มาสร้างเป็น dict ที่มีสมาชิกเป็น list ของข้อมูล
# แล้วนำ dict นั้น มาสร้างเป็น Pandas DataFrame 

rows = {
    "action_date": [],
    "url": [],
    "title": [],
    "username": []
}
items = pantip_trend_block.find_elements(By.CLASS_NAME, "pt-list-item")
for item in items:
    rows["action_date"].append(curr_datetime)
    rows["url"].append(item.find_element(By.TAG_NAME, "a").get_attribute("href"))
    rows["title"].append(item.find_element(By.TAG_NAME, "h2").text)
    rows["username"].append(item.find_element(By.TAG_NAME, "h5").text)
df = pd.DataFrame(rows)

# -------------------------------------------------------
# ส่วนที่ 5 : นำ DataFrame ที่ได้ insert เข้า Database
#
# โดยการ insert เข้า Database ทำโดยใช้คำสั่ง to_sql 
# และต้องระบุ if_exists เป็น append เพื่อให้เขียนข้อมูลต่อท้ายตารางไปเรื่อย ๆ 

conn_str = "mysql+pymysql://root:password@host.docker.internal:3306/de_inter"
engine = sa.create_engine(conn_str)
conn = engine.connect()
df.to_sql("lumpini_pantip_trend", conn, index=False, if_exists="append")
conn.close()
