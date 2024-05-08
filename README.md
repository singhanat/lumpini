# lumpini

Workshop สรุปรวมความรู้ตลอด 3 วัน ของการอบรม Data Engineering ภายใต้โครงการ  GEEKS ระดับ Intermediate ครั้งที่ 1

## คำแนะนำ

soucre code นี้ คล้ายกับ chospital ที่เราทำด้วยกันในห้องอบรมเป็นอย่างมาก ความแตกต่างสำคัญบน 3 ไฟล์ ดังนี้
1. [lumpini_pipeline.py](lumpini_pipeline.py) ซึ่งเป็น source code ของ data pipeline ซึ่งสามารถอ่านรายละเอียดจาก comment ภายในไฟล์ได้
2. [Dockerfile](Dockerfile) ซึ่งดัดแปลงจาก Dockerfile ของ chospital โดยเพิ่มส่วนการ install Google Chrome สำหรับทำงานร่วมกับ Selenium
3. [crontab](crontab) มีการเปลี่ยนเล็กน้อบ จาก * * * * * ซึ่งหมายถึง ทำงานทุก 1 นาที เป็น 0 * * * * ซึ่งหมายถึงให้ทำงานในนาทีที่ 0 ของทุกชั่วโมง
   
## คำสั่ง Docker

สร้าง Docker Image จาก source code ด้วยคำสั่งดังนี้
```
docker build --tag lumpini:1.0 .
```

สำหรับ Mac OS ที่ใช้ Apple Chip ใช้คำสั่งนี้ เพื่อเลือก Dockerfile เป็น Dockerfile.macos
```
docker build --tag lumpini:1.0 --file Dockerfile.macos .
```

สร้าง Docker Container จาก Docker Image ที่สร้างสำเร็จข้างต้น ด้วยคำสั่งดังนี้
```
docker run --name lumpini_test -it -d lumpini:1.0
```
