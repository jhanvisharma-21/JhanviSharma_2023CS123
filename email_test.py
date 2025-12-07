import smtplib

server = smtplib.SMTP("smtp.gmail.com", 587)
server.starttls()
server.login("jhanvisharma.0021@gmail.com", "jrqs fiii vbjl zvhe")
server.sendmail("jhanvisharma.0021@gmail.com", "jhanvisharma140@gmail.com", "Hello from CMD!")
server.quit()