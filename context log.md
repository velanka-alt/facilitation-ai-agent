# Context Log (예시)

## 목적
- 이 문서는 프로젝트 참여자가 중간에 합류하더라도 지금까지의 진행 상황과 영향 범위를 빠르게 이해하도록 만든다.
- PR/브랜치/문서/웹 MVP 등 모든 작업 흐름과 의존성을 기록한다.

## 프로젝트 정보
- Repo: `facilitation-ai-agent`
- 작업 경로: `D:\AI Agent\AI Agent\facilitation-ai-agent`
- 현재 날짜: 2026-02-02 (월)

---

## 1) 현재 진행 상태 요약
- **문서/키워드/샘플/웹 MVP 작업은 대부분 완료**되었고, **PR 리뷰/머지 단계**로 넘어간 상태.
- PR은 기본 5개 + 후속 패치 2개까지 **총 7개** 존재.
- 머지 순서 및 PR 의존성이 중요함(특히 tool-frame docs + 후속 패치).

---

## 2) 브랜치 / PR 현황 (현재 기준)

### 기본 PR 5개
1. `w1/tool-frame-docs`
   - 내용: `tool_frame_reference.md`, `tool_frame_keywords.md` 생성
   - 상태: PR 생성됨 (리뷰 대기)

2. `mode-c/refine-template`
   - 내용: Mode C 템플릿 확장 + 샘플 3개 업데이트
   - 상태: PR 생성됨 (리뷰 대기)

3. `mvp/web-app`
   - 내용: Flask MVP 웹 앱 추가 (카드+점수 기반 추천)
   - 상태: PR 생성됨 (리뷰 대기)

4. `docs/facilitation-qna`
   - 내용: 100Q&A md화 + 오탈자 정리 (101번 삭제)
   - 상태: PR 생성됨 (리뷰 대기)

5. (기존) `Mode A` 관련 템플릿/샘플은 이미 완료된 상태(별도 PR 존재)

### 후속 패치 PR 2개
6. `tool-keywords-tuning`
   - 내용: 키워드 사전 변형 보강 (스테이크홀더, 라이프 라인, 갤러리 워크, 포인트 쉐어링 등)
   - **base는 w1/tool-frame-docs**
   - 상태: PR 생성됨 (리뷰 대기)

7. `mvp-usability-mode-check`
   - 내용: Mode B 샘플 인코딩 깨짐 해결 + 내용 전면 정리
   - 상태: PR 생성됨 (리뷰 대기)

8. `mvp-usability-tuning`
   - 내용: MVP 추천 로직 개선 (인원수 기반 가중치, 키워드 없을 때 기본 추천, 추천 이유 표시)
   - **base는 mvp/web-app**
   - 상태: PR 생성됨 (리뷰 대기)

---

## 3) 머지 순서 (필수)
1. `w1/tool-frame-docs`
2. `tool-keywords-tuning` (후속 패치)
3. `mode-c/refine-template`
4. `mvp/web-app`
5. `mvp-usability-tuning` (후속 패치)
6. `mvp-usability-mode-check`
7. `docs/facilitation-qna`

---

## 4) 주요 파일 변경 사항 요약

### 도구/키워드 문서
- `docs/tool_frame_reference.md`: 툴/프레임 기준 레퍼런스 문서
- `docs/tool_frame_keywords.md`: 매칭용 키워드 사전
- 후속 패치에서 키워드 변형(띄어쓰기/영문) 보강

### Mode C 템플릿
- `scenarios/mode_c/input_template.md`: 입력 필드 확장
- `scenarios/mode_c/output_template.md`: 추천 옵션 구조 확장
- `tests/mode_c_sample_01~03.md`: 샘플 새 포맷 반영

### Mode B 샘플 정리
- `tests/mode_b_sample_01~06.md`: 한글 깨짐 해결 + 내용 전면 정리

### 웹 MVP
- `app/app.py`: 카드 매칭 로직 + 인원수 기반 가중치 + fallback 추천
- `app/templates/index.html`: 추천 이유, fallback notice 표시
- `app/static/style.css`: UI 스타일(추천 이유/notice 추가)

### Q&A 문서
- `docs/facilitation_qna_100.md`: 100문항 Q&A md화

---

## 5) 웹 MVP 사용 방법 (간단)
```
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
python app/app.py
```
- 입력 필드: 목적 / 사용 상황 / 인원수
- 키워드 매칭이 없으면 기본 추천 표시

---

## 6) 외부 테스트 링크 (참고)
- Cloudflare Tunnel 사용 경험 있음 (임시 URL)
- 현재 활성 URL은 갱신 필요 (세션 종료 시 만료)

---

## 7) 작업자별 역할 (머지 이후 기준)

- 작업자 1: 레퍼런스/키워드 문서 최종 검수 + Q&A 오탈자 확인
- 작업자 2: Mode B/C 샘플 품질 검증 + MVP 동작 테스트
- 작업자 3: Mode A 템플릿/샘플 구조 확인
- 작업자 4: 배포/외부 테스트 가이드 정리

---

## 8) 주의사항
- **PR base 확인 필수**: 후속 패치는 반드시 원 PR 위에 쌓아야 충돌 최소화
- 병합 후 `main` 기준 재점검 필요
- `.venv`, `cloudflared.log` 등은 gitignore 처리됨

---

## 9) 다음 해야 할 일 (요약)
1) PR 리뷰 요청/수집
2) 머지 순서대로 병합
3) 머지 후 체크리스트 실행
4) 최종 README/가이드 통합 정리

---

## 작성자 메모
- 본 로그는 협업자가 중간 합류 시 빠르게 상황을 이해하도록 만든 지침서 초안
- 업데이트 시: PR 상태/머지 완료 여부/새 작업 내용을 계속 기록할 것

