
import torch
from ultralytics import YOLO
import gradio as gr
from PIL import Image, ImageDraw

# โหลดโมเดล YOLO โดยใช้ ultralytics
model_path = 'best.pt'  # เปลี่ยนชื่อไฟล์ตามที่คุณอัปโหลด
model = YOLO(model_path)  # โหลดโมเดลโดยตรงจาก ultralytics

def inference(gr_input):
    """
    ฟังก์ชัน inference สำหรับ Gradio
    """
    # ทำการ inference ด้วยโมเดล YOLO
    results = model(gr_input)

    # วาดกรอบผลการทำนายลงบนรูปภาพ
    draw_prediction = ImageDraw.Draw(gr_input)
    for result in results:
        for box in result.boxes:
            x, y, x2, y2 = box.xyxy[0]  # ตำแหน่งกรอบที่ตรวจพบ
            score = box.conf[0]  # ความมั่นใจของการทำนาย
            if score > 0.5:  # กำหนด threshold เพื่อแสดงเฉพาะผลที่น่าเชื่อถือ
                draw_prediction.rectangle((x, y, x2, y2), outline="red", width=2)
    return gr_input

# กำหนดอินพุตและเอาต์พุตสำหรับ Gradio
imagein = gr.Image(label="Input Image", type="pil")
imageout = gr.Image(label="Predicted Image", type="pil")

# สร้างอินเตอร์เฟส Gradio
interface = gr.Interface(
    fn=inference,
    inputs=imagein,
    outputs=imageout,
    title="Potholes detection",
)

# เริ่มรันอินเตอร์เฟส
if __name__ == "__main__":
    interface.launch(server_name="0.0.0.0", server_port=8080)  # ปรับให้ทำงานบนพอร์ต 8080 สำหรับ Koyeb
