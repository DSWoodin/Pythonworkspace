# 케니 에지 알고리즘은 에지 검출의 최적화를 위해
# 최소 오류율, 위치 정확도, 한 두께라는 기준을 사용함

# 최소 오류율
# 케니 에지 알고리즘은 에지를 검출할 때 
# 참 양성(True Positive, 실제 에지를 올바르게 검출한 것)을 높이고 
# 거짓 양성(False Positive, 에지가 아닌데 잘못 검출한 것)을 낮추려
# 에지 검출을 최적화하는 여러 단계(ex. 소벨 필터를 통한 그레이디언트
# 계산, 비최대 억제 등)를 통해서 최소 오류율을 달성함

# 위치 정확도
# 검출된 에지의 위치가 실제 에지의 위치와 얼마나 정확하게 일치하는가
# 케니 알고리즘은 이를 위해 그레이디언트의 최대값(-> 최대 에지강도)을
# 찾아내고, 이를 기준으로 에지의 위치를 결정 -> 위치 정확도의 최대화

# 한 두께
# 검출된 에지가 한 픽셀 두께(One-pixel wide)로 나타나도록 하는 것이
# 케니 알고리즘의 목표임, 이를 위해 비최대 억제(NMS)을 사용함

# 비최대 억제(Non-Maximum Suppression)는 에지 화소에 적용하는데,
# 에지 방향에 수직인 두 이웃 화소의 에지 강도가 자신보다 작아야만
# 에지로 살아남고, 그렇지 않으면 에지가 아닌 화소로 바뀜
# 다시 말해 두 이웃 화소와 비교해 자신이 최대가 아니면 억제됨

# 케니 알고리즘은 거짓 양성을 줄이기 위해 2개의 이력 임계값을 사용함
# Tlow와 Thigh를 사용하는데, 에지 추적은 에지 강도가 Thigh 이상인
# 화소에서 시작함, 이후 추적은 Tlow 임계값을 넘는 에지들로 진행됨
# 즉, 추적 이력이 있는 이웃을 가진 화소는 에지 강도가 낮더라도
# 실제 에지로 인정하게 됨

# 이렇게 Thigh보다 에지 강도가 높은 '강한 에지'와 Tlow~Thigh 사이에
# 있는 '약한 에지'만 실제 에지로 인정하는 히스테리시스(Hysteresis)
# 과정을 통해 에지를 검출함, 캐니는 Thigh를 Tlow의 2~3배로 권고함

# 최종 캐니 에지 검출 과정
# 1. 가우시안 필터(스무딩 필터)를 이용한 노이즈 감소 (이미지 전처리)
# 2. 소벨 필터를 이용해 에지 강도의 방향을 계산 (그레이디언트 계산)
# 3. 비최대 억제를 이용해 한 두께의 에지로 만듬
# 4. 이중 임계값을 이용해 에지를 강한 에지와 약한 에지로 분류
# 5. 히스테리시스로 강한 에지와 연결된 약한 에지를 최종 에지로 결정

import cv2 as cv

img = cv.imread('source/ch4/soccer.jpg')

gray = cv.cvtColor(img, cv.COLOR_BGR2GRAY)

# OpenCV에서는 캐니 알고리즘을 구현한 Canny() 함수를 제공함
# Canny(영상, Tlow, Thigh, 소벨 필터 크기(default:3), L2gradient)

# 소벨 필터 크기는 default가 3인데, 이는 3x3 사이즈의 필터를
# 사용하겠다는 의미이고, 커널 크기는 일반적으로 3,5,7등의 홀수 값

# 마지막 파라미터 L2gradient는 default가 False로 설정되어 있음
# False는 L1 노름을 사용하여 그레이디언트 계산 (|Gx| + |Gy|)
# True는 L2 노름으로 계산 (np.sqrt(Gx**2 + Gy**2))
# L2gradient=True로 설정하면 더욱 정확한 에지 강도를 제공함
canny1 = cv.Canny(gray, 50, 150)
canny2 = cv.Canny(gray, 100, 200)

cv.imshow('Original',gray)
cv.imshow('Canny1',canny1)
cv.imshow('Canny2',canny2)

# 이력 임계값이 높은 canny2의 경우 더욱 확실한, 즉 에지 강도가
# 큰 화소만 추적하기 때문에 더 적은 에지가 발생한 것을 확인
# 예를 들면 등번호 3에서 획의 일부가 손실되었음

# 반대로 이력 임계값이 낮은 canny1의 경우에는 등번호 3번이 온전히
# 검출된 대신에, 잔디밭에서 잠음 에지가 많이 발생함

cv.waitKey()
cv.destroyAllWindows()

# 1986년에 제안된 케니 에지 알고리즘은 지금까지도 가장 체계적인
# 에지 검출 이론으로 인정받지만, 이러한 에지 검출은 모두 명암에 의존
# 따라서 물체 경계에 나타난 진짜 에지와 그림자로 인한 가짜 에지를
# 구분하지 못함, 에지 검출 연구는 캐니 이후에 뚜렷한 개선이 없음