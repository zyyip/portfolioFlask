import os
import json
import datetime
import requests

from collections import deque
from flask import Flask, session, request, render_template, redirect, url_for, jsonify, send_from_directory
from flask_session import Session
from flask_socketio import SocketIO, emit, join_room
from flask_mail import Mail, Message

from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker


from werkzeug.utils import secure_filename

from models import *


app = Flask(__name__)
app.config["SECRET_KEY"] = "b'\x0f\x1c\x16\xc9q\xfe\x96\xe22\x12\x91x\xc4Z]\xfe\xec\x87\x08z\xbdH\xcf\x1a'"
app.config["UPLOAD_DIR"] = os.getenv("UPLOAD_DIR")
app.config["SQLALCHEMY_DATABASE_URI"] = os.getenv("DATABASE_URL")
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
db.init_app(app)

# Check for environment variable
if not os.getenv("DATABASE_URL"):
    raise RuntimeError("DATABASE_URL is not set")

# Configure session to use filesystem
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = 'filesystem'
Session(app)

# Set up database
engine = create_engine(os.getenv("DATABASE_URL"))
db = scoped_session(sessionmaker(bind=engine))

#setup email
mail_settings = {
    "MAIL_SERVER": 'smtp.gmail.com',
    "MAIL_PORT": 465,
    "MAIL_USE_TLS": False,
    "MAIL_USE_SSL": True,
    "MAIL_USERNAME": os.environ['EMAIL_USER'],
    "MAIL_PASSWORD": os.environ['EMAIL_PASSWORD'],
    "MAIL_RECIPIENT": os.environ['MAIL_RECIPIENT']
}
app.config.update(mail_settings)
mail = Mail(app)

#setup socket
socketio = SocketIO(app)
openChannels = []
channelsMessages = dict()



@app.route("/")
def index():
    return render_template("login.html")


@app.route("/home/<int:userid>")
def bookreview(userid):
    if 'oldvisitor' in session:
        return render_template("index.html", useridx=userid)
    else:
        session['oldvisitor'] = 1
        db.execute("INSERT INTO views(userid) VALUES (%i)"%(userid))
        db.commit()
        return render_template("index.html", useridx=userid)

@app.route("/hnfpage/<int:userid>")
def hnfpage(userid):
    if 'oldvisitor' in session:
        return render_template("hnfapp.html", useridx=userid)
    else:
        session['oldvisitor'] = 1
        db.execute("INSERT INTO views(userid) VALUES (%i)"%(userid))
        db.commit()
        return render_template("hnfapp.html", useridx=userid)


@app.route("/harvardxpage/<int:userid>")
def harvardxpage(userid):
    if 'oldvisitor' in session:
        return render_template("harvardxpage.html", useridx=userid)
    else:
        session['oldvisitor'] = 1
        db.execute("INSERT INTO views(userid) VALUES (%i)"%(userid))
        db.commit()
        return render_template("harvardxpage.html", useridx=userid)


@app.route("/feedback/<int:userid>")
def feedbackpage(userid):
    if 'oldvisitor' in session:
        return render_template("feedback.html", useridx=userid)
    else:
        session['oldvisitor'] = 1
        db.execute("INSERT INTO views(userid) VALUES (%i)"%(userid))
        db.commit()
        return render_template("feedback.html", useridx=userid)



@app.route("/add_resume_count", methods=["POST"])
def add_resume_count():
    
    if request.method == "POST":
        queries= request.json['queries']

        # userIDx = int(userID['userID'])
        # db.execute("INSERT INTO resumecount(userid) VALUES (%i)"%(userIDx))
        db.execute(queries)
        db.commit()
    return json.dumps({'success':True}), 200, {'ContentType':'application/json'} 
 
 

@app.route("/submitfeedback", methods=["POST"])
def submitfeedback():
    contact_name = request.form.get("name")
    phone_number = request.form.get("phone_number")
    email = request.form.get("email")
    descriptions = request.form.get("description")
    response = request.form.get("checkbox")
    userid = request.form.get("userid")

    db.execute("INSERT INTO feedbackCount(userid, contact_name, phone_number, email, descriptions, response) VALUES ('%s', '%s', '%s', '%s', '%s', '%s')"%(userid, contact_name, phone_number, email, descriptions, response))
    db.commit()
    return render_template("feedback.html", useridx=userid, message="Feedback submitted successfully!")



#Second part
@app.route("/admindashboard")
def admindashboard():
    if "userid" in session:
        today = datetime.date.today().strftime("%B %d, %Y")
        userid = str(session["userid"])

        userinfo = db.execute("SELECT * from users WHERE userid="+userid).first()

        todayView = db.execute("SELECT COUNT(*) from views WHERE viewdate > CURRENT_DATE AND userid ="+userid).first()[0]
        todayResume = db.execute("SELECT COUNT(*) from resumecount WHERE downloaddate > CURRENT_DATE AND userid ="+userid).first()[0]
        todayFeedback = db.execute("SELECT COUNT(*) from feedbackcount WHERE feedbackdate > CURRENT_DATE AND userid ="+userid).first()[0]
        todayChannel = db.execute("SELECT COUNT(*) from channel WHERE datecreated > CURRENT_DATE AND userid ="+userid).first()[0]
        todayTotal = int(todayView) + int(todayResume) + int(todayFeedback) + int(todayChannel)
        totalView = db.execute("SELECT COUNT(*) from views WHERE userid="+userid).first()[0]
        totalResume = db.execute("SELECT COUNT(*) from resumecount WHERE userid="+userid).first()[0]
        totalFeedback = db.execute("SELECT COUNT(*) from feedbackcount WHERE userid="+userid).first()[0]
        totalFeedback = db.execute("SELECT COUNT(*) from feedbackcount WHERE userid="+userid).first()[0]
        totalChannel = db.execute("SELECT COUNT(*) from channel WHERE userid="+userid).first()[0]

        lineChartLabels = db.execute("SELECT to_char(viewdate,'DD') AS day FROM views WHERE extract(year from viewdate) = extract(year from current_timestamp) AND extract(month from viewdate) = extract(month from current_timestamp) AND userid ="+userid+" GROUP BY to_char(viewdate,'DD')").fetchall()
        lineChartData = db.execute("SELECT COUNT(*) FROM views WHERE extract(year from viewdate) = extract(year from current_timestamp) AND extract(month from viewdate) = extract(month from current_timestamp) AND userid ="+userid+" GROUP BY extract(day from viewdate)").fetchall()
        
        # barChartLabels = db.execute("SELECT TO_CHAR(viewdate, 'Month') AS month FROM views WHERE extract(year from viewdate) = extract(year from current_timestamp) AND userid ="+userid+" GROUP BY TO_CHAR(viewdate, 'Month'), extract(month from viewdate) ORDER BY extract(month from viewdate) ASC").fetchall()
        barChartData = db.execute("SELECT COUNT(views.viewdate) FROM (select 1 as mon union all select 2 union all select 3 union all select 4 union all select 5 union all select 6 union all select 7 union all select 8 union all select 9 union all select 10 union all select 11 union all select 12) m left outer join views on m.mon = extract(month from views.viewdate) and extract(year from views.viewdate) = extract(year from current_timestamp) AND userid ="+userid+" GROUP BY m.mon ORDER BY m.mon ASC;").fetchall()

        resumeChartLabels =   db.execute("SELECT to_char(downloaddate,'DD') AS day FROM resumecount WHERE extract(year from downloaddate) = extract(year from current_timestamp) AND extract(month from downloaddate) = extract(month from current_timestamp) AND userid ="+userid+" GROUP BY to_char(downloaddate,'DD')").fetchall()
        resumeChartData = db.execute("SELECT COUNT(*) FROM resumecount WHERE extract(year from downloaddate) = extract(year from current_timestamp) AND extract(month from downloaddate) = extract(month from current_timestamp) AND userid ="+userid+" GROUP BY extract(day from downloaddate)").fetchall()

        lineChartLabels = list(lineChartLabels)
        lineChartData = list(lineChartData)
        # barChartLabels = list(barChartLabels)
        barChartData = list(barChartData)
        resumeChartLabels = list(resumeChartLabels)
        resumeChartData = list(resumeChartData)


        # print(resumeChartData)
        # print(lineChartLabels)
        # print(lineChartData)    
        # print(barChartLabels)
        # print(barChartData)

        # for x in lineChartData[0]:
        #     print(x)

        return render_template("admin.html", userinfo=userinfo, todayDate = today, 
        todayViews = todayView, todayResumes = todayResume, todayFeedbacks = todayFeedback, todayChannels = todayChannel, todayTotals = todayTotal,
        totalViews = totalView, totalResumes = totalResume, totalFeedbacks = totalFeedback, totalChannels = totalChannel,
        lineChartLabels = lineChartLabels, lineChartData = lineChartData,
        # barChartLabels = barChartLabels,
        barChartData = barChartData,
        resumeChartLabels = resumeChartLabels, resumeChartData = resumeChartData)
    else:
        return redirect(url_for("index"))


# @app.route("/getlinechart")
# def getlinechart():
#     if "userid" in session:
#         lineChartLabels = db.execute("SELECT extract(day from viewdate) as day FROM views WHERE extract(year from viewdate) = extract(year from current_timestamp) AND extract(month from viewdate) = extract(month from current_timestamp) GROUP BY extract(day from viewdate)").fetchall()
#         lineChartData = db.execute("SELECT COUNT(*) FROM views WHERE extract(year from viewdate) = extract(year from current_timestamp) AND extract(month from viewdate) = extract(month from current_timestamp) GROUP BY extract(day from viewdate)").fetchall()
        
#         barChartLabels = db.execute("SELECT TO_CHAR(viewdate, 'Month') AS month FROM views WHERE extract(year from viewdate) = extract(year from current_timestamp) GROUP BY TO_CHAR(viewdate, 'Month')").fetchall()
#         barChartData = db.execute("SELECT COUNT(*) FROM views WHERE extract(year from viewdate) = extract(year from current_timestamp) GROUP BY TO_CHAR(viewdate, 'Month')").fetchall()

#         lineChartLabels = list(lineChartLabels)
#         lineChartData = list(lineChartData)

#         return jsonify({'lineChartLabels': [dict(row) for row in lineChartLabels], 'lineChartData': [dict(row) for row in lineChartData]})


@app.route("/adminfeedbacks")
def adminfeedback():
    if "userid" in session:
        userid = str(session["userid"])
        userinfox = db.execute("SELECT * from users WHERE userid="+userid).first()
        feedbackAll = db.execute("SELECT * FROM feedbackcount where userid="+userid).fetchall()
        return render_template("adminfeedbacks.html", userinfo = userinfox, feedbackalls = feedbackAll)
    else:
        return redirect(url_for("index"))


@app.route("/logout")
def logout():
    session.pop("userid", None)
    return redirect(url_for("index"))



@app.route("/loginpage")
def loginpage():
    return render_template("login.html")


@app.route("/login", methods=["POST"])
def login():
    emails = request.form.get("email")
    pwd = request.form.get("password")

    userinfo = db.execute("""SELECT * from users WHERE email='%s' AND pwd='%s'"""%(emails,pwd)).first()

    if userinfo is None:
        return render_template("login.html", message="Incorrect login or password!")

    session["userid"] = userinfo[0]

    return redirect(url_for("admindashboard"))


@app.route("/register")
def registrationpage():
    return render_template("registration.html")


@app.route("/registration", methods=["POST"])
def registration():
    fname = request.form.get("first_name")
    lname = request.form.get("last_name")
    email = request.form.get("email")
    password = request.form.get("password")

    db.execute("INSERT INTO users(fname, lname, email, pwd) VALUES ('%s', '%s', '%s', '%s')"%(fname, lname, email, password))
    db.commit()
    return render_template("login.html", message="Successfully registered! Please login!")
 

#channel part
@app.route("/channelindex/<int:userid>")
def channelindex(userid):
    return render_template("channelindex.html", channels=openChannels, useridx=userid)


@app.route("/adminchannel/<int:userid>")
def adminchannel(userid):
    admincheck = "yes"
    return render_template("channelindex.html", channels=openChannels, useridx=userid, admincheck=admincheck)



@app.route("/createchannel/<int:userid>", methods=['GET', 'POST'])
def createchannel(userid):
    """ Create a channel and redirect to its page """

    # Get channel name from form
    channel = db.execute("SELECT MAX(channelid) FROM channel").first()
   
    if channel[0] is None:
        newChannel = 1
        db.execute("INSERT INTO channel(userid) VALUES ("+str(userid)+")")
        db.commit()
    else:
        newChannel = int(channel[0])+1
        db.execute("INSERT INTO channel(userid) VALUES ("+str(userid)+")")
        db.commit()

    if request.method == "POST":
        return render_template("channelindex.html", channels=openChannels)

    else:
        if newChannel in openChannels:
            return render_template("error.html", message="that channel already exists!")

        # Add channel to global list of channels
        openChannels.append(newChannel)

        # Add channel to global dict of channels with messages
        # Every channel is a deque to use popleft() method
        # https://stackoverflow.com/questions/1024847/add-new-keys-to-a-dictionary
        channelsMessages[newChannel] = deque()
        # return render_template("channel.html", channels=openChannels, messages=channelsMessages[newChannel], channel=newChannel)
        # print(openChannels[0])

        with app.app_context():
            msg = Message(subject="Alert! New channel created!",
            sender=app.config.get("MAIL_USERNAME"),
            recipients=[app.config.get("MAIL_RECIPIENT")], # replace with your email for testing
            body="Alert! A new channel has been created. Do reply to the message asap!")
            mail.send(msg)


        return render_template("channelindex.html", addedChannel=newChannel)
        




@socketio.on('newMessage')
def send_msg(msg, timestamp, username, current_channels):
    """ Receive message with timestamp and broadcast on the channel """

    # Broadcast only to users on the same channel.
    # room = session.get('current_channel')

    # Save 100 messages and pass them when a user joins a specific channel.

    if len(channelsMessages[int(current_channels)]) > 100:
        # Pop the oldest message
        channelsMessages[int(current_channels)].popleft()

    channelsMessages[int(current_channels)].append(
        [timestamp, username, msg])

    emit('announce message', {
        'user': username,
        'timestamp': timestamp,
        'msg': msg},
        room=current_channels)


@app.route("/channel/<channel>", methods=['GET', 'POST'])
def enter_channels(channel):
    """ Show channel page to send and receive messages """

    if "userid" in session:
            current_channel = channel
            admincheck = "yes"
            return render_template("channel.html", channels=openChannels, messages=channelsMessages[int(current_channel)], channel=int(current_channel), admincheck = admincheck)
    else:
        return redirect("/channelindex")


@app.route("/channel", methods=['GET', 'POST'])
def enter_channel():
    """ Show channel page to send and receive messages """

    if request.method == "POST":
        current_channel = request.form.get("current_channel")
        # print("Hello" + str(current_channel))
        return render_template("channel.html", channels=openChannels, messages=channelsMessages[int(current_channel)], channel=int(current_channel))
    else:
        return redirect("/channelindex")
        


@socketio.on("joined", namespace='/')
def joined(channel, username):

    # Save current channel to join room.

    join_room(channel)

    # emit('status', {
    #     'userJoined': username,
    #     'channel': room,
    #     'msg': session.get('username') + ' has entered the channel'},
    #     room=room)




@app.route("/receive-file/", methods=["POST"])
def receive_file():
    channel_name = request.form.get("channel_name")
    file = request.files["file"]
    if file.filename == "":
        return jsonify({"message": "empty file name"}), 204

    filename = secure_filename(file.filename)
    new_filename = os.path.join(app.config['UPLOAD_DIR'], filename)
    if os.path.isfile(new_filename):
        # File already exists
        pass

    file.save(new_filename)
    link = "/download/" + filename
    return jsonify({"message": "file saved",
                    "filename": filename,
                    "link": link}), 201


@app.route("/download/<filename>")
def download(filename):
    if not os.path.isfile(os.path.join(app.config['UPLOAD_DIR'], filename)):
        return jsonify({"message": "file not found"}), 404

    return send_from_directory(app.config["UPLOAD_DIR"],filename,as_attachment=True)


@socketio.on("file sent")
def file_sent(data):
    channel_name = data["channel_name"]
    username = data["username"]
    filename = data["filename"]
    link = data["link"]
    curr_time = data["curr_time"]
    channel_name = int(channel_name)
    # print(username)

    channelsMessages[channel_name].append(
        [curr_time, username, link, filename])

    if len(channelsMessages[channel_name]) > 100:
        # Pop the oldest message
        channelsMessages[channel_name].popleft()

    channel_name=str(channel_name)    
    emit("announce file",
         {"channel_name": channel_name, "username": username, "timestamp": curr_time, "link": link, "filename": filename}, room=channel_name)

