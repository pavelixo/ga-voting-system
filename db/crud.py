from sqlalchemy.orm import Session
from db.models import Candidate


def create_candidate(db: Session, user_id: int, username: str, avatar_url: str):
  if get_candidate_by_id(db=db, user_id=user_id):
    raise ValueError(f'Candidate with user_id {user_id} already exists.')
  
  candidate = Candidate(user_id=user_id, username=username, avatar_url=avatar_url)
  db.add(candidate)
  db.commit()
  db.refresh(candidate)
  return candidate

def remove_candidate(db: Session, user_id: int):
  candidate = get_candidate_by_id(db=db, user_id=user_id)

  if candidate:
    db.delete(candidate)
    db.commit()
    return candidate
  else:
    raise ValueError("Candidate not found")

def add_vote(db: Session, user_id: int):
  candidate = get_candidate_by_id(db=db, user_id=user_id)

  if candidate:
    candidate.votes += 1
    db.commit()
    db.refresh(candidate)
    return candidate
  else:
    raise ValueError("Candidate not found")

def remove_vote(db: Session, user_id: int):
  candidate = get_candidate_by_id(db=db, user_id=user_id)

  if candidate:
    candidate.vote -= 1
    db.commit()
    db.refresh(candidate)
    return candidate
  else:
    raise ValueError("Candidate not found")

def get_candidate_by_id(db: Session, user_id: int):
  return db.query(Candidate).filter(Candidate.user_id == user_id).first()

def get_all_candidates(db: Session):
  return db.query(Candidate).all()