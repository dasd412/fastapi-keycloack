import logging

from sqlmodel import Session

logger = logging.getLogger(__name__)


class UnitOfWork:
    """
    Base UnitOfWork - 트랜잭션 관리만 담당. 각 도메인에서 상속하여 리포지토리 추가
    서비스 레이어에서 단일 엔티티에 대한 트랜잭션이든, 여러 엔티티들에 대한 트랜잭션이던 상관 없이 이 클래스를 상속해서 사용하세요.
    """

    def __init__(self, session: Session):
        print("DEBUG: Initializing UnitOfWork")
        logger.info("Initializing UnitOfWork")
        self.session = session
        self._committed = False

    def commit(self):
        print("DEBUG: UnitOfWork - Calling session.commit()")
        logger.info("UnitOfWork: Calling session.commit()")
        self.session.commit()
        self._committed = True
        print("DEBUG: UnitOfWork - session.commit() completed")
        logger.info("UnitOfWork: session.commit() completed")

    def rollback(self):
        print("DEBUG: UnitOfWork - Calling session.rollback()")
        logger.info("UnitOfWork: Calling session.rollback()")
        self.session.rollback()
        print("DEBUG: UnitOfWork - session.rollback() completed")
        logger.info("UnitOfWork: session.rollback() completed")

    def __enter__(self):
        print("DEBUG: UnitOfWork - Entering context")
        logger.info("UnitOfWork: Entering context")

        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        print(f"DEBUG: UnitOfWork - Exiting context, exc_type={exc_type}")
        logger.info(f"UnitOfWork: Exiting context, exc_type={exc_type}")
        if exc_type is None:  # 예외 없음
            self.commit()  # 커밋
        else:  # 예외 발생
            self.rollback()  # 롤백
        print(f"DEBUG: UnitOfWork - Exited, committed={self._committed}")
        logger.info(f"UnitOfWork: Exited, committed={self._committed}")
