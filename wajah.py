import cv2
import numpy as np 
import sqlite3
import os
import time
import smtplib 
from email.mime.multipart import MIMEMultipart 
from email.mime.text import MIMEText 
from email.mime.base import MIMEBase 
from email import encoders 

conn = sqlite3.connect('database.db')
c = conn.cursor()

fname = "recognizer/trainingData.yml"
if not os.path.isfile(fname):
  print("Please train the data first")
  exit(0)

face_cascade = cv2.CascadeClassifier('haarcascades/haarcascade_frontalface_default.xml')
cap = cv2.VideoCapture(0)
recognizer = cv2.face.LBPHFaceRecognizer_create()
recognizer.read(fname)
def recognize():
      while True:
        ret, img = cap.read()
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        faces = face_cascade.detectMultiScale(gray, 1.3, 5)
        for (x,y,w,h) in faces:
          cv2.rectangle(img,(x,y),(x+w,y+h),(0,255,0),3)
          ids,conf = recognizer.predict(gray[y:y+h,x:x+w])
          c.execute("select name from users where id = (?);", (ids,))
          result = c.fetchall()
          name = result[0][0]
          nama = result[0][0]
          print nama
          if conf < 50:
            cv2.putText(img, name, (x+2,y+h-5), cv2.FONT_HERSHEY_SIMPLEX, 1, (150,255,0),2)
            break
	#menambah foto
            #foto mengulang 1 kali
            #if name == name:
             #     mail()
          else:
            cv2.putText(img, 'tidak dikenali', (x+2,y+h-5), cv2.FONT_HERSHEY_SIMPLEX, 1, (0,0,255),2)
        cv2.imshow('Face Recognizer',img)
        k = cv2.waitKey(30) & 0xff
        if k == 27:
          break
          cap.release()
          time.sleep(5)
          continue
def mail():
      cv2.imwrite('opencv'+str(name)+'.jpg',img)
      cv2.destroyWindow('Face Recognizer') 
      fromaddr = "sgoku231@gmail.com"
      toaddr = "lamunesseliot@gmail.com"
#toaddr = "lamunesseliot@gmail.com"
   
# instance of MIMEMultipart 
      msg = MIMEMultipart() 
  
# storing the senders email address   
      msg['From'] = fromaddr 
  
# storing the receivers email address  
      msg['To'] = toaddr 
  
# storing the subject  
      msg['Subject'] = "Seseorang datang kerumah"
  
# string to store the body of the mail 
      body = "tes pesan otomatis alexa"
  
# attach the body with the msg instance 
      msg.attach(MIMEText(body, 'plain')) 
  
# open the file to be sent  
      filename = "opencv.jpg"
      attachment = open("opencv"+str(name)+".jpg", "rb") 
  
# instance of MIMEBase and named as p 
      p = MIMEBase('application', 'octet-stream') 
  
# To change the payload into encoded form 
      p.set_payload((attachment).read()) 
  
# encode into base64 
      encoders.encode_base64(p) 
      p.add_header('Content-Disposition', "attachment; filename= %s" % filename) 
  
# attach the instance 'p' to instance 'msg' 
      msg.attach(p) 
  
# creates SMTP session 
      s = smtplib.SMTP('smtp.gmail.com', 587) 
  
# start TLS for security 
      s.starttls() 
  
# Authentication 
      s.login(fromaddr, "ZGFpcw==") 
  
# Converts the Multipart msg into a string 
      text = msg.as_string() 
# sending the mail 
      s.sendmail(fromaddr, toaddr, text)  
      time.sleep(10)          
recognize()
#cv2.destroyAllWindows()