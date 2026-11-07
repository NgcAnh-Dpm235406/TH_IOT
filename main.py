from machine import Pin, PWM, ADC
import time

# 1. CẤU HÌNH GÓC ĐẶC BIỆT
GOC_SO_12 = 0    # Không hoạt động -> chỉ số 12 (0 độ)
GOC_SO_1  = 30   # 12 giờ đúng -> 6 động cơ đều chỉ số 1 (30 độ)

# 2. KHỞI TẠO 6 SERVO (TẦN SỐ 50Hz)
servo_h1 = PWM(Pin(13), freq=50)
servo_h2 = PWM(Pin(12), freq=50)
servo_m1 = PWM(Pin(14), freq=50)
servo_m2 = PWM(Pin(27), freq=50)
servo_s1 = PWM(Pin(26), freq=50)
servo_s2 = PWM(Pin(25), freq=50)

tat_ca_servo = [servo_h1, servo_h2, servo_m1, servo_m2, servo_s1, servo_s2]

# 3. KHỞI TẠO 3 BIẾN TRỞ
pot_gio  = ADC(Pin(34))
pot_phut = ADC(Pin(35))
pot_giay = ADC(Pin(32))

pot_gio.atten(ADC.ATTN_11DB)
pot_phut.atten(ADC.ATTN_11DB)
pot_giay.atten(ADC.ATTN_11DB)

# 4. HÀM QUAY SERVO VÀ TÍNH GÓC
def quay_servo(servo, goc):
    goc = max(0, min(180, goc))
    duty = int(26 + (goc / 180.0) * (128 - 26))
    servo.duty(duty)
    return int(goc)

def dieu_khien_cap_servo(servo_1, servo_2, gia_tri, chu_ky_max):
    nua_chu_ky = chu_ky_max / 2.0
    if gia_tri <= nua_chu_ky:
        g1 = quay_servo(servo_1, (gia_tri / nua_chu_ky) * 180.0)
        g2 = quay_servo(servo_2, GOC_SO_12)
    else:
        g1 = quay_servo(servo_1, GOC_SO_12)
        g2 = quay_servo(servo_2, ((gia_tri - nua_chu_ky) / nua_chu_ky) * 180.0)
    return g1, g2

for s in tat_ca_servo:
    quay_servo(s, GOC_SO_12)

print("=== HE THONG DONG HO 6 SERVO DA SAN SANG ===")
print("Hay dung chuot xoay 3 bien tro ben trai de chinh Gio - Phut - Giay!")

luu_thoi_gian = (-1, -1, -1)

# 5. VÒNG LẶP CHÍNH
while True:
    gio  = round((pot_gio.read()  / 4095.0) * 12)
    phut = round((pot_phut.read() / 4095.0) * 60)
    giay = round((pot_giay.read() / 4095.0) * 60)

    # Chỉ cập nhật và in ra màn hình đen khi bạn xoay biến trở làm đổi thời gian
    if (gio, phut, giay) != luu_thoi_gian:
        luu_thoi_gian = (gio, phut, giay)

        if (gio == 12 and phut == 0 and giay == 0) or (gio == 12 and phut == 60 and giay == 60):
            for s in tat_ca_servo:
                quay_servo(s, GOC_SO_1)
            print(f"Thoi gian: {gio:02d}:{phut:02d}:{giay:02d} -> [12 GIO DUNG] Ca 6 Servo deu chi SO 1 (30 do)")
        else:
            h1, h2 = dieu_khien_cap_servo(servo_h1, servo_h2, gio,  12)
            m1, m2 = dieu_khien_cap_servo(servo_m1, servo_m2, phut, 60)
            s1, s2 = dieu_khien_cap_servo(servo_s1, servo_s2, giay, 60)
            print(f"Thoi gian: {gio:02d}:{phut:02d}:{giay:02d} | Gio({h1}°, {h2}°) | Phut({m1}°, {m2}°) | Giay({s1}°, {s2}°)")

    time.sleep_ms(50)