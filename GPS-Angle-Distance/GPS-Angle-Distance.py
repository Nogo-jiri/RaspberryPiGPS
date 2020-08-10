#필요한 모듈 불러오기
import serial
import math
import json

#시리얼 포트 지정
SERIAL_PORT = "/dev/serial0"

#필요한 변수 선언
PosX = 0
PosY = 0
TarX = 0
TarY = 0
distance = 0
angle = 0

#목표 위치의 좌표값 불러오기
with open('TargetLocation.json') as json_file:
    json_TarLoc = json.load(json_file)
    TarY = float(json_TarLoc["TargetLatitude"])
    TarX = float(json_TarLoc["TargetLongitude"])

#GPS 모듈에서 받아온 데이터 파싱
def formatDegreesMinutes(coordinates, digits):
    parts = coordinates.split(".")
    if (len(parts) != 2):
        return coordinates
    if (digits > 3 or digits < 2):
        return coordinates
    left = parts[0]
    right = parts[1]
    degrees = str(left[:digits])
    minutes = str(right[:3])
    return degrees + "." + minutes

#파싱한 데이터에서 현재 위치의 좌표값 구하기
def getPositionData(gps):
    data = gps.readline()
    message = data[0:6]
    if (message == "$GPRMC"):
        parts = data.split(",")
        if parts[2] == 'V':
            print("GPS Module disabled")
        else:
            global PosX
            global PosY
            PosY = float(formatDegreesMinutes(parts[3], 2))
            PosX = float(formatDegreesMinutes(parts[5], 3))
    else:
        pass

#목표 위치의 좌표값과 현재 위치의 좌표값을 계산해 방위각과 거리 구하기
def calculation():
    global DisX
    global DisY
    global distance
    global angle
    DisX = (TarX - PosX) * 69.1 * math.cos(PosY / 57.3) * 1.6
    DisY = (TarY - PosY) * 69.1 * 1.6
    distance = (DisX ** 2 + DisY ** 2) ** 0.5
    angle = math.degrees(math.atan2(DisX,DisY))
    if angle < 0:
        angle += 360

'''
프로그램 시작
'''

print("프로그램을 시작합니다.")

#GPS 설정
gps = serial.Serial(SERIAL_PORT, baudrate = 9600, timeout = 0.5)

#유효한 값이 불러와질 때까지 현재 위치의 좌표값 불러오기
while PosX == 0:
    getPositionData(gps)

#방위각과 거리 계산
calculation()

#결과 출력
print("입력하신 목표 위치의 좌표는 위도 "+str(TarY)+", 경도 "+str(TarX)+"입니다.")
print("현재 위치의 좌표는 위도 "+str(PosY)+", 경도 "+str(PosX)+"입니다.")
print("목표 위치는 현재 위치로부터 방위각(동쪽) "+str(angle)+"°, "+str(distance)+" km만큼 떨어져 있습니다.")
