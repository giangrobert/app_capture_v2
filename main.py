import sys
from PyQt5.QtGui import QPixmap, QFont, QPalette, QBrush,QMovie,QIcon,QImage
from PyQt5.QtWidgets import QApplication, QMessageBox,QMainWindow, QPushButton, QLabel, QVBoxLayout, QWidget, QDesktopWidget
from PyQt5.QtCore import Qt, QTimer
import sys
import cv2
import os
import zipfile
import shutil

class WelcomeWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        # Establecer el título y la geometría de la ventana
        self.setWindowTitle("Página de Bienvenida")
        self.setStyleSheet("color: white;") 
        
        self.setGeometry(100, 100, 600, 400)

        # Remover los botones de maximizar, minimizar y cerrar
        self.setWindowFlags(Qt.Window | Qt.FramelessWindowHint)


         # Configurar una etiqueta para la imagen de fondo
        fondo = QLabel(self)
        fondo.setGeometry(0, 0, 800, 600)  # Establecer el tamaño de la etiqueta al tamaño de la ventana

        # Cargar la imagen de fondo
        fondo_imagen = QPixmap("D:/app_capture/src/imgs/bacground.jpg")
        fondo.setPixmap(fondo_imagen)

        # Mensaje de "BIENVENIDOS"
        self.welcomeLabel = QLabel("BIENVENIDOS", self)
        self.welcomeLabel.setFont(QFont('Arial', 24))
        self.welcomeLabel.setAlignment(Qt.AlignTop | Qt.AlignCenter)
        self.welcomeLabel.setGeometry(0, 50, self.width(), 50)



        # Configurar una etiqueta para el GIF animado
        gif_label = QLabel(self)
        gif_label.setGeometry(0, 0, self.width(), self.height())
        gif_movie = QMovie("D:/app_capture/src/imgs/infinity.gif")  
        gif_label.setMovie(gif_movie)
        gif_movie.start()
        gif_label.setAlignment(Qt.AlignBottom | Qt.AlignHCenter)

        # Centrar la ventana en la pantalla
        self.center_on_screen()

        # Cerrar la ventana automáticamente después de 5 segundos
        QTimer.singleShot(3000, self.startApp)

    def center_on_screen(self):
        screen = QDesktopWidget().screenGeometry()
        window_geometry = self.geometry()
        self.move(int((screen.width() - window_geometry.width()) / 2), 
                  int((screen.height() - window_geometry.height()) / 2))

    def startApp(self):
        self.mainWin = MainWindow()
        self.mainWin.show()
        self.close()


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Ventana Principal")
        self.setGeometry(100, 100, 800, 600)
        self.setWindowFlags(Qt.Window | Qt.FramelessWindowHint)
        

        # Configurar una etiqueta para la imagen de fondo
        fondo = QLabel(self)
        fondo.setGeometry(0, 0, self.width(), self.height())  # Ajustar al tamaño de la ventana

        # Cargar la imagen de fondo
        fondo_imagen = QPixmap("D:/app_capture/src/imgs/bg2.png")  # Reemplaza con la ruta de tu imagen de fondo
        fondo_imagen = fondo_imagen.scaled(self.width(), self.height(), Qt.KeepAspectRatioByExpanding)
        fondo.setPixmap(fondo_imagen)


         # Configurar un botón de cierre con una imagen de fondo
        boton_cerrar = QPushButton(self)
        boton_cerrar.setGeometry(self.width() - 30, 10, 20, 20)  # Posición y tamaño del botón
        
    
        icono_imagen = QPixmap("D:/app_capture/src/imgs/close.png")
        icono = QIcon(icono_imagen)
        boton_cerrar.setIcon(icono)
        boton_cerrar.setIconSize(icono_imagen.size())  
        boton_cerrar.setStyleSheet("background-color: transparent; border: none;")



        boton_cerrar.clicked.connect(self.cerrar_ventana)

    # Establecer el título de la ventana
        self.setWindowTitle("Instrucciones")

        # Configurar etiquetas con instrucciones
        etiqueta_instrucciones1 = QLabel("1. Mira directamente a la cámara.", self)
        etiqueta_instrucciones2 = QLabel("2. Asegúrate de tener buena iluminación.", self)
        etiqueta_instrucciones3 = QLabel("3. Evita obstrucciones.", self)
        etiqueta_instrucciones4 = QLabel("4. Mueve tu cabeza a la derecha y a la izquierda.", self)
        etiqueta_instrucciones5 = QLabel("5. Mueve tu cabeza.", self)
        etiqueta_instrucciones6 = QLabel("6. Permanece a una distancia moderada.", self)
        etiqueta_instrucciones7 = QLabel("7. Pulsa 'q' para finalizar la captura.", self)

        # Configurar geometría y alineación de etiquetas
        etiqueta_instrucciones1.setGeometry(self.width(), self.height() // 2 - 80, 200, 20)
        etiqueta_instrucciones1.setAlignment(Qt.AlignCenter)

        etiqueta_instrucciones2.setGeometry(self.width(), self.height() // 2 - 70, 200, 20)
        etiqueta_instrucciones2.setAlignment(Qt.AlignCenter)

        etiqueta_instrucciones3.setGeometry(self.width(), self.height() // 2 - 60, 200, 20)
        etiqueta_instrucciones3.setAlignment(Qt.AlignCenter)

        etiqueta_instrucciones4.setGeometry(self.width() // 2 - 100, self.height() // 2 - 50, 200, 20)
        etiqueta_instrucciones4.setAlignment(Qt.AlignCenter)

        etiqueta_instrucciones5.setGeometry(self.width() // 2 - 100, self.height() // 2 - 40, 200, 20)
        etiqueta_instrucciones5.setAlignment(Qt.AlignCenter)

        etiqueta_instrucciones6.setGeometry(self.width() // 2 - 100, self.height() // 2 - 30, 200, 20)
        etiqueta_instrucciones6.setAlignment(Qt.AlignCenter)

        etiqueta_instrucciones7.setGeometry(self.width() // 2 - 100, self.height() // 2 - 20, 200, 20)
        etiqueta_instrucciones7.setAlignment(Qt.AlignCenter)


        self.etiqueta_camara = QLabel(self)
        self.etiqueta_camara.setGeometry(50, 50, 640, 480)

        # Configurar un temporizador para actualizar la vista previa de la cámara
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.actualizar_vista_camara)
        self.captura = None  # Variable para la captura de la cámara

        self.center_on_screen()
           # Configurar la animación de hover
        boton_cerrar.setStyleSheet("""
         QPushButton {
                background-color: transparent;
                border: none;
            }
            QPushButton:hover {
                background-color: red;  /* Cambiar el color de fondo al pasar el mouse */
            }
        """)


      # Configurar un botón para iniciar la captura de la cámara
        self.boton_iniciar = QPushButton("🎞️ Iniciar Captura", self)
        self.boton_iniciar.setGeometry(50, 480, 200, 30)
        self.boton_iniciar.clicked.connect(self.iniciar_captura)

        # Obtener el tamaño de la pantalla
        screen_size = QDesktopWidget().screenGeometry()


        # Ajustar el texto del botón
        self.boton_iniciar.setStyleSheet("color: white; font-weight: bold; background-color: #00bfff; border-radius: 10px;")

        # Configurar un botón para descargar las capturas
        self.boton_descargar = QPushButton("💻 Descargar Capturas", self)
        self.boton_descargar.setGeometry(300, 480, 200, 30)
        self.boton_descargar.clicked.connect(self.descargar_capturas)
        self.boton_descargar.setEnabled(False)  # Deshabilitado al inicio

        self.boton_descargar.setStyleSheet("color: black; font-weight: bold; background-color: #FFC000; border-radius: 10px;")


        # Configurar un temporizador para actualizar la vista previa de la cámara
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.actualizar_vista_camara)
        self.captura = None  # Variable para la captura de la cámara
        self.capturando = False  # Indica si se está capturando
        self.tiempo_captura = 15 * 1000  # 15 segundos en milisegundos
        self.fotogramas_capturados = []

    def iniciar_captura(self):
        if not self.capturando:
            self.captura = cv2.VideoCapture(0)
            self.captura.set(cv2.CAP_PROP_CONVERT_RGB, 1.0)
            self.capturando = True
            self.timer.start(100)  # Actualizar cada 100 ms
            QTimer.singleShot(self.tiempo_captura, self.detener_captura)

    def detener_captura(self):
        if self.capturando:
            self.captura.release()
            self.timer.stop()
            self.boton_descargar.setEnabled(True)
            self.capturando = False

    def actualizar_vista_camara(self):
        if self.captura is not None:
            # Capturar un fotograma de la cámara
            ret, frame = self.captura.read()

            if ret:
                # Convertir el fotograma de OpenCV a formato QImage
                frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                h, w, ch = frame.shape
                bytes_per_line = ch * w
                q_image = QImage(frame.data, w, h, bytes_per_line, QImage.Format_RGB888)

                # Escalar la imagen para que se ajuste a la etiqueta de la cámara
                q_image = q_image.scaled(self.etiqueta_camara.size(), Qt.KeepAspectRatio)

                # Mostrar la imagen en la etiqueta de la cámara
                self.etiqueta_camara.setPixmap(QPixmap.fromImage(q_image))

                # Almacenar el fotograma capturado
                self.fotogramas_capturados.append(frame)

    def descargar_capturas(self):
        if self.fotogramas_capturados:
            carpeta_destino = "captura"
            os.makedirs(carpeta_destino, exist_ok=True)

            for i, fotograma in enumerate(self.fotogramas_capturados):
                nombre_archivo = os.path.join(carpeta_destino, f"captura_{i}.jpg")
                cv2.imwrite(nombre_archivo, fotograma)

            # Comprimir la carpeta en un archivo ZIP
            shutil.make_archive(carpeta_destino, 'zip', carpeta_destino)

            # # Mover el archivo ZIP a la carpeta de descargas
            # carpeta_zip = carpeta_destino + ".zip"
            # carpeta_descargas = os.path.expanduser("~/Dowloads")
            # shutil.move(carpeta_zip, carpeta_descargas)
            # Mostrar un mensaje informativo
            QMessageBox.information(self, "Guardado Exitoso", "Las capturas se han guardado correctamente en la carpeta de descargas. ¡Gracias por usar nuestra aplicación!")


    def center_on_screen(self):
            screen = QDesktopWidget().screenGeometry()
            window_geometry = self.geometry()
            self.move(int((screen.width() - window_geometry.width()) / 2), 
                    int((screen.height() - window_geometry.height()) / 2))
            
    def cerrar_ventana(self):
        self.close()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    win = WelcomeWindow()
    win.show()
    sys.exit(app.exec_())