import web
from web import form
import smtplib

render = web.template.render('templates/')
urls = ('/', 'Alert')
app = web.application(urls, globals())

# Alert System Input      

alert = form.Form(
    form.Textbox("Username", post="@gmail.com"),
    form.Password("Password"),
    form.Textbox("Phone Number", 
    	form.Validator('Please enter a valid 10 digit phone number.', lambda x:int(x)!=10), size='10', maxlength='10'),
    form.Dropdown('Carrier', ['AT&T', 'Verizon', 'Sprint', 'T-Mobile', 'Simple Mobile']),
    form.Checkbox('Default Alert'),
    form.Textarea('Personal Alert'),
    form.Button('Warn Me!'))

class Alert:

    def GET(self): 
        form = alert()
        return render.alertwebsite(form) 

    def POST(self):		
		form = alert()
		if not form.validates(): 
			return render.alertwebsite(form)
		else:
			input1 = alert(web.input())
			email = input1['Username'].value
			password = input1['Password'].value
			number = input1['Phone Number'].value
			input2 = web.input()
			if input2.get('Carrier') == 'At&T':
				carrier = '@txt.att.net'
			elif input2.get('Carrier') == 'Verizon':
				carrier = '@vtext.com'
			elif input2.get('Carrier') == 'Sprint':
				carrier = '@messaging.sprintpcs.com'
			elif input2.get('Carrier') == 'T-Mobile':
				carrier = '@tmomail.net'
			elif input2.get('Carrier') == 'Simple Mobile':
				carrier = '@smtext.com'
			input3 = web.input()
			if input3.has_key('Default Alert') == True:
				message = 'Your meat needs care!'
			else:
				message = input1['Personal Alert'].value
		
			server = smtplib.SMTP("smtp.gmail.com", 587)
			server.starttls()
			server.login(str(email) + '@gmail.com', str(password))
			server.sendmail('User', str(number) + str(carrier), str(message))		
		
			return render.alertwebsite(form)
			
if __name__=="__main__":
    web.internalerror = web.debugerror
    app.run()