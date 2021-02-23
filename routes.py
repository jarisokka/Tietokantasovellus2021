from app import app
from flask import render_template, request, redirect, flash, session, Response
import messages, users
from werkzeug.security import check_password_hash, generate_password_hash
import os

#pages
@app.route("/")
def index():
    return render_template("index.html")

@app.route("/ready")
def ready():
    return render_template("ready.html")

@app.route("/upload")
def upload():
    if session.get("user_id") != 1:
        return render_template("error.html", error="Ei oikeutta nähdä sivua.") 

    count = messages.count()
    imageid = messages.get_imageid()
    return render_template("upload.html", count=count, imageid=imageid)

@app.route("/result")
def result():
    if session.get("user_id") != 1:
        return render_template("error.html", error="Ei oikeutta nähdä sivua.") 

    count = messages.count()
    results = messages.get_results()
    voters = messages.count_voters()
    return render_template("result.html", count=count, results=results, voters=voters)

@app.route("/vote")
def vote():
    if session.get("user_id") == None:
        return render_template("error.html", error="Ei oikeutta nähdä sivua.")  

    user_id = session["user_id"]
    #admin can always see the voting page
    if user_id != 1:
        result = messages.check_voter(user_id)
    else:
        result = 1    
    imageid = messages.get_imageid()
    return render_template("vote.html", imageid=imageid, result=result, user_id=user_id)

@app.route("/show_images")
def show_images():
    imageid = messages.get_imageid()
    count = len(imageid)   
    return render_template("show_images.html", count=count, imageid=imageid)

@app.route("/delete")
def delete():
    if session.get("user_id") != 1:
        return render_template("error.html", error="Ei oikeutta nähdä sivua.") 

    idname = messages.get_idname()
    print(idname)
    return render_template("delete.html", idname=idname)

#actions
@app.route("/images/<int:id>")
def images(id):
    response = messages.get_image(id)
    return response

@app.route("/login", methods=["get","post"])
def login():
    if request.method == "GET":
        return render_template("login.html")
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        if users.login(username,password):
            session["username"] = username
            session["csrf_token"] = os.urandom(16).hex()                  
            return redirect("/")
        else:
            flash("Väärä tunnus tai salasana.", "error")
            return redirect("/")

@app.route("/logout")
def logout():
    users.logout()
    return redirect("/")

@app.route("/register", methods=["get","post"])
def register():
    if request.method == "GET":
        return render_template("register.html")
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        if users.register(username,password):
            flash("Rekisteröityminen onnistui, Voit seuraavaksi kirjautua sisään.", "ok")
            return redirect("/")
        else:
            flash("Rekisteröinti ei onnistunut.", "error")
            return redirect("/register")

@app.route("/sendvote", methods=["POST"])
def sendvote():
    #security check
    if session["csrf_token"] != request.form["csrf_token"]:
        abort(403)
    #handle voting    
    imageid = request.form.getlist("id")
    data = request.form
    images = len(imageid)

    check = {1:0, 2:0, 3:0, 4:0, 5:0}   #this is used to check there are no double votes

    for id in imageid:                  #updating and verifying the votes
        if id in data:
            image_id = int(id)
            new = data[id]
            old = messages.get_points(image_id)       
            if check[int(new)] == 0:    #check if there are double amount of same votes
                check[int(new)] = 1
                points = int(old) + int(new)
                messages.update_votes(points, image_id)
            else:
                flash("Virhe; useammalle kuvalle annettu sama äänimäärä. Suorita uusi äänestys.", "error")
                return redirect("/vote")
        else:
            images -= 1

    #check that some votes are given
    if images != 0:
        messages.commit() #register votes
        user_id = session["user_id"]
        messages.register_voter(user_id) #register voter
    else:    
        flash("Virhe; yhtään ääntä ei annettu.", "error")
        return redirect("/vote")

    return redirect("/ready")

@app.route("/send", methods=["POST"])
def send():
    #security check
    print(session["csrf_token"])
    print(request.form["csrf_token"])
    if session["csrf_token"] != request.form["csrf_token"]:
        abort(403)
    #check image   
    file = request.files["file"]
    name = file.filename
    if not name.endswith(".jpg"):
        flash("Väärä tiedostotyyppi", "error")
        return redirect("/upload")
    data = file.read()
    if len(data) > 500*1024:
        flash("Liian suuri tiedostokoko, max koko on 500kt.", "error")
        return redirect("/upload")

    #check photographer
    photographer = request.form["photographer"]
    if len(photographer) == 0:
        flash("Kuvaajan nimi puuttuu.", "error")
        return redirect("/upload")
    
    #send to the db
    if messages.send_image(name, data, photographer):
        return redirect("/upload")
    else:
        flash("Kuvien lataus epäonnistui.", "error")
        return redirect("/upload")

@app.route("/remove", methods=["POST"])
def remove_image():
    #security check
    if session["csrf_token"] != request.form["csrf_token"]:
        abort(403)
    #handle deleting
    imageid = request.form["id"]
    name = messages.get_imagename(imageid)

    if messages.delete_image(imageid):
        flash("Kuva " + name + " poistettiin onnistuneesti.", "ok")
        return redirect("/delete")
    else:
        flash("Kuvan poisto ei onnistunut.", "error")
        return redirect("/delete")

@app.route("/emptyvotes", methods=["POST"])
def empty():
    #security check
    if session["csrf_token"] != request.form["csrf_token"]:
        abort(403)
    #handle removing votes
    if messages.empty():
        flash("Äänestystulokset nollattu", "ok")
        return redirect("/delete")
    else:
        flash("Tyhjennys ei onnistunut", "error")
        return redirect("/delete")
