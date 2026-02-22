BASE_URL = "https://oasis.jbnu.ac.kr"

LOGIN_HEADER = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/144.0.0.0 Safari/537.36",
    "Referer": f"{BASE_URL}/com/login.do",
    "Origin": f"{BASE_URL}",
    "X-Requested-With": "XMLHttpRequest"
}

LOGIN_URL = f"{BASE_URL}/com/com/sstm/logn/findLoginNXOS.action"

LOGIN_OTP_TRIGGER = f"{BASE_URL}/com/com/sstm/logn/otpProcess.action"

LOGIN_OTP_CHECK = f"{BASE_URL}/com/com/sstm/logn/otpCheck.action"

SCORE_URL = f"{BASE_URL}/uni/uni/scor/view/findCmpltScoreInq.action?version=0"

# 공대 관련 페이로드
SCORE_PAYLOAD = {
    "rType": "B1", 
    "strUnivCd": "3000000001",
    "strmjDeepCourYn": "Y"
}

STD_INFO_URL = f"{BASE_URL}/uni/uni/sreg/sreb/findSregMattrMngt.action?version=0"

COURSES_TAKEN_URL = f"{BASE_URL}/uni/uni/scor/view/findCmpltScoreInq.action?version=0"

COURSES_TAKEN_PAYLOAD = {
    "rType": "C",
    "cptnFg": ""
}