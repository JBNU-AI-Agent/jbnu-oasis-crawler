from pydantic import BaseModel, Field, BeforeValidator, ConfigDict
from typing import Optional, Dict, Any, List, Annotated

def empty_to_zero(v):
    """
    넥사크로 XML 특성상 값이 없으면 빈 문자열("")로 넘어옵니다.
    이 값을 float으로 변환하려 하면 에러가 나므로, 빈 값이면 0.0을 반환합니다.
    """
    if v == "" or v is None:
        return 0.0
    return float(v)

# 이 타입을 쓰면 아무리 이상한 빈 문자가 와도 안전하게 숫자(float)로 바뀝니다.
SafeFloat = Annotated[float, BeforeValidator(empty_to_zero)]

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


# 개별 과목 스키마 (알맹이)
class ScoreItem(BaseModel):
    model_config = ConfigDict(populate_by_name=True)
    # validation_alias: 입력받을 때만 "YY"를 찾고, 출력은 "year"로 나갑니다.
    year: str = Field(validation_alias="YY", description="수강 년도 (예: 2021)")
    semester: str = Field(validation_alias="SHTMNM", description="학기명 (예: 1학기)")
    
    subject_code: str = Field(validation_alias="SBJTCD", description="과목 코드")
    subject_name: str = Field(validation_alias="SBJTNM", description="과목명")
    course_type: str = Field(validation_alias="CPTNFGNM", description="이수 구분 (교양, 전공필수 등)")
    
    # 학점과 평점은 안전하게 숫자로 변환합니다.
    credit: SafeFloat = Field(validation_alias="PNT", description="학점")
    gpa: SafeFloat = Field(validation_alias="DISGRDSCOR", default=0.0, description="평점 (예: 4.5, Pass 과목은 0.0)")
    
    # Pass/Fail 과목 등급
    grade: str = Field(validation_alias="DISPSCOR", default="", description="최종 등급 (A+, Pass 등)")
    
    # 🌟 핵심: 재수강이 아닌 일반 과목은 원본 데이터에 아예 'REMT' 태그가 없습니다.
    # 따라서 Optional[str]과 default=None으로 설정해 에러를 방지합니다.
    remarks: Optional[str] = Field(validation_alias="REMT", default=None, description="비고 (재이수신청 등)")