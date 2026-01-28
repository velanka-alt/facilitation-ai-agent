# Facilitation AI Agent

퍼실리테이터의 설계, 운영, 회고를 돕는 실무형 AI 에이전트입니다.

## 구성
- `docs/`: 미션, 가드레일, 용어, 단계별 계획, 매칭 규칙, 검수 필요 목록
- `scenarios/`: 모드별 입력/출력 템플릿과 사용 가이드
- `tests/`: 입력 샘플과 기대 출력
- `samples/`: 익명화된 레퍼런스 텍스트 추출본과 인덱스

## 기본 흐름
1) 모드 선택 (A/B/C)
2) 입력 템플릿 작성
3) 출력 템플릿에 맞춰 산출물 생성
4) 테스트 케이스로 품질 확인

## 레퍼런스 사용
- 매칭 규칙: `docs/matching_rules.md`
- 샘플 인덱스: `samples/gesia_all/_index.csv`
- 샘플 형식: `samples/gesia_all`는 원본의 텍스트 추출본(`.txt`)만 포함
- 원본 확인 필요 목록: `docs/verification_needed.csv`
