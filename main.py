from fastapi import FastAPI,HTTPException,status
from pydantic import BaseModel,Field

app = FastAPI()
courses = [
    {"id": 1, "code": "PY101", "name": "Python Basic", "duration": 30, "fee": 3000000},
    {"id": 2, "code": "API101", "name": "FastAPI Basic", "duration": 24, "fee": 2500000},
    {"id": 3, "code": "JV101", "name": "Java Basic", "duration": 40, "fee": 4000000}
]

class BaseCourse(BaseModel):
    
    code:str = Field(...,min_length=5)
    name:str = Field(...,min_length=5)
    duration:int = Field(...,gt=0)
    fee:int = Field(...,gt=0)
class UpdateCourse(BaseCourse):
    pass
@app.get("/courses",status_code=status.HTTP_200_OK,tags=["Courses"])
def get_course():
    return{
        "status":"Success",
        "message":"Lay thanh cong",
        "courses":courses
    }
@app.get("/courses/{course_id}",status_code=status.HTTP_200_OK,tags=["Courses"])
def get_courses(course_id:int):
    for course in courses:
        if course["id"] == course_id:
                return{
            "status":"Founded",
            "message":"Tim thay roi",
            "course":course
        }
    
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail="Course not found."
    )
@app.get("/courses",status_code=status.HTTP_200_OK,tags=["Courses"])
def get_course(keyword:str,min_fee:int,max_fee:int):
        result = list(filter(lambda course:keyword in course["name"] and min_fee <= course["fee"] <= max_fee,courses))
        return{
            "status":"Success",
            "message":"Tim duowc roi",
            "courses":result
        }
                 
@app.post("/courses",status_code=status.HTTP_201_CREATED,tags=["Courses"])
def post_course(course:BaseCourse):
    new_course ={
        "id":len(courses)+1,
        "code":course.code,
        "name":course.name,
        "duration":course.duration,
        "fee":course.fee
    }
    courses.append(new_course)
    return{
        "status":"Success",
        "message":"Tao thanh cong khoa hoc",
        "course":new_course
    }

@app.put("/courses/{course_id}",status_code=status.HTTP_200_OK,tags=["Courses"])
def update_course(course_upd:UpdateCourse,course_id:int):
    for course in courses:
        if course["id"] == course_id:
            course["code"] = course_upd.code
            course["name"] = course_upd.name
            course["duration"] = course_upd.duration
            course["fee"] = course_upd.fee
            return{
                "status":"Done",
                "message":"Update Done"
            }
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail="Course not found."
    )
@app.delete("/courses/{course_id}",status_code=status.HTTP_200_OK,tags=["Courses"])
def delete_course(course_id:int):
    for index,course in enumerate(courses):
        if course["id"] == course_id:
            courses.pop(index)
            return{
                "status":"Done",
                "message":"Xoa thanh cong"
            }
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail="Xoa thanh cong"
    )

    