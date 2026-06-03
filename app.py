from flask import Flask
from routes.usuario import ws_usuario
from routes.cita import ws_cita
from routes.especialidad import ws_especialidad
from routes.horario import ws_horario
from routes.medico import ws_medico
from routes.medico_especialidad import ws_medico_especialidad
from routes.administrativo import ws_administrativo
from routes.paciente import ws_paciente

app = Flask(__name__)
app.register_blueprint(ws_usuario, url_prefix='/api')
app.register_blueprint(ws_cita, url_prefix='/api')
app.register_blueprint(ws_especialidad, url_prefix='/api')
app.register_blueprint(ws_horario, url_prefix='/api')
app.register_blueprint(ws_medico, url_prefix='/api')
app.register_blueprint(ws_medico_especialidad, url_prefix='/api')
app.register_blueprint(ws_administrativo, url_prefix='/api')
app.register_blueprint(ws_paciente, url_prefix='/api')



@app.route('/')
def home():
    return 'MedicalApp - Running API Restful'


@app.route('/especialidades')
def especialidades():
   return 'Especialidades médicas'

#@app.route('/medicos')
#def medicos():
#    return 'Conozca a su médico'


#@app.route('/citas')
#def citas():
#    return 'Registre una cita desde la comodidad de su hogar'



#Iniciar el servicio web con Flask
if __name__ == '__main__':
    app.run(port=3007, debug=True, host='0.0.0.0')