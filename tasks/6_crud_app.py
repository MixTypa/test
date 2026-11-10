from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, EmailStr, Field
from itertools import count

app = FastAPI(title="Users CRUD")

_users: dict[int, "User"] = {}
_ids = count(1)

class UserIn(BaseModel):
    name: str = Field(..., min_length=1, max_length=100)
    email: EmailStr

class User(UserIn):
    id: int

@app.get("/users", response_model=list[User])
def list_users():
    return list(_users.values())

@app.post("/users", response_model=User, status_code=201)
def create_user(u: UserIn):
    uid = next(_ids)
    _users[uid] = User(id=uid, **u.model_dump())
    return _users[uid]

@app.get("/users/{uid}", response_model=User)
def get_user(uid: int):
    if uid not in _users:
        raise HTTPException(404, "user not found")
    return _users[uid]

@app.put("/users/{uid}", response_model=User)
def update_user(uid: int, u: UserIn):
    if uid not in _users:
        raise HTTPException(404, "user not found")
    _users[uid] = User(id=uid, **u.model_dump())
    return _users[uid]

@app.delete("/users/{uid}", status_code=204)
def delete_user(uid: int):
    if uid not in _users:
        raise HTTPException(404, "user not found")
    del _users[uid]

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
