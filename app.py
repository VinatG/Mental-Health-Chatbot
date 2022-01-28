from flask import Flask,request, redirect, session,g
from flask.templating import render_template
from gensim.parsing.preprocessing import strip_non_alphanum, preprocess_string
from bot_new import quering
from flask_mail import Mail, Message
from flask_sqlalchemy import SQLAlchemy
app = Flask(__name__)

mail = Mail(app) # instantiate the mail class
   
# configuration of mail
app.config['MAIL_SERVER']='smtp.gmail.com'
app.config['MAIL_PORT'] = 465
app.config['MAIL_USERNAME'] = 'btpproj@gmail.com'
app.config['MAIL_PASSWORD'] = 'btpproj#20'
app.config['MAIL_USE_TLS'] = False
app.config['MAIL_USE_SSL'] = True
mail = Mail(app)

app.secret_key = "Chatbotasdfghjk"
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///userdetails.db" #initialize the database
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# create database structure
class UserDetails(db.Model):
    sno = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200), nullable = False)
    emailId = db.Column(db.String(200), nullable = False)
    password = db.Column(db.String(200), nullable = False)
    severity = db.Column(db.Float, nullable = False)

# the template based questions
tempques = [("Are you facing any of these challenges","Anger","Anxiety","Stress","Depression"),
            ("Which of these areas of life do you want to improve?","Health","Work_life balance","Relationships","Social Life"),
            ("Have you received any therapy in the past","Yes","No","",""),
            ("Have you thought of self harm","Yes","NO","",""),
            ("What is your relationship status","Single","Dating","Married","Other"),
            ("Do you consider yourself a religious or spiritual person","Yes, religious","Yes, spiritual","Yes, religious and spiritual","No"),
            ("Are you currently taking any medication","Yes","No","","")]

# saving user session cookies
@app.before_request
def before_request():
    if 'emailId' in session:
        user = UserDetails.query.filter_by(emailId=session['emailId']).first()
        g.user = user

# show the starter page
@app.route("/")
def hello_world():
    return render_template("starter.html")

# show the signup page
@app.route("/signup", methods=['GET','POST'])
def signUp():
    message = ""
    if request.method=='POST':
        uname = request.form['uname']
        emailId = request.form['email']
        password = request.form['password']
        severity = 0
        user = UserDetails.query.filter_by(emailId=emailId).first() # if this returns a user, then the email already exists in database

        if user: # if a user is found, we want to redirect back to signup page so user can try again
            message = "The Email address already exists"
        else:
            userdet = UserDetails(name = uname, emailId = emailId, password = password,severity=severity)
            db.session.add(userdet)
            session['emailId'] = emailId
            db.session.commit()
            return redirect("/tempq/0")

    return render_template("signup.html", message = message)

# show the signinpage
@app.route("/signin", methods=['GET','POST'])
def signIn():
    message = ""
    if request.method=='POST':
        emailId = request.form['signinemail']
        password = request.form['signinpassword']
        user = UserDetails.query.filter_by(emailId=emailId).first()

        if user and password == user.password:
            session['emailId'] = user.emailId
            return redirect("/resp")
        else:
            message = "Please check your email address or password"
    return render_template("signin.html", message=message)

# The set template based questions are asked
@app.route("/tempq/<int:ct>", methods=['GET','POST'])
def tempq(ct):
    if ct == len(tempques):
        return redirect("/resp")
    return render_template("templateques.html", temp = tempques[ct], count = ct+1)

#The greetings page is presented
@app.route("/resp", methods=['GET','POST'])
def resp():
    # if request.method=='POST':
    name = g.user.name
    print("name:",name)
    try:
        preprocessed = [word for word in preprocess_string(name) if word not in (
                        'people', 'call', 'friend')][0]
        name = [word for word in strip_non_alphanum(name.lower()).split(
                ) if preprocessed in word][0]
    except:
        name = name.split()[0]
    name = name[0].upper() + name[1:]
    print("Hi " + name + "! My name's Rebecca. Let's start with our session.")
    question = "How are you doing?"

    return render_template("greetings.html", name = name, question= question, check = "truq")

# The interactive questions chat section 
@app.route("/mainchat/<string:check>/<string:question>", methods=['GET','POST'])
def mainchat(check,question):
    if request.method=='POST' and check == "truq":
        response = request.form['query']
        if check == "truq":
            nextquestion,score = quering(question+'?',response)
    elif check == "falq":
        nextquestion,score = quering(question,"bad")
    
    g.user.severity = (score + g.user.severity)/2   #compute cumulative severity score
    if nextquestion == None:
        if g.user.severity < 0.2: #if the cumulative score is less than 0.2 this means severe condition 
            return redirect("/bookappointment") # the user is given option between book appointment and relevant articles
        else:
            return redirect("/notify") #else the user is recommended relevant articles 
    
    if nextquestion[-1] == "?":
        check = "truq"
    else:
        check = "falq"
    
    return render_template("compchat.html", question = nextquestion, check = check)

# The option to choose appointment or relevant articles
@app.route("/bookappointment")
def bookapp():
    return render_template("bookappointment.html")

# Mailing the book appointment status 
@app.route("/bookfinal")
def bookfinal():
    msg = Message(
                'Appointment Status',
                sender ='btpproj@gmail.com',
                recipients = [g.user.emailId]
               )
    msg.body = """The Appointment with the associate is scheduled at 3pm tomorrow 
                The associate will connect with you on this link: .....
                The contact number of associate is : 0000000000"""
    mail.send(msg)
    return render_template("bookfinal.html")

# Mailing the relevant articles 
@app.route("/notify")
def notify():
    msg = Message(
                'Recommended Articles',
                sender ='btpproj@gmail.com',
                recipients = [g.user.emailId]
               )
    msg.body = """Here are some of the articles that we have chosen for you. 
                https://www.trendingus.com/positive-thinking/ , https://www.successconsciousness.com/blog/positive-attitude/positive-thinking-articles/ , 
                https://www.mayoclinic.org/healthy-lifestyle/stress-management/in-depth/positive-thinking/art-20043950 ,
                Do give them a read. Don't hesitate to reach out to us. We are in this together.
                Thanks and Regards,
                Team Healthiva """
    mail.send(msg)
    return render_template("finalpage.html")

if __name__ == "__main__":  
    app.run(debug=True)