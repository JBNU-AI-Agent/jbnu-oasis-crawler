from pydantic import BaseModel, Field
from typing import Optional, Dict, Any

class LoginRequest(BaseModel):
    user_id: str
    user_pw: str
    otp: str  # <-- OTP를 로그인할 때 같이 받습니다!

class StudentInfoResponse(BaseModel):
    student_no: Optional[str] = Field(None, validation_alias="STDNO")  # 학번
    name: Optional[str] = Field(None, validation_alias="NM")     # 이름
    college: Optional[str] = Field(None, validation_alias="UNIVCDNM") # 단과대학
    department: Optional[str] = Field(None, validation_alias="MJCDNM") # 학과
    grade: Optional[str] = Field(None, validation_alias="SHTRNM") # 학년
    entrance_date: Optional[str] = Field(None, validation_alias="ENTRDT")      # 입학일자
    completed_semesters: Optional[str] = Field(None, validation_alias="TTCPTNSHTMCNT") # 이수학기
    curriculum_year: Optional[str] = Field(None, validation_alias="SUBMATTYY") # 교과과정년도
    gpa: Optional[str] = Field(None, validation_alias="TOTALSCORAVG") # 총 평점

    class Config:
        extra = "ignore" # 정의되지 않은 다른 필드는 무시하거나 "allow"로 설정
        
        
class CreditResponse(BaseModel):
    # validation_alias: "입력받을 때(XML)만 이 키를 써라"
    # 출력할 때는 변수명(major_type)으로 나갑니다.
    
    major_type: Optional[str] = Field(None, validation_alias="MAJORFG")          # 전공구분
    department: Optional[str] = Field(None, validation_alias="SUSTMIXNM")        # 학과
    category: Optional[str] = Field(None, validation_alias="GUBUN")              # 이수구분 (졸업학점/이수학점)
    
    # 학점 정보
    required_culture_points: Optional[str] = Field(None, validation_alias="MINCULTPNT") # 교양필수
    required_major_points: Optional[str] = Field(None, validation_alias="MINMJNECEPNT")     # 전공필수
    choice_major_points: Optional[str] = Field(None, validation_alias="MINMJCHOICEPNT")     # 전공선택
    
    total_points: Optional[str] = Field(None, validation_alias="GRDTPNT")        # 총 학점

    class Config:
        populate_by_name = True
        extra = "ignore"