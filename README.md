# Keycloak POC

> **개인 학습 프로젝트**
> FastAPI, SQLModel, Repository Pattern, Unit of Work 패턴을 학습하기 위한 POC 프로젝트입니다.

---

# 실행 방법

## 패키지 관리 (uv)

### 패키지 추가
```bash
uv add fastapi sqlalchemy
```

### dev 패키지 추가
```bash
uv add --dev pytest black
```

### 패키지 제거
```bash
uv remove requests
```

### 의존성 동기화 (설치)
```bash
uv sync
```

### 의존성 잠금 (uv.lock 업데이트)
```bash
uv lock
```

---

## 서버 실행

### FastAPI 서버 실행
```bash
uv run uvicorn main:app --reload
```

### Python 스크립트 실행
```bash
ENVFILE=envs/test.env uv run python src/main.py
```

---

## 코드 품질 관리 (ruff)

### Linting
전체 검사:
```bash
uv run ruff check src/
```

자동 수정:
```bash
uv run ruff check src/ --fix
```

Unsafe 수정 포함:
```bash
uv run ruff check src/ --fix --unsafe-fixes
```

### Formatting
포맷 적용:
```bash
uv run ruff format src/
```

포맷 검사만 (변경 안 함):
```bash
uv run ruff format src/ --check
```

### 통합 (추천)
Lint + Format 한 번에:
```bash
uv run ruff check src/ --fix && uv run ruff format src/
```

---

# 규칙
## core, domain 패키지 구분
core는 도메인을 몰라야 한다. 
core에 domain 쪽 import 금지.
domain에서 core import 할 것.

core는 공통, 추상화된 것이 들어가고 
domain은 도메인 특화된 것 넣을 것

### domain 마다 넣을 요소들
- dependencies.py (라우터에 의존성 주입용도)
- models.py (디비 모델)
- repository.py (디비 접근 구현체)
- router.py 
- schemas.py (dto)
- service.py (비즈니스 로직)
- unit_of_work.py (트랜잭션 경계)

일관성을 위해 단일 엔티티던, 여러 엔티티던 상관없이 unit_of_work로 묶어서 commit

repository는 flush()만 하므로 commit이 필요하면 반드시 unit_of_work 사용할 것

만약 통합 unit of work가 필요하다면, 새로운 domain aggregate가 발견된 것임 

---

## sync, async 구분

sync는 prefix 없음
async는 async prefix 있음

sync endpoint와 async endpoint 구분해서 unit of work와 repository 구현체 사용할 것


---

## 라우터 추가하려면
api_gateway에 추가할 것

---

# 모노레포 통합 방법

이 프로젝트를 더 큰 모노레포의 구성원으로 추가하는 방법입니다.

## 디렉토리 구조

```
monorepo/
├── services/
│   ├── keycloak-poc/          # 이 프로젝트
│   │   ├── src/
│   │   ├── pyproject.toml
│   │   └── README.md
│   ├── another-service/
│   └── worker-service/
├── libs/
│   └── shared/                # 공통 라이브러리 (선택사항)
├── pyproject.toml             # 워크스페이스 설정
└── README.md
```

---

## 통합 단계

### 1. 프로젝트 이동

```bash
# 모노레포 루트에서
mkdir -p services/keycloak-poc
cp -r /path/to/keycloak-poc/* services/keycloak-poc/
```

또는 Git 히스토리를 보존하려면:

```bash
# 모노레포 루트에서
git subtree add --prefix=services/keycloak-poc \
  https://github.com/username/keycloak-poc.git main
```

---

### 2. 워크스페이스 설정

**monorepo/pyproject.toml** 생성 또는 수정:

```toml
[tool.uv.workspace]
members = [
    "services/*",
    "libs/*"
]
```

---

### 3. 의존성 동기화

```bash
# 모노레포 루트에서
uv sync
```

---

## 실행 방법

### 독립 실행
```bash
cd services/keycloak-poc
uv run python src/main.py
```

### 모노레포 루트에서 실행
```bash
# 특정 서비스 실행
uv run --package keycloak-poc python src/main.py
```

---

## 공통 라이브러리 사용 (선택사항)

서비스 간 코드 공유가 필요한 경우:

**services/keycloak-poc/pyproject.toml:**
```toml
[project]
dependencies = [
    "shared-lib",  # libs/shared 참조
    "fastapi>=0.128.0",
    # ... 기타 의존성
]
```

**libs/shared/pyproject.toml:**
```toml
[project]
name = "shared-lib"
version = "0.1.0"
```

---

## 주의사항

- Import 경로는 변경 불필요 (각 서비스가 독립적)
- 각 서비스의 `src/`가 source root로 유지됨
- uv workspace가 의존성을 자동으로 관리

---

