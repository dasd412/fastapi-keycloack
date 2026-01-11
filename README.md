# Keycloak POC

> **개인 학습 프로젝트**
> FastAPI, SQLModel, Repository Pattern, Unit of Work 패턴을 학습하기 위한 POC 프로젝트입니다.

---

## 프로젝트 구조

```
keycloak-poc/
├── src/
│   ├── main.py                     # 애플리케이션 진입점
│   ├── api_gateway.py              # 라우터 통합
│   ├── core/                       # 공통 모듈 (도메인 독립적)
│   │   ├── config/
│   │   │   └── settings.py         # 환경 설정
│   │   ├── repository/
│   │   │   └── postgres/
│   │   │       ├── base_model.py   # BaseModel (id, created_at, updated_at)
│   │   │       ├── repository.py   # PostgresRepository (Generic Base)
│   │   │       └── session.py      # Session 생성 및 관리
│   │   ├── service/
│   │   │   └── unit_of_work.py     # UnitOfWork Base
│   │   └── exception/
│   │       ├── base_exception.py
│   │       └── handler.py
│   └── domain/                     # 도메인별 모듈
│       └── system_setting/
│           ├── dependencies.py     # 의존성 주입
│           ├── models.py           # DB 모델
│           ├── repository.py       # Repository 구현
│           ├── router.py           # API 엔드포인트
│           ├── schemas.py          # DTO (Pydantic)
│           ├── service.py          # 비즈니스 로직
│           └── unit_of_work.py     # 트랜잭션 경계
├── docker/
│   └── init.sql                    # DB 초기화 SQL
├── Dockerfile
├── docker-compose.yml
├── pyproject.toml                  # 프로젝트 설정 및 의존성
└── README.md
```

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

### 로컬 개발 (Python)
FastAPI 서버 실행:
```bash
uv run uvicorn main:app --reload
```

환경 변수 파일 지정:
```bash
ENVFILE=envs/test.env uv run python src/main.py
```

### Docker Compose 실행
개발 환경 (PostgreSQL + FastAPI):
```bash
# 백그라운드 실행
docker-compose up -d

# 로그 확인
docker-compose logs -f app

# 중지
docker-compose down

# 데이터 포함 완전 삭제
docker-compose down -v
```

재빌드가 필요한 경우:
```bash
docker-compose up --build
```

### API 테스트
Swagger UI:
```
http://localhost:8000/docs
```

cURL 예제:
```bash
# CREATE
curl -X POST http://localhost:8000/api/v1/system_setting \
  -H "Content-Type: application/json" \
  -d '{"key": "test_key", "value": "test_value"}'

# READ (전체 목록)
curl http://localhost:8000/api/v1/system_setting

# READ (ID로 조회)
curl http://localhost:8000/api/v1/system_setting/{uuid}

# READ (Key로 조회)
curl http://localhost:8000/api/v1/system_setting/by-key/test_key

# UPDATE
curl -X PATCH http://localhost:8000/api/v1/system_setting/{uuid} \
  -H "Content-Type: application/json" \
  -d '{"value": "updated_value"}'

# DELETE
curl -X DELETE http://localhost:8000/api/v1/system_setting/{uuid}
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

---

## domain 마다 넣을 요소들
- **dependencies.py** - 라우터에 의존성 주입용도
- **models.py** - 디비 모델
- **repository.py** - 디비 접근 구현체 (Base Repository 상속)
- **router.py** - API 엔드포인트
- **schemas.py** - DTO (Pydantic 모델)
- **service.py** - 비즈니스 로직
- **unit_of_work.py** - 트랜잭션 경계

---

## 트랜잭션 관리 규칙

### 1. Repository는 flush()만 수행
- Repository의 CRUD 메서드는 `session.flush()`만 호출
- **절대 `session.commit()` 호출 금지**
- 트랜잭션 커밋은 상위 레이어(Service)에서 Unit of Work를 통해 관리

### 2. Unit of Work를 통한 트랜잭션 관리
일관성을 위해 **단일 엔티티든, 여러 엔티티든 상관없이** unit_of_work로 묶어서 commit

**Service 레이어에서 사용**:
```python
def create(self, data: SomeCreate) -> SomeModel:
    with self.uow:  # 트랜잭션 시작
        result = self.uow.some_repo.create(data.model_dump())
    return result  # 자동 커밋 (예외 발생 시 자동 롤백)
```

### 3. 읽기 전용 작업
읽기 전용 작업(get, list 등)은 Unit of Work 없이 Repository 직접 사용 가능:
```python
def get_by_id(self, uuid: UUID) -> SomeModel | None:
    return self.uow.some_repo.get_by_id(uuid)
```

### 4. 여러 Repository를 사용하는 경우
만약 통합 unit of work가 필요하다면, **새로운 domain aggregate가 발견된 것**임

---

## 의존성 주입 규칙

### Session 공유 원칙
**중요**: 하나의 요청에서 **단일 Session 인스턴스**만 생성하고 공유해야 함

**잘못된 예** (Session이 2개 생성됨):
```python
def get_repository(session: Annotated[Session, Depends(PGSession())]):
    return SomeRepository(session)  # 세션 A

def get_uow(
    session: Annotated[Session, Depends(PGSession())],  # 세션 B (다른 인스턴스!)
    repo: Annotated[SomeRepository, Depends(get_repository)]
):
    return SomeUnitOfWork(session, repo)  # ❌ repo와 uow가 다른 세션 사용
```

**올바른 예** (Session 1개만 생성):
```python
def get_uow(session: Annotated[Session, Depends(PGSession())]):
    repository = SomeRepository(session)  # 같은 세션 공유
    return SomeUnitOfWork(session, repository)  # ✅ 동일한 세션 사용
```

### sessionmaker 사용 필수
SQLModel의 `Session.exec()` 메서드를 사용하려면 `sessionmaker`에서 `class_=Session` 지정 필요:
```python
from sqlalchemy.orm import sessionmaker
from sqlmodel import Session

sessionmaker(
    class_=Session,  # ✅ SQLModel Session 사용
    autocommit=False,
    autoflush=False,
    expire_on_commit=False,
    bind=engine,
)
```

---

## sync, async 구분

sync는 prefix 없음
async는 async prefix 있음

sync endpoint와 async endpoint 구분해서 unit of work와 repository 구현체 사용할 것

---

## 라우터 규칙

### 1. API 엔드포인트 추가
새 라우터를 추가하려면 `api_gateway.py`에 등록:
```python
from domain.new_domain.router import new_router

basic_router.include_router(new_router)
```

### 2. 에러 처리
- **404 Not Found**: 리소스가 없을 때 `HTTPException` 발생
- **204 No Content**: UPDATE, DELETE 성공 시 response body 없음
- **201 Created**: CREATE 성공 시 생성된 객체 반환

### 3. 경로 충돌 방지
Path parameter 사용 시 충돌 방지:
```python
# ❌ 잘못된 예 (/{uuid}와 /{key} 충돌)
@router.get("/{uuid}")
@router.get("/{key}")

# ✅ 올바른 예 (명시적 경로 구분)
@router.get("/{uuid}")
@router.get("/by-key/{key}")
```

---

## 명명 규칙

### 파일 및 함수명
- **파일명**: snake_case (예: `system_setting.py`)
- **클래스명**: PascalCase (예: `SystemSettingService`)
- **함수명**: snake_case (예: `get_by_id`)
- **상수**: UPPER_SNAKE_CASE (예: `MAX_RETRY_COUNT`)

### 일관성 유지
- Repository 메서드: `create`, `get_by_id`, `get_list`, `update`, `delete`
- Service 메서드: Repository와 동일한 네이밍
- Router 함수: HTTP 메서드 의미와 일치 (`create`, `get_by_id`, `update`, `delete`)

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

