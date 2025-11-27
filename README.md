===== TABLA NUEVA SQL ======

-- Crear base de datos
CREATE DATABASE IF NOT EXISTS edu_cursos;
USE edu_cursos;

-- Tabla Usuarios
CREATE TABLE usuarios (
    id_usuario INT PRIMARY KEY AUTO_INCREMENT,
    nombre VARCHAR(20) NOT NULL,
    apellido VARCHAR(20) NOT NULL,
    email VARCHAR(50) UNIQUE NOT NULL,
    password VARCHAR(50) NOT NULL,
    fecha_registro DATETIME DEFAULT NOW()
);

-- Tabla Cursos
CREATE TABLE cursos (
    id_curso INT PRIMARY KEY AUTO_INCREMENT,
    titulo VARCHAR(50) NOT NULL,
    descripcion TEXT NULL,
    categoria VARCHAR(50) NULL,
    duracion_horas INT NULL,
    fecha_creacion DATETIME DEFAULT NOW(),
    activo TINYINT(1) DEFAULT 1
);

-- Tabla Inscripciones
CREATE TABLE inscripciones (
    id_inscripcion INT PRIMARY KEY AUTO_INCREMENT,
    id_usuario INT NOT NULL,
    id_curso INT NOT NULL,
    fecha_inscripcion DATETIME DEFAULT NOW(),
    estado ENUM('Inscripto','En curso','Finalizado') DEFAULT 'Inscripto',
    FOREIGN KEY (id_usuario) REFERENCES usuarios(id_usuario),
    FOREIGN KEY (id_curso) REFERENCES cursos(id_curso)
);


-- Tabla Progreso
CREATE TABLE progreso (
    id_progreso INT PRIMARY KEY AUTO_INCREMENT,
    id_usuario INT NOT NULL,
    id_curso INT NOT NULL,
    modulo_actual INT DEFAULT 0,
    tema_actual INT DEFAULT 0,
    datos_progreso JSON,
    curso_completado TINYINT(1) DEFAULT 0,
    fecha_ultima_actualizacion DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,

    FOREIGN KEY (id_usuario) REFERENCES usuarios(id_usuario) ON DELETE CASCADE,
    FOREIGN KEY (id_curso) REFERENCES cursos(id_curso) ON DELETE CASCADE,

    UNIQUE KEY unique_user_course (id_usuario, id_curso)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

CREATE INDEX idx_usuario_curso ON progreso(id_usuario, id_curso);
CREATE INDEX idx_curso_completado ON progreso(curso_completado);


-- Tabla Pagos
CREATE TABLE pagos (
    id_pago INT PRIMARY KEY AUTO_INCREMENT,
    id_usuario INT NOT NULL,
    id_curso INT NOT NULL,
    monto DECIMAL(10,2) NOT NULL,
    metodo_pago ENUM('Tarjeta','PayPal','Transferencia') NOT NULL,
    fecha_pago DATETIME DEFAULT NOW(),
    estado_pago ENUM('Pendiente','Aprobado','Rechazado') DEFAULT 'Pendiente',
    FOREIGN KEY (id_usuario) REFERENCES usuarios(id_usuario),
    FOREIGN KEY (id_curso) REFERENCES cursos(id_curso)
);

-- Tabla Certificados
CREATE TABLE certificados (
    id_certificado INT PRIMARY KEY AUTO_INCREMENT,
    id_inscripcion INT NOT NULL,
    codigo_unico VARCHAR(50) UNIQUE NOT NULL,
    fecha_emision DATETIME DEFAULT NOW(),
    url_pdf VARCHAR(100) NULL,
    FOREIGN KEY (id_inscripcion) REFERENCES inscripciones(id_inscripcion)
);

-- Tabla Reembolsos
CREATE TABLE reembolsos (
    id_reembolso INT PRIMARY KEY AUTO_INCREMENT,
    id_pago INT NOT NULL,
    fecha_solicitud DATETIME DEFAULT NOW(),
    motivo TEXT NULL,
    estado_reembolso ENUM('Pendiente','Aprobado','Rechazado') DEFAULT 'Pendiente',
    FOREIGN KEY (id_pago) REFERENCES pagos(id_pago)
);









================= LO QUE SE FUÉ AGREGANDO  ======================



ALTER TABLE cursos
ADD COLUMN imagen TEXT,
ADD COLUMN precio DECIMAL(10,2);



----------------------------------------



ALTER TABLE usuarios
ADD COLUMN fecha_nacimiento DATE NULL AFTER apellido,
ADD COLUMN dni VARCHAR(20) NULL AFTER fecha_nacimiento,
ADD COLUMN telefono VARCHAR(30) NULL AFTER dni;




-------------------------------------------------------



SE ELIMINA LA TABLA MODULOS



-------------------------------------------------------

PARTE PARA EL ADMIN:

-- Agregar columna 'rol' a la tabla usuarios
ALTER TABLE usuarios 
ADD COLUMN rol ENUM('estudiante', 'admin') NOT NULL DEFAULT 'estudiante' AFTER password;

-- Insertar usuario administrador
INSERT INTO usuarios (nombre, apellido, email, password, rol) 
VALUES ('Admin', 'Sistema', 'admin@educacionit.com', 'admin123', 'admin');



--------------------------------------------------------





AGREGAR EN CURSOS:

INSERT INTO cursos (titulo, descripcion, categoria, duracion_horas, precio, imagen)
VALUES 
('Manejo de IA', 'Aprenderás a utilizar herramientas de inteligencia artificial para generar contenido atractivo e integrarlo en tus proyectos.', 'Inteligencia Artificial', 40, 35000, 'cursos_copy/ia.JPG'),
('Chat GPT', 'Aprende a interactuar y generar respuestas con Chat GPT de forma efectiva para tus proyectos y aplicaciones.', 'Inteligencia Artificial', 35, 30000, 'cursos_copy/11.JPG'),
('IA para contenido visual', 'Aprenderás a utilizar herramientas de IA para generar contenido visual atractivo e integrarlo en tus proyectos.', 'Inteligencia Artificial', 40, 35000, 'cursos_copy/Captura1.JPG'),
('IA avanzada para proyectos', 'Profundiza en técnicas avanzadas de IA y aprende a implementarlas en proyectos complejos.', 'Inteligencia Artificial', 50, 40000, 'cursos_copy/ia-generativa-1.jpeg');

INSERT INTO cursos (titulo, descripcion, categoria, duracion_horas, precio, imagen)
VALUES 
('Python', 'Ideal para analizar y gestionar datos en tiempo real gracias a su sencillez y gran número de bibliotecas.', 'Programación y Desarrollo', 45, 25000, 'cursos_copy/python.JPG'),
('Java', 'Aprende a crear aplicaciones robustas y portables para diversas plataformas con Java.', 'Programación y Desarrollo', 50, 28000, 'cursos_copy/java.JPG'),
('.Net', 'Crea aplicaciones escalables para web, escritorio, móviles y servicios en la nube.', 'Programación y Desarrollo', 50, 27000, 'cursos_copy/net.JPG'),
('JavaScript', 'Aprende los fundamentos y desarrolla soluciones dinámicas y eficientes con ejercicios prácticos.', 'Programación y Desarrollo', 40, 26000, 'cursos_copy/javascrip.JPG');

INSERT INTO cursos (titulo, descripcion, categoria, duracion_horas, precio, imagen)
VALUES 
('Community Manager', 'Aprende a gestionar comunidades online, crear contenido y fomentar la interacción con seguidores.', 'Marketing Digital', 35, 20000, 'cursos_copy/managger.JPG'),
('SEO', 'Optimiza tu sitio web para buscadores y mejora la visibilidad de tu marca.', 'Marketing Digital', 30, 22000, 'cursos_copy/SEO.png'),
('Publicidad en Redes Sociales', 'Aprende a crear campañas efectivas en Facebook, Instagram y LinkedIn.', 'Marketing Digital', 40, 25000, 'cursos_copy/META-ADS.png'),
('Marketing de Contenido', 'Domina las estrategias de correo electrónico para fidelizar clientes y aumentar ventas.', 'Marketing Digital', 25, 18000, 'cursos_copy/CANVA.png');

INSERT INTO cursos (titulo, descripcion, categoria, duracion_horas, precio, imagen)
VALUES 
('Introducción a UI/UX', 'Conceptos básicos, esenciales y prácticos de diseño de interfaces. Experiencia de usuario, abarcando principios de usabilidad.', 'Diseño UI/UX', 35, 25000, 'cursos_copy/ui-ux.jpg'),
('UI Animations / Microinteracciones', 'Animaciones sutiles, feedback visual para el usuario, transiciones y diseño responsivo.', 'Diseño UI/UX', 35, 25000, 'cursos_copy/experiencia-do-usuario-ux.jpg'),
('Herramientas de Diseño Profesionales/Avanzado', 'Manejo de Figma, Adobe XD, diseños intuitivos, funcionales y visualmente atractivos.', 'Diseño UI/UX', 30, 22000, 'cursos_copy/ui.jpg'),
('UX para productos digitales', 'Diseño centrado en el usuario para mejorar la experiencia en productos digitales.', 'Diseño UI/UX', 40, 30000, 'cursos_copy/diseno-productos-digitales.jpg');

INSERT INTO cursos (titulo, descripcion, categoria, duracion_horas, precio, imagen)
VALUES 
('Ciencia de Datos', 'Desarrollo e implementación de soluciones basadas en Big Data, Machine Learning y Deep Learning.', 'Big Data', 40, 22000, 'cursos_copy/OPTIMIZACION.png'),
('Introducción a Big Data', 'Conoce los fundamentos del Big Data, arquitecturas distribuidas y ecosistemas de datos masivos.', 'Big Data', 40, 24000, 'cursos_copy/BigData.png'),
('IA y Big Data', 'Aprende a manejar grandes volúmenes de datos con Hadoop y Spark para análisis distribuidos.', 'Big Data', 45, 28000, 'cursos_copy/Data.jpg'),
('Análisis de Datos', 'Analiza datos masivos aplicando estadísticas, machine learning y visualización con Python.', 'Big Data', 45, 30000, 'cursos_copy/POWER-BI.png');


