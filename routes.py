from app import app
from flask import render_template, request, redirect, flash, session, Response
import messages, users
from werkzeug.security import check_password_hash, generate_password_hash

#pages
@app.route("/")
def index():
    return render_template("index.html")

@app.route("/ready")
def ready():
    return render_template("ready.html")

@app.route("/upload")
def upload():
    count = messages.count()
    imageid = messages.get_imageid()
    return render_template("upload.html", count=count, imageid=imageid)

@app.route("/result")
def result():
    count = messages.count()
    results = messages.get_results()
    return render_template("result.html", count=count, results=results)

@app.route("/vote")
def vote():
    imageid = messages.get_imageid()
    return render_template("vote.html", imageid=imageid)

@app.route("/show_images")
def show_images():
    imageid = messages.get_imageid()
    count = len(imageid)   
    return render_template("show_images.html", count=count, imageid=imageid)

@app.route("/delete")
def delete():
    idname = messages.get_idname()
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
            return redirect("/")
        else:
            flash("Väärä tunnus tai salasana")
            return redirect("/")

@app.route("/logout")
def logout():
    del session["username"]
    return redirect("/")

@app.route("/register", methods=["get","post"])
def register():
    if request.method == "GET":
        return render_template("register.html")
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        if users.register(username,password):
            return redirect("/")
        else:
            flash("Rekisteröinti ei onnistunut")
            return redirect("/register")

@app.route("/sendvote", methods=["POST"])
def sendvote():
    imageid = request.form.getlist("id")
    data = request.form

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
                flash("Virhe; useammalle kuvalle annettu sama äänimäärä. Suorita uusi äänestys.")
                return redirect("/vote")
        else:
            print("ei ääniä")

    messages.commit()
    return redirect("/ready")

@app.route("/send", methods=["POST"])
def send():
    #check image   
    file = request.files["file"]
    name = file.filename
    if not name.endswith(".jpg"):
        flash("Väärä tiedostotyyppi")
        return redirect("/upload")
    data = file.read()
    if len(data) > 4000*1024:
        flash("Liian suuri tiedostokoko, max koko on 4MB")
        return redirect("/upload")

    #check photographer
    photographer = request.form["photographer"]
    if len(photographer) == 0:
        flash("Kuvaajan nimi puuttuu")
        return redirect("/upload")
    
    #send to the db
    if messages.send_image(name, data, photographer):
        return redirect("/upload")
    else:
        flash("Kuvien lataus epäonnistui")
        return redirect("/upload")

@app.route("/remove", methods=["POST"])
def remove_image():
    imageid = request.form["id"]
    if messages.delete_image(imageid):
        return redirect("/delete")
    else:
        flash("Kuvan poisto ei onnistunut")
        return redirect("/delete")


