import requests
import asyncio
import xml.etree.ElementTree as ET
from functools import partial
from app.utils import get_logger
from typing import List, Dict, Optional
from app.core import constants as const

logger = get_logger("oasis.client")

class OasisClient:
    """
    [Facade Pattern]
    복잡한 3단계(ID/PW -> Trigger -> OTP) 인증 과정을
    단 하나의 메서드(authenticate)로 캡슐화합니다.
    """
    def __init__(self):
        self.session = requests.Session()
        self.headers = const.LOGIN_HEADER
        self.session.headers.update(self.headers)

    async def _async_post(self, url, **kwargs):
        """requests.post를 비동기 스레드에서 실행"""
        func = partial(self.session.post, url, **kwargs)
        return await asyncio.to_thread(func)

    async def authenticate(self, user_id: str, user_pw: str, otp: str) -> dict | None:
        """
        [핵심] 외부에서는 이 함수 하나만 호출하면 됩니다.
        내부적으로 3번의 HTTP 요청을 순차적으로 처리하고 쿠키를 반환합니다.
        """
        try:
            # --- [Step 1] ID/PW 검증 ---
            payload_login = {
                "rType": "3tier", "loginType": "3tier", "userUid": user_id, "userPwd": user_pw,
                "langFg": "K", "loginGubun": "O", "loginSystem": "oasis"
            }
            res1 = await self._async_post(const.LOGIN_URL, json=payload_login)
            if res1.status_code != 200:
                logger.warning(f"Step 1 Failed: {res1.status_code}")
                return None

            # --- [Step 2] OTP 프로세스 트리거 (서버 상태 변경용) ---
            # 구글 OTP라도 서버 내부 플래그를 위해 호출해주는 게 안전합니다.
            res2 = await self._async_post(const.LOGIN_OTP_TRIGGER, data={"userId": user_id})
            if res2.status_code != 200:
                logger.warning(f"Step 2 Failed: {res2.status_code}")
                return None

            # --- [Step 3] OTP 코드 검증 ---
            res3 = await self._async_post(const.LOGIN_OTP_CHECK, data={"userCode": otp})
            
            # 쿠키 확인 (성공 시 JSESSIONIDSSO 발급됨)
            if "JSESSIONIDSSO" in self.session.cookies:
                logger.info(f"User {user_id}: Authentication successful")
                return self.session.cookies.get_dict()
            else:
                logger.warning(f"Step 3 Failed: Invalid OTP or Session")
                return None

        except Exception as e:
            logger.error(f"Authentication Error: {e}")
            return None

    async def fetch_xml(self, url: str, xml_payload: str) -> Optional[List[Dict[str, str]]]:
        headers = {"Content-Type": "text/xml"}
        try:
            res = await self._async_post(url, data=xml_payload, headers=headers)
            if res.status_code == 200:
                return self._parse_nexacro_xml(res.text)
            return None
        except Exception as e:
            logger.error(f"XML 데이터 요청 실패: {e}")
            return None

    def build_payload(self, std_no: str, extra_params: dict | None) -> str:
        """
        std_no와 쿠키는 기본으로 포함하고, 
        extra_params로 rType이나 기타 파라미터를 덮어쓰거나 추가합니다.
        """
        # 1. 기본 파라미터 설정
        params = {
            "stdNo": std_no,
            "rType": "Tab1", # 기본값
            "sRes": "Y"
        }
        
        # 2. 쿠키 추가
        params.update(self.session.cookies.get_dict())
        
        # 3. 추가 파라미터 병합 (사용자가 넘긴 값으로 덮어씀)
        if extra_params:
            params.update(extra_params)

        # 4. XML 생성
        param_xml_list = []
        for k, v in params.items():
            param_xml_list.append(f'<Parameter id="{k}">{v}</Parameter>')
            
        params_str = "".join(param_xml_list)

        return f"""<?xml version="1.0" encoding="UTF-8"?>
        <Root xmlns="http://www.nexacroplatform.com/platform/dataset">
            <Parameters>
                {params_str}
            </Parameters>
        </Root>"""

    def _parse_nexacro_xml(self, xml_string: str) -> List[Dict[str, str]]:
        """
        어떤 넥사크로 XML 응답이든 파싱해서 Dictionary 형태로 반환합니다.
        구조: {
            "Parameters": {파라미터들...},
            "Datasets": {
                "DS_성적": [DataFrame],
                "DS_시간표": [DataFrame],
                ...
            }
        }
        """
        root = ET.fromstring(xml_string)
        
        # 2. 네임스페이스 제거 로직
        for el in root.iter():
            if '}' in el.tag:
                el.tag = el.tag.split('}', 1)[1]
                
        # result = {
        #     "Parameters": {},
        #     "Datasets": {}
        # }
        
        # params_node = root.find("Parameters")
        # if params_node is not None:
        #     for param in params_node.findall("Parameter"):
        #         p_id = param.get("id")
        #         p_val = param.text if param.text else ""
        #         result["Parameters"][p_id] = p_val
        
        for dataset in root.findall("Dataset"):
            # ds_id = dataset.get("id")
            
            row_list = []
            rows = dataset.find("Rows")
            
            if rows is not None:
                for row in rows.findall("Row"):
                    row_data = {}
                    for col in row.findall("Col"):
                        col_id = col.get("id")
                        col_val = col.text
                        row_data[col_id] = col_val
                    row_list.append(row_data)
            
        return row_list
    
            # if row_list:
            #     result["Datasets"][ds_id] = pd.DataFrame(row_list)
            # else:
            #     result["Datasets"][ds_id] = pd.DataFrame()
        
                