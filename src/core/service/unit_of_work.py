from sqlmodel import Session


class SyncUnitOfWork:
    """
    Base UnitOfWork - 트랜잭션 관리만 담당. 각 도메인에서 상속하여 리포지토리 추가
    서비스 레이어에서 단일 엔티티에 대한 트랜잭션이든, 여러 엔티티들에 대한 트랜잭션이던 상관 없이 이 클래스를 상속해서 사용하세요.
    """

    def __init__(self, session: Session):
        self.session = session

    def commit(self):
        self.session.commit()

    def rollback(self):
        self.session.rollback()

    def __enter__(self):
        return self

    def close(self):
        self.session.close()

    def __exit__(self, exc_type, exc_val, exc_tb):
        if exc_type is None:  # 예외 없음
            self.commit()  # 커밋
        else:  # 예외 발생
            self.rollback()  # 롤백
        self.session.close()
