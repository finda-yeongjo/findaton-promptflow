import json
import re
from promptflow import tool


@tool
def convert_to_json(data):
    # 문자열로 받아진 input data를 처리합니다.
    data_string = data.strip()
    
    # 데이터 항목들을 추출하기 위한 정규 표현식 사용
    pattern = re.compile(r'(\d+)\. ([^-]+) - ([^기]+) 기준 금리는 ([^,]+), 약정금액은 ([^(]+)\(([^\)]+)\)')
    matches = pattern.finditer(data_string)

    result = []
    for match in matches:
        result.append({
            "no": match.group(1),
            "name": match.group(2).strip(),
            "loan": match.group(3).strip(),
            "rate": match.group(4).strip(),
            "price": match.group(5).strip() + " (" + match.group(6).strip() + ")"
        })

    # 변환된 JSON 객체를 문자열로 변환하여 반환합니다.
    return json.dumps(result, ensure_ascii=False, indent=2)

# 테스트를 위한 데이터 문자열 (에러 로그에서 문자열 부분을 복사)
test_data = '''
[
    {
        "1. 롯데캐피탈 - 신용대출 기준 금리는 16.8%, 약정금액은 91,500,000(구천백오십만원)입니다."
        "2. 다올저축은행 - Fi모바일자동대출 기준 금리는 10.83%, 약정금액은 50,000,000(오천만원)입니다."
        "3. BNK경남은행 - BNK모바일신용대출 기준 금리는 5.25%, 약정금액은 49,000,000(사천구백만원)입니다."
    }
]
'''

# 첫번째 및 마지막 대괄호를 제거하고, 내부 딕셔너리의 시작과 끝 대괄호를 제거합니다.
# 이 부분은 입력된 데이터 문자열이 올바른 JSON 형식이 아니기 때문에 필요한 단계입니다.
test_data = test_data.strip()[1:-1].strip()[1:-1].strip()

# 함수 호출 및 결과 출력
converted_json = convert_to_json(test_data)
print(converted_json)