import sys
from PyQt5.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout,
                            QLineEdit, QTextEdit, QLabel, QPushButton, QDateEdit,
                            QFormLayout, QDialog, QRadioButton, QMessageBox)
import bcrypt
import mysql.connector
# import smtplib (proximamente se utilizara en nuevas funciones)

class MyLogin(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Login")
        self.setGeometry(100,100,350,180)
        self.setContentsMargins(20,20,20,20)
        
        try:
            self.db = mysql.connector.connect(
                user="root",# Aqui se coloca el user, creo que siempre seria root
                password="12345", # Aqui colocas tu contraseña
                host="localhost",
                database="biblioteca"
            )
            print("Conexion exitosa")
        except:
            QMessageBox.warning(self, "Error", "No se pudo conectar a la base de datos")
        
        center = QWidget()
        layout = QFormLayout()
        
        lbl = QLabel("Inicio de sesion")
        lbl_name = QLabel("Ingrese su nombre de usuario:")
        lbl_pw = QLabel("Contraseña: ")
        
        self.txt_name = QLineEdit()
        self.txt_pw = QLineEdit()
        self.txt_pw.setEchoMode(QLineEdit.Password)
        self.btn = QPushButton("Iniciar")
        self.btn.clicked.connect(self.clicked_btn)
        
        self.label = QLabel("¿Crear una cuenta?")
        self.reg = QPushButton("Registrarse")
        self.reg.clicked.connect(self.clicked_reg)
        
        layout.addRow(lbl)
        layout.addRow(lbl_name, self.txt_name)
        layout.addRow(lbl_pw, self.txt_pw)
        layout.addRow(self.btn)
        layout.addRow(self.label, self.reg)
        center.setLayout(layout)
        self.setCentralWidget(center)
        
    def clicked_btn(self):
        user = self.txt_name.text()
        pw = self.txt_pw.text()
        
        if not user or not pw:
            QMessageBox.warning(self, "Error", "Por favor ingrese su usuario y contraseña")
        else:
            cursor = self.db.cursor()
            cursor.execute(f"SELECT * FROM usuario WHERE user_name ='{user}'")
            result = cursor.fetchone()
            if result:
                username = result[3]
                stored_pw = result[5].encode()  # No es necesario encodear la contraseña almacenada
                pw_encoded = pw.encode()
                if bcrypt.checkpw(pw_encoded, stored_pw):
                    QMessageBox.information(self, "Sesión iniciada", "Bienvenido")
                    self.hide()
                    main_window = miBiblioteca(self, self)
                    main_window.show()
                else:
                    QMessageBox.warning(self, "Error", "Contraseña incorrecta")
            else:
                QMessageBox.warning(self, "Error", "Usuario no encontrado")
                
    def clicked_reg(self):
        reg_window = register_user(self)
        reg_window.show()


class register_user(QMainWindow):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.parent = parent
        self.setWindowTitle("Registrarse")
        self.setGeometry(100,100,350,250)
        self.setContentsMargins(20,20,20,20)
        
        center = QWidget()
        layout = QFormLayout()
        
        lbl = QLabel("Registrarse")
        lbl_name = QLabel("Ingrese su nombre:")
        lbl_lastname = QLabel("Ingrese su apellido:")
        lbl_un = QLabel("Ingrese un nombre de usuario:")
        lbl_email = QLabel("Ingrese un correo:")
        lbl_pw = QLabel("Contraseña: ")
        lbl_pw2 = QLabel("Confirmar contraseña: ")
        
        self.txt_name = QLineEdit()
        self.txt_lastname = QLineEdit()
        self.txt_un = QLineEdit()
        self.txt_email = QLineEdit()
        self.txt_pw = QLineEdit()
        self.txt_pw.setEchoMode(QLineEdit.Password)
        self.txt_pw2 = QLineEdit()
        self.txt_pw2.setEchoMode(QLineEdit.Password)
        self.btn_reg = QPushButton("Registrarse")
        self.btn_reg.clicked.connect(self.register)
        
        layout.addRow(lbl)
        layout.addRow(lbl_name, self.txt_name)
        layout.addRow(lbl_lastname, self.txt_lastname)
        layout.addRow(lbl_un, self.txt_un)
        layout.addRow(lbl_email, self.txt_email)
        layout.addRow(lbl_pw, self.txt_pw)
        layout.addRow(lbl_pw2, self.txt_pw2)
        layout.addRow(self.btn_reg)
        center.setLayout(layout)
        self.setCentralWidget(center)
        
    def register(self):
        name = self.txt_name.text()
        lastname = self.txt_lastname.text()
        un = self.txt_un.text()
        email = self.txt_email.text()
        pw = self.txt_pw.text()
        pw2 = self.txt_pw2.text()
        
        if not name or not lastname or not un or not email or not pw or not pw2:
            QMessageBox.warning(self, "Error", "Por favor ingrese todos los campos")
        elif pw != pw2:
            QMessageBox.warning(self, "Error", "Las contraseñas no coinciden")
        else:
            pw_encoded = pw.encode()
            salt = bcrypt.gensalt(12)
            hash_pw = bcrypt.hashpw(pw_encoded, salt)
            
            cursor = self.parent.db.cursor()
            cursor.execute("INSERT INTO usuario (nombre, apellido, user_name, email, contraseña) VALUES (%s, %s, %s, %s, %s)", (name,lastname, un, email, hash_pw))
            self.parent.db.commit()
            
            QMessageBox.information(self, "Registro exitoso", "Usuario creado con éxito")
            self.close()


class miBiblioteca(QMainWindow):
    def __init__(self, parent=None, login=None):
        super().__init__(parent)
        self.login = login
        
        self.setGeometry(100,100,450,380)
        self.setWindowTitle("Mis libros")
        self.setContentsMargins(25,10,25,20)
        
        try:
            self.db = mysql.connector.connect(
                user="root",# Aqui se coloca el user, creo que siempre seria root
                password="12345", # Aqui colocas tu contraseña
                host="localhost",
                database="biblioteca"
            )
            print("Conexion exitosa")
        except:
            QMessageBox.warning(self, "Error", "No se pudo conectar a la base de datos")
        
        center = QWidget()
        layout = QFormLayout()
        
        lbl1 = QLabel("Ingrese los datos del libro:\n")
        self.lbl_titulo = QLabel("Ingrese el titulo:")
        self.txt_titulo = QLineEdit()
        self.lbl_autor = QLabel("Ingrese el autor: ")
        self.txt_autor = QLineEdit()
        self.lbl_genero = QLabel("Ingrese el genero:")
        self.txt_genero = QLineEdit()
        self.lbl_editorial = QLabel("Ingrese la editorial:")
        self.txt_editorial = QLineEdit() 
        self.lbl_sinopsis= QLabel("Ingrese una sinopsis:")
        self.txt_sinopsis = QLineEdit()
        self.lbl_fecha = QLabel("Ingrese la fecha de publicacion:")
        self.txt_fecha = QDateEdit()  
        self.lbl_estado = QLabel("Ingrese el estado:")
        self.txt_estado = QLineEdit()
        self.btn_add = QPushButton("Agregar libro")
        self.btn_see = QPushButton("Ver Libros")
        self.btn_add.clicked.connect(self.clicked_add)
        self.btn_see.clicked.connect(self.clicked_see)
        self.view = QTextEdit()
        
        self.btn_update = QPushButton("Actualizar mis libros")
        self.btn_update.clicked.connect(self.clicked_update)
        self.btn_delete = QPushButton("Eliminar un libro")
        self.btn_delete.clicked.connect(self.clicked_delete)
        self.btn_search = QPushButton("Buscar libro")
        self.btn_search.clicked.connect(self.clicked_search)
        self.btn_exit = QPushButton("Cerrar sesión")
        self.btn_exit.clicked.connect(self.clicked_exit)
        
        layout.addRow(lbl1)
        layout.addRow(self.lbl_titulo, self.txt_titulo)
        layout.addRow(self.lbl_autor, self.txt_autor)
        layout.addRow(self.lbl_genero, self.txt_genero)
        layout.addRow(self.lbl_editorial, self.txt_editorial)
        layout.addRow(self.lbl_sinopsis, self.txt_sinopsis)
        layout.addRow(self.lbl_fecha, self.txt_fecha)
        layout.addRow(self.lbl_estado, self.txt_estado)
        layout.addRow(self.btn_add, self.btn_see)
        layout.addRow(self.view)
        layout.addRow(self.btn_update, self.btn_delete)
        layout.addRow(self.btn_search)
        layout.addRow(self.btn_exit)
        
        center.setLayout(layout)
        self.setCentralWidget(center)
        
    def clicked_add(self):
        try:
            cursor = self.db.cursor()
            titulo = self.txt_titulo.text()
            autor = self.txt_autor.text()
            genero = self.txt_genero.text()
            editorial = self.txt_editorial.text()
            sinopsis = self.txt_sinopsis.text()
            fecha_publicacion = self.txt_fecha.date().toString("yyyy-MM-dd")
            estado = self.txt_estado.text()
            
            cursor.execute("""
                INSERT INTO libro (titulo, autor, genero, editorial, sinopsis, fecha_publicacion, estado)
                VALUES (%s, %s, %s, %s, %s, %s, %s)
            """, (titulo, autor, genero, editorial, sinopsis, fecha_publicacion, estado))
            self.db.commit()
            self.view.setText("Libro agregado con éxito")
        except:
            self.view.setText("Error al agregar libro")
        finally:
            self.txt_titulo.clear()
            self.txt_autor.clear()
            self.txt_genero.clear()
            self.txt_editorial.clear()
            self.txt_sinopsis.clear()
            self.txt_fecha.setDate(QDateEdit.currentDate())
            self.txt_estado.clear()
    
    def clicked_see(self):
        cursor = self.db.cursor()
        cursor.execute("SELECT * FROM libro")
        resultados = cursor.fetchall()
        
        texto = "Libros:\n"
        texto += "---------------------------\n"
        for fila in resultados:
            texto += f"Título: {fila[1]}\n"
            texto += f"Autor: {fila[2]}\n"
            texto += f"Género: {fila[3]}\n"
            texto += f"Editorial: {fila[4]}\n"
            texto += f"Sinopsis: {fila[5]}\n"
            texto += f"Fecha de publicación: {fila[6]}\n"
            texto += f"Estado: {fila[7]}\n"
            texto += "---------------------------\n"
        self.view.setText(texto)
        
    def clicked_update(self):
        self.question = QDialog()
        self.question.setWindowTitle("Actualizar libro")
        
        layout = QFormLayout()
        self.lbl_id = QLabel("ID del libro:")
        self.txt_id = QLineEdit()
        self.lbl_titulo = QLabel("Título:")
        self.txt_titulo_update = QLineEdit()
        self.lbl_autor = QLabel("Autor:")
        self.txt_autor_update = QLineEdit()
        self.lbl_genero = QLabel("Género:")
        self.txt_genero_update = QLineEdit()
        self.lbl_editorial = QLabel("Editorial:")
        self.txt_editorial_update = QLineEdit()
        self.lbl_sinopsis = QLabel("Sinopsis:")
        self.txt_sinopsis_update = QLineEdit()
        self.lbl_fecha = QLabel("Fecha de publicación:")
        self.txt_fecha_update = QDateEdit()
        self.lbl_estado = QLabel("Estado:")
        self.txt_estado_update = QLineEdit()
        
        btn_yes = QPushButton("Actualizar")
        btn_yes.clicked.connect(self.exec_update)
        btn_no = QPushButton("Volver")
        btn_no.clicked.connect(lambda: self.question.reject())
        
        layout.addRow(self.lbl_id, self.txt_id)
        layout.addRow(self.lbl_titulo, self.txt_titulo_update)
        layout.addRow(self.lbl_autor, self.txt_autor_update)
        layout.addRow(self.lbl_genero, self.txt_genero_update)
        layout.addRow(self.lbl_editorial, self.txt_editorial_update)
        layout.addRow(self.lbl_sinopsis, self.txt_sinopsis_update)
        layout.addRow(self.lbl_fecha, self.txt_fecha_update)
        layout.addRow(self.lbl_estado, self.txt_estado_update)
        layout.addRow(btn_yes, btn_no)
        
        self.question.setLayout(layout)
        if self.question.exec_() == QDialog.Accepted:
            self.exec_update()
            
    def exec_update(self):
        try:
            cursor = self.db.cursor()
            id_libro = int(self.txt_id.text())
            titulo = self.txt_titulo_update.text()
            autor = self.txt_autor_update.text()
            genero = self.txt_genero_update.text()
            editorial = self.txt_editorial_update.text()
            sinopsis = self.txt_sinopsis_update.text()
            fecha_publicacion = self.txt_fecha_update.date().toString("yyyy-MM-dd")
            estado = self.txt_estado_update.text()
            
            cursor.execute("""
                UPDATE libro
                SET titulo = %s, autor = %s, genero = %s, editorial = %s, sinopsis = %s, fecha_publicacion = %s, estado = %s
                WHERE id = %s
            """, (titulo, autor, genero, editorial, sinopsis, fecha_publicacion, estado, id_libro))
            self.db.commit()
            self.view.setText("Libro actualizado con éxito")
        except:
            self.view.setText("Error al actualizar libro")
        finally:
            self.question.accept()
    
    def clicked_delete(self):
        self.question = QDialog()
        self.question.setWindowTitle("Eliminar libro")
        
        layout = QFormLayout()
        self.lbl_id = QLabel("ID del libro:")
        self.txt_id = QLineEdit()
        btn_yes = QPushButton("Eliminar")
        btn_yes.clicked.connect(self.exec_delete)
        btn_no = QPushButton("Volver")
        btn_no.clicked.connect(lambda: self.question.reject())
        
        layout.addRow(self.lbl_id, self.txt_id)
        layout.addRow(btn_yes, btn_no)
        self.question.setLayout(layout)
        if self.question.exec_() == QDialog.Accepted:
            self.exec_delete()
            
    def exec_delete(self):
        try:
            cursor = self.db.cursor()
            id_libro = int(self.txt_id.text())
            cursor.execute("DELETE FROM libro WHERE id = %s", (id_libro,))
            self.db.commit()
            self.view.setText("Libro eliminado con éxito")
        except:
            self.view.setText("Error al eliminar libro")
        finally:
            self.question.accept()
    
    def clicked_search(self):
        self.question = QDialog()
        self.question.setWindowTitle("Buscar libro")
        layout = QFormLayout()
        self.lbl_id = QLabel("ID del libro:")
        self.txt_id = QLineEdit()
        
        btn_yes = QPushButton("Buscar")
        btn_yes.clicked.connect(self.exec_search)
        btn_no = QPushButton("Volver")
        btn_no.clicked.connect(lambda: self.question.reject())
        layout.addRow(self.lbl_id, self.txt_id)
        layout.addRow(btn_yes, btn_no)
        self.question.setLayout(layout)
        
        if self.question.exec_() == QDialog.Accepted:
            pass
        
    def exec_search(self):
        try:
            cursor = self.db.cursor()
            id_libro = int(self.txt_id.text())
            cursor.execute("SELECT * FROM libro WHERE id = %s", (id_libro,))
            resultados = cursor.fetchall()
            
            if resultados:
                texto = "Libro encontrado:\n"
                for fila in resultados:
                    texto += f"Título: {fila[1]}\n"
                    texto += f"Autor: {fila[2]}\n"
                    texto += f"Género: {fila[3]}\n"
                    texto += f"Editorial: {fila[4]}\n"
                    texto += f"Sinopsis: {fila[5]}\n"
                    texto += f"Fecha de publicación: {fila[6]}\n"
                    texto += f"Estado: {fila[7]}\n"
                self.view.setText(texto)
            else:
                self.view.setText("Libro no encontrado")
        except:
            self.view.setText("Error al buscar libro")
        finally:
            self.question.accept()
            
    def clicked_exit(self):
        self.question = QDialog()
        self.question.setWindowTitle("Cerrar sesión")
        
        layout = QVBoxLayout()
        label = QLabel("¿Está seguro de cerrar sesión?")
        btn_yes = QPushButton("Si")
        btn_no = QPushButton("No")
        btn_no.setChecked(True)
        
        btn_yes.clicked.connect(self.exit_main)
        btn_no.clicked.connect(lambda: self.question.reject())
        layout.addWidget(label)
        layout.addWidget(btn_yes)
        layout.addWidget(btn_no)
        
        self.question.setLayout(layout)
        if self.question.exec_() == QDialog.Accepted:
            self.exit_main()
            
    def exit_main(self):
        self.hide()
        self.login.show()
        self.login.txt_name.clear()
        self.login.txt_pw.clear()

app = QApplication(sys.argv)
login = MyLogin()
login.show()
sys.exit(app.exec_())