from fastapi import APIRouter, Depends, Body, HTTPException
from app.schemas.crawler import StudentInfoResponse, LoginRequest
from app.schemas.response import SuccessResponse, ErrorResponse
from app.services.oasis_service import OasisService
from app.crawlers.base import BaseCrawler
from app.crawlers.score import CreditCrawler
from app.crawlers.student_info import StudentInfoCrawler
from app.crawlers.taken_courses import TakenCourseCrawler
from typing import List
from app.schemas.crawler import CreditResponse, ScoreItem

router = APIRouter()

@router.post("/auth/session", response_model=SuccessResponse[dict], status_code=200)
async def get_session(
    # 로그인에 필요한 정보를 Body로 받아야 합니다 (기존 LoginRequest 스키마 활용 권장)
    req: LoginRequest,
    service: OasisService = Depends(OasisService)
):
    cookies = await service.login_and_get_cookies(req.user_id, req.user_pw, req.otp)
    
    if not cookies:
        # HTTPException import 필요
        from fastapi import HTTPException
        raise HTTPException(status_code=401, detail="Authentication failed")

    # SuccessResponse로 감싸서 반환
    return SuccessResponse(data=cookies)

@router.post("/student/info/sync", response_model=SuccessResponse[dict])
async def get_student_info(
    std_no: str = Body(...),      # 학번 (Payload 생성용)
    cookies: dict = Body(...),    # 로그인 세션 쿠키
    service: OasisService = Depends(OasisService),
    crawler: BaseCrawler = Depends(StudentInfoCrawler) # 학생 정보 크롤러 주입
):
    # 1. 서비스 로직 호출 (쿠키와 학번을 넘겨 데이터 수집)
    success = await service.sync_student_info(cookies, crawler, std_no) #
    
    # 2. 데이터 수집 실패 시 예외 처리
    if not success:
        raise HTTPException(status_code=400, detail="Failed to sync data")
        
    # 3. 성공 응답 반환 (SuccessResponse가 자동으로 Pydantic 모델 변환)
    return SuccessResponse(data={"message": "Student info synchronized successfully"})

@router.get("/student/info/{std_no}", response_model=SuccessResponse[StudentInfoResponse])
async def read_student_info(
    std_no: str,
    service: OasisService = Depends(OasisService)
):
    """[응답 전용] DB에 저장된 학생 정보를 조회합니다. (쿠키 필요 없음)"""
    data = await service.get_student_info_from_db(std_no)
    
    if not data:
        raise HTTPException(status_code=404, detail="Data not found. Please sync first.")
        
    return SuccessResponse(data=data)

@router.post("/credits/sync", response_model=SuccessResponse[dict])
async def sync_credits(
    std_no: str = Body(...),
    cookies: dict = Body(...),
    service: OasisService = Depends(OasisService),
    crawler: BaseCrawler = Depends(CreditCrawler)
):
    """[저장 전용] 학교 서버에서 성적 정보를 가져와 DB를 업데이트합니다."""
    success = await service.sync_credits(cookies, crawler, std_no)
    
    if not success:
         return SuccessResponse(data={"message": "No data found or sync failed"})
        
    return SuccessResponse(data={"message": "Credits synchronized successfully"})


@router.get("/credits/{std_no}", response_model=SuccessResponse[List[CreditResponse]])
async def read_credits(
    std_no: str,
    service: OasisService = Depends(OasisService)
):
    """[응답 전용] DB에 저장된 성적 정보를 조회합니다."""
    data = await service.get_credits_from_db(std_no)
    
    # 데이터가 없으면 빈 리스트 반환 (혹은 404)
    return SuccessResponse(data=data)


@router.post("/taken-courses/sync", response_model=SuccessResponse[None])
async def sync_courses(
    std_no: str = Body(...),
    cookies: dict = Body(...),
    service: OasisService = Depends(OasisService),
    crawler: BaseCrawler = Depends(TakenCourseCrawler)
):
    """[저장 전용] 학교 서버에서 수강 과목 정보를 가져와 DB를 업데이트합니다."""
    success = await service.sync_taken_courses(cookies, crawler, std_no)
    
    if not success:
         return ErrorResponse(message = "No data found or sync failed")
        
    return SuccessResponse(message = "Taken courses list synchronized successfully")

@router.get("/taken-courses/{std_no}", response_model=SuccessResponse[List[ScoreItem]])
async def get_courses(
    std_no: str,
    service: OasisService = Depends(OasisService)
):
    """[응답 전용] DB에 저장된 수강과목 정보를 조회합니다."""
    
    data = await service.get_courses_from_db(std_no)
    
    # 데이터가 없으면 빈 리스트 반환 (혹은 404)
    return SuccessResponse(data=data)