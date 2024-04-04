from sqlalchemy.orm import Session

import models


def get_robots(db: Session):
    return db.query(models.Robot).all()
