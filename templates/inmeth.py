import web
from web import form
import subprocess

render = web.template.render('templates/')

urls = ('/', 'index', '/settings', 'settings')
app = web.application(urls, globals())

myform = form.Form(
	form.Checkbox('Turn on Control'),
    form.Textbox('Set Point',
     	form.notnull,
     	form.regexp('\d+', 'Error: Temperature must be a digit')),
    form.Checkbox('Turn on Alert'),
    form.Textbox("Highest allowable Temp. of BBQ",
    	form.notnull,
    	form.regexp('\d+', 'Error: Temperature must be a digit')),
    	#form.Validator('Must be between 150 and 500 F', lambda x:150<int(x)<500)),
    form.Textbox("Desired Temp. of BBQ",
    	form.notnull,
    	form.regexp('\d+', 'Error: Temperature must be a digit')),
    	#form.Validator('Must be between 150 and 500 F', lambda x:150<int(x)<500)),
    form.Button("Submit"))

class index:
	def GET(self):
		temp = subprocess.check_output(["tail", "-1", '/var/www/cgi-bin/temp.csv'])
		templist = temp.split(',')
		tempout = [templist[1], templist[2].strip("\r\n")]
		return render.main_page(tempout)

class settings:

    def GET(self): 
        form = myform()
        return render.inputwebsite(form)

    def POST(self):
        form = myform()
        if not form.validates():
        	return render.inputwebsite(form)
        else:
        	input1 = web.input()
        	input2 = myform(web.input())
        	setpoint = input2['Set Point'].value
        	input3 = web.input()
        	input4 = myform(web.input())
        	hightemp = input4['Highest allowable Temp. of BBQ'].value
        	input5 = myform(web.input())
        	destemp = input5['Desired Temp. of BBQ'].value
        	if input1.has_key('Turn on Control') == True:
        		control = '1'
        	else:
        		control = '0'

        	if input3.has_key('Turn on Alert') == True:
        		alert = '1'
        	else:
        		alert = '0'

        	controller = open('control.csv','w')
        	controller.write(str(control) + '\n')
        	controller.write(str(setpoint) + '\n')
          	controller.write(str(alert) + '\n')
           	controller.write(str(hightemp) + '\n')
           	controller.write(str(destemp))
        	controller.close()

         	raise web.seeother('/')
