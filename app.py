from flask import Flask, request, jsonify

app = Flask(__name__)

# JSON 형태의 요청 본문을 파싱하기 위한 미들웨어 설정 (Flask는 기본적으로 처리)
# app.json_encoder = MyCustomJSONEncoder # 필요시 커스텀 인코더 설정 가능

@app.route('/kakao/chatbot', methods=['POST'])
def kakao_chatbot():
    # 1. 카카오톡으로부터 받은 요청 본문(JSON) 확인
    req = request.get_json()
    print(f"Received request: {req}") # 디버깅을 위해 요청 전체를 출력

    # 2. 사용자 발화(utterance) 추출
    # 카카오톡 챗봇 요청의 기본 구조는 userRequest -> utterance 입니다.
    utterance = req['userRequest']['utterance']
    print(f"User utterance: {utterance}") # 사용자 발화 출력

    # 3. 챗봇 응답 로직 (예시)
    response_text = ''
    if "안녕" in utterance:
        response_text = "안녕하세요! 무엇을 도와드릴까요?"
    elif "날씨" in utterance:
        response_text = "오늘 날씨는 맑고 따뜻합니다. 외출하기 좋은 날씨네요!"
    elif "시간" in utterance:
        import datetime
        now = datetime.datetime.now()
        response_text = f"현재 시간은 {now.hour}시 {now.minute}분입니다."
    else:
        response_text = "죄송합니다. 이해하지 못했습니다. 다시 말씀해주세요."

    # 4. 카카오톡 챗봇 응답 형식에 맞춰 JSON 생성
    # 카카오톡 챗봇 API의 'SimpleText' 응답 형식입니다.
    response_data = {
        "version": "2.0",
        "template": {
            "outputs": [
                {
                    "simpleText": {
                        "text": response_text
                    }
                }
            ]
        }
    }

    # 5. JSON 응답 전송
    return jsonify(response_data)

# 서버 시작
if __name__ == '__main__':
    # 개발 서버 실행 (모든 IP에서 접속 가능하도록 설정)
    # 실제 배포 시에는 Gunicorn, uWSGI 등 WSGI 서버를 사용해야 합니다.
    app.run(host='0.0.0.0', port=3000, debug=True)
    # debug=True는 개발 중 코드 변경 시 자동 재시작 및 디버깅 정보를 제공합니다.
    # 운영 환경에서는 debug=False로 설정해야 합니다.