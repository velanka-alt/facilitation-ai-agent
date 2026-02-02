# Context Log

## 목적
- 이 문서는 프로젝트 참여자가 중간에 합류하더라도 지금까지의 진행 상황과 영향 범위를 빠르게 이해하도록 만든다.
- PR/브랜치/문서/웹 MVP 등 모든 작업 흐름과 의존성을 기록한다.

## 프로젝트 정보
- Repo: `facilitation-ai-agent`
- 작업 경로: `D:\AI Agent\AI Agent\facilitation-ai-agent`
- 현재 날짜: 2026-02-02 (월)

---

## 1) 최근 업데이트 (2026-02-02)
- `mvp-usability-tuning`: 전 모드에 전문 설계/컨설팅 권고 문구 규칙을 적용
- 장시간 기준을 **8시간 이상**으로 명시
- Mode A: 입력 템플릿 확장, README 동기화, 온라인 샘플 1건 추가
- Mode B/C: 입력 템플릿에 복잡 조건 여부 필드 추가
- `docs/style_guide.md`: 표준 권고 문구와 적용 조건 명시
- `docs/PR_GUIDE.md`: PR 생성 가이드 추가
- `.github/PULL_REQUEST_TEMPLATE.md`: PR 템플릿 확장(범위/의존성/검증 항목 명시)
- `docs/escalation_guide.md`: AI/컨설팅 경계 가이드 추가
- `docs/output_phrasing_bank.md`: 출력 문구 모음 추가

---

## 2) 브랜치 / PR 후보 목록 (상태 확인 필요)
- `w1/tool-frame-docs`: 툴/프레임 레퍼런스 + 키워드 사전 생성
- `tool-keywords-tuning`: 키워드 변형 보강 (base: `w1/tool-frame-docs`)
- `mode-c/refine-template`: Mode C 템플릿 확장 + 샘플 업데이트
- `mvp/web-app`: Flask 기반 MVP 웹 앱 추가
- `mvp-usability-tuning`: MVP 추천 로직 개선 + 컨설팅 권고 규칙/Mode A 업데이트 + PR 가이드/템플릿 + 경계 가이드 + 출력 문구 모음
- `mvp-usability-mode-check`: Mode B 샘플 정리
- `docs/facilitation-qna`: 100 Q&A 문서화
- `docs/context-log`: 컨텍스트 로그 추가 (필요 시 반영)

---

## 3) 머지 순서 (권장)
1. `w1/tool-frame-docs`
2. `tool-keywords-tuning`
3. `mode-c/refine-template`
4. `mvp/web-app`
5. `mvp-usability-tuning`
6. `mvp-usability-mode-check`
7. `docs/facilitation-qna`

---

## 4) 주요 파일 변경 사항 요약

### 도구/키워드 문서
- `docs/tool_frame_reference.md`: 툴/프레임 레퍼런스
- `docs/tool_frame_keywords.md`: 매칭 키워드 사전

### Mode A 템플릿
- `scenarios/mode_a/input_template.md`: 입력 필드 확장
- `scenarios/mode_a/output_template.md`: 권고 문구 규칙 추가
- `tests/mode_a_sample_05.md`: 온라인 샘플 추가

### Mode B/C 템플릿
- `scenarios/mode_b/input_template.md`: 복잡 조건 여부 필드 추가
- `scenarios/mode_c/input_template.md`: 복잡 조건 여부 필드 추가

### 공통 스타일 가이드
- `docs/style_guide.md`: 권고 문구 기준 및 표준 문구 추가

### PR 운영 가이드
- `docs/PR_GUIDE.md`: PR 생성 가이드 추가
- `.github/PULL_REQUEST_TEMPLATE.md`: PR 템플릿 확장

### 경계 가이드
- `docs/escalation_guide.md`: AI/컨설팅 경계 가이드 추가

### 문구 모음
- `docs/output_phrasing_bank.md`: 출력 문구 모음 추가

---

## 5) 웹 MVP 사용 방법 (간단)
```
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
python app/app.py
```

---

## 6) 다음 해야 할 일 (요약)
1) PR 상태 확인 및 리뷰 요청
2) 권장 순서대로 머지
3) 머지 후 샘플/템플릿 일관성 재점검

---

## 작성자 메모
- 업데이트 시: PR 상태/머지 완료 여부/새 작업 내용을 계속 기록할 것
