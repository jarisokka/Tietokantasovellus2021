from db import db
from flask import make_response


#GET
def count():
    result = db.session.execute("SELECT COUNT(*) FROM images")
    count = result.fetchone()[0]
    return count

def count_voters():
    result = db.session.execute("SELECT COUNT(*) FROM voters")
    voters = result.fetchone()[0]
    return voters

def get_imageid():
    result = db.session.execute("SELECT id FROM images")
    imageid = result.fetchall()
    return imageid

def get_idname():
    result = db.session.execute("SELECT id, name FROM images")
    idname = result.fetchall()
    return idname

def get_imagename(id):
    sql = "SELECT name FROM images WHERE id=:id"
    result = db.session.execute(sql, {"id":id})
    name = result.fetchone()[0]
    return name

def get_results():
    result = db.session.execute("SELECT V.image_id, V.points, P.name FROM votes V, photographer P \
    WHERE V.image_id=P.image_id ORDER BY V.points DESC")
    results = result.fetchall()
    return results

def get_image(id):
    sql = "SELECT data FROM images WHERE id=:id"
    result = db.session.execute(sql, {"id":id})
    data = result.fetchone()[0]
    response = make_response(bytes(data))
    response.headers.set("Content-Type","image/jpeg")
    return response

def get_points(image_id):
    result = db.session.execute("SELECT points FROM votes WHERE image_id=:image_id", {"image_id":image_id})
    points = result.fetchone()[0]
    return points

def check_voter(user_id):
    result = db.session.execute("SELECT user_id FROM voters WHERE user_id=:user_id", {"user_id":user_id})
    if result.fetchone() == None:
        return 0
    else:
        return 2

#SEND
def send_image(name, data, photographer):
    #insert image
    sql = "INSERT INTO images (name,data) VALUES (:name,:data) RETURNING id"
    result = db.session.execute(sql, {"name":name,"data":data})
    image_id = result.fetchone()[0]

    #insert photographer
    sql = "INSERT INTO photographer (image_id, name) VALUES (:image_id,:name)"
    db.session.execute(sql, {"image_id":image_id, "name":photographer})
    
    #insert votes
    points = 0
    sql = "INSERT INTO votes (image_id, points) VALUES (:image_id, :points)"
    db.session.execute(sql, {"image_id":image_id, "points":points})
    
    #submit
    db.session.commit()
    return True

def update_votes(points, image_id):
    sql = "UPDATE votes SET points = :points WHERE image_id = :image_id"
    db.session.execute(sql, {"points":points, "image_id":image_id})

def commit():
    db.session.commit()

def delete_image(id):
    sql = "DELETE FROM images WHERE id=:id"
    db.session.execute(sql, {"id":id})
    db.session.commit()
    return True

def register_voter(user_id):
    sql = "INSERT INTO voters (user_id) VALUES (:user_id)"
    db.session.execute(sql, {"user_id":user_id})
    db.session.commit()
