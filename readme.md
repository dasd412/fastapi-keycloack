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