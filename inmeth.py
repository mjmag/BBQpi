import web
from web import form
import subprocess
from functions import set_control, get_temp, update_figure


render = web.template.render('templates/')
urls = ('/', 'index', '/settings', 'settings')
app = web.application(urls, globals())

myform = form.Form(
    form.Checkbox('Turn on Control'),
    form.Textbox('Desired BBQ Temp',
                 form.notnull,
                 form.regexp('\d+', 'Error: Temperature must be a digit')),
    form.Checkbox('Turn on Alert'),
    form.Textbox("Highest Allowable Temp of BBQ",
                 form.notnull,
                 form.regexp('\d+', 'Error: Temperature must be a digit')),
    #form.Validator('Must be between 150 and 500 F', lambda x:150<int(x)<500)),
    form.Textbox("Desired Meat Temp",
                 form.notnull,
                 form.regexp('\d+', 'Error: Temperature must be a digit')),
    #form.Validator('Must be between 150 and 500 F', lambda x:150<int(x)<500)),
    form.Button("Submit"))


class index:
    def GET(self):
        tempout = get_temp()
        update_figure()
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
            input = web.input()
            cmd = []
            cmd.append('Turn on Control' in input)
            cmd.append(float(form['Desired BBQ Temp'].value))
            cmd.append(float(form['Turn on Alert'].checked))
            cmd.append('Highest Allowable Temp of BBQ' in input)
            cmd.append(float(form['Desired Meat Temp'].value))
            set_control(cmd)

            raise web.seeother('/')
