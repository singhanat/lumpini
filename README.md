# lumpini

## คำสั่ง Docker

สร้าง Docker Image จาก source code ด้วยคำสั่งดังนี้
```
docker build --tag lumpini:1.0 .
```

สร้าง Docker Container จาก Docker Image ที่สร้างสำเร็จข้างต้น ด้วยคำสั่งดังนี้
```
docker run --name lumpini_test -it -d lumpini:1.0
```

## สำหรับ Mac OS

สำหรับ Mac OS ที่ใช้ Apple Chip ใช้คำสั่งนี้ เพื่อเลือก Dockerfile เป็น Dockerfile.macos
```
docker build --tag lumpini:1.0 --file Dockerfile.macos .
```

สำหรับ Mac OS การ Run ต้องเพิ่ม option ดังนี้

```
docker run --name lumpini_test --add-host=host.docker.internal:host-gateway -it -d lumpini:1.0
```

## สำหรับ Linux

สร้าง Docker Image จาก source code ด้วยคำสั่งดังนี้
```
docker build --tag lumpini:1.0 .
```

สำหรับ Mac OS การ Run ต้องเพิ่ม option ดังนี้

```
docker run --name lumpini_test --add-host=host.docker.internal:host-gateway -it -d lumpini:1.0
```
