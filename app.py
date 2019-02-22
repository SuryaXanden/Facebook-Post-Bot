from selenium import webdriver
from time import sleep
from flask import Flask, render_template, request
from werkzeug import secure_filename
from selenium.webdriver.chrome.options import Options
import os

def Facebook(usr,pwd,path,desc,speed):
    if usr:
        chrome_options = Options()  
        chrome_options.add_argument("--headless")

        driver = webdriver.Chrome(executable_path = './chromedriver.exe', chrome_options = chrome_options)
        

        #<--- code to login --->
        driver.get('https://en-gb.facebook.com/login')
        usr_box = driver.find_element_by_id('email')
        usr_box.send_keys(usr)
        pwd_box = driver.find_element_by_id('pass')
        pwd_box.send_keys(pwd)
        login_button = driver.find_element_by_id('loginbutton')
        login_button.submit()
        #<--- / code to login --->
        #Wait until login
        sleep(speed)

        #<--- code to remove opaque screen --->
        remover = driver.find_element_by_tag_name('body').click()
        #<--- / code to remove opaque screen --->
        #WALL
        give = driver.find_element_by_xpath("//*[@name='xhpc_message']")
        #Wait for wall
        sleep(speed)

        #DESCRIPTION
        give.send_keys(desc)
        sleep(speed)

        #ATTACH MEDIA
        file = driver.find_element_by_xpath("//input[@data-testid='media-sprout']")
        sleep(speed)

        #sending media
        file.send_keys(path)
        #wait while it uploads
        sleep(speed*1.75)

        #POST
        post = driver.find_element_by_css_selector('button[data-testid="react-composer-post-button"]')
        post.click()
        #wait for post to be made
        sleep(speed*1.5)
        driver.close()
        return
    pass

app = Flask(__name__)

@app.route('/', methods = ['GET'])
def index():    
    return render_template('index.html')

@app.route('/', methods = ['POST'])
def go():
    fun = request.form['fun']
    fup = request.form['fup']
    if fun is None or fup is None:
        fun = fup = ""

    file = request.files['media']
    filename = secure_filename(file.filename)
    media = os.path.abspath(filename)
    file.save(media)

    desc = request.form['desc']

    speed = int(request.form['speed'])

    Facebook(fun,fup,media,desc,speed)

    return '''
            <script>
            alert('Success :)');
            window.location = "/";
            </script>
    '''

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=80,debug=False,threaded=True)