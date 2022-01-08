# How to run the project
export FLASK_APP="application.py"
export DATABASE_URL="postgresql://aswhnyzjhwhoyc:7f7cd26cb3bbeb10b78f7017bcc3e07aaf15dee9752607183c4a50b79fe97f16@ec2-54-165-36-134.compute-1.amazonaws.com:5432/d4fqbm2gc713m3"
export EMAIL_USER="enter your gmail account here"
export EMAIL_PASSWORD="enter your gmail password here"
export MAIL_RECIPIENT="enter alert receiving email here"
export UPLOAD_DIR="fileuploads"
pip install -r requirements.txt
flask run 


# Login credentials
email: yipzhenyu@gmail.com
password: password


**Please do open my project in icognito/private mode to prevent any disruptions


# Final Project
For my final project, I want to go back to the reason why i wanted to take this course, which was in hope of finding a job as a software developer. I thought of it for a long time and felt that I should create a portfolio webpage for myself to show to my future employers during interviews if necessary. Thus, my final project would be a portfolio webpage with statistic analysis.

Firstly upon logging in, I will be brought to the admin page(admin.html), I will be greeted with a dashboard that consists of bar graphs, line charts and a statistics summary of my portfolio page. The summary tells me about how many people have visited my website, downloaded my resume, requested to have a live chat with me and even a feedback count tracker for the current day.
The layout used for the admin pages is "layout3.html"

The admin will have access to three other pages namely admin feedback page(adminfeedbacks.html), admin live chat page(channelindex.html) and their own personal portfolio webpage(index.html).

For me, in my portfolio page, I gave a brief introduction of myself, my programming knowledge, my experiences, my education certificates and lastly, my past projects.
The layout that was used for the portfolio is "layout.html"
Users can view my past projects by clicking on the images, which connects to (hnfapp.html, harvardxpage.html) and my past university final year project dairy.
If my viewers would like to contact me, they can click on my phone number or email me by clicking on my email at the footer of the page. They can also connect with me at my social accounts whcih are at the top, with each icon describing what social account it links to.

At the bottom right, there is a floating icon that provides 3 other features. They can download my latest resume in pdf format, have a live chat with me or even provide me a feedback on my portfolio. 
When they click on live chat, they will be automatically be redirected to a fresh new channel that is automatically created for each viewer and the admin will receive an email alert that a new channel was created and reminds the admin to respond as soon as possible. Even if the viewer leaves the browser, the viewer can still continue the conversation on any other day as all the messages are saved and by clicking on the live chat button again, they will be redirected back to the previous live chat channel.
If they would like to just leave a feedback for my portfolio, that is also possible by clicking on the feedback icon. They can request to be responded by clicking on the yes radio button.


Final Project video: https://youtu.be/6xS5FakNssk



