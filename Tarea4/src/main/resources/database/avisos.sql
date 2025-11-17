INSERT INTO aviso_adopcion (id, fecha_ingreso, comuna_id, sector, nombre, email, celular, tipo, cantidad, edad, unidad_medida, fecha_entrega, descripcion) VALUES (1,'2025-10-18 20:31:28',130208,'Barrio Universitario','Camila Soto','camila.soto@ejemplo.com','+56 9 5652 5155','gato',1,6,'m','2025-10-30 20:31:28','Gatita siamés muy cariñosa, ideal para departamento.');
INSERT INTO aviso_adopcion (id, fecha_ingreso, comuna_id, sector, nombre, email, celular, tipo, cantidad, edad, unidad_medida, fecha_entrega, descripcion) VALUES (2,'2025-10-11 20:31:28',130222,'Lo Hermida','Andrés Pizarro','andres.pizarro@ejemplo.com','+56 9 1234 5678','perro',2,2,'a','2025-11-02 20:31:28','Huskie siberiano, muy jugueton. Necesita patio grande.');
INSERT INTO aviso_adopcion (id, fecha_ingreso, comuna_id, sector, nombre, email, celular, tipo, cantidad, edad, unidad_medida, fecha_entrega, descripcion) VALUES (3,'2025-09-18 20:31:28',130220,'La Dehesa','Valentina Díaz','valentina.diaz@ejemplo.com','+56 9 9876 5432','perro',2,1,'a','2025-10-28 20:31:28','Boyeros de Berna, amigables con niños y otras mascotas. Adoptar juntos si es posible.');
INSERT INTO aviso_adopcion (id, fecha_ingreso, comuna_id, sector, nombre, email, celular, tipo, cantidad, edad, unidad_medida, fecha_entrega, descripcion) VALUES (4,'2025-09-22 20:31:28',130229,'Villa Las Parcelas','Javier Roa','javier.roa@ejemplo.com','+56 9 5555 4444','gato',1,3,'m','2025-11-07 20:31:28','Gatita carey rescatada, es un poco tímida al principio, pero muy leal.');
INSERT INTO aviso_adopcion (id, fecha_ingreso, comuna_id, sector, nombre, email, celular, tipo, cantidad, edad, unidad_medida, fecha_entrega, descripcion) VALUES (5,'2025-08-19 20:31:28',130102,'Chicureo','Sofía Morales','sofia.morales@ejemplo.com','+56 9 7777 8888','perro',1,3,'a','2025-10-25 20:31:28','Perro Pastor Suizo. Ideal para guardia y compañía, muy obediente.');
INSERT INTO comentario (id, nombre, texto, fecha, aviso_id) VALUES (1, 'Desarrollador', 'Tal parece que el comentario cargó bien desde la base de datos :)','2025-10-18 20:31:28',1);

INSERT INTO foto (id, ruta_archivo, nombre_archivo, actividad_id) VALUES (1,'uploads/siamese-cat.jpg','siamese-cat.jpg',1);
INSERT INTO foto (id, ruta_archivo, nombre_archivo, actividad_id) VALUES (2,'uploads/red-siberian-husky-portrait.jpg','red-siberian-husky-portrait.jpg',2);

INSERT INTO foto (id, ruta_archivo, nombre_archivo, actividad_id) VALUES (3,'uploads/boyer_de_berna_0.jpg','boyer_de_berna_0.jpg',3);

INSERT INTO foto (id, ruta_archivo, nombre_archivo, actividad_id) VALUES (4,'uploads/tortoiseshell-sadie.jpg','tortoiseshell-sadie.jpg',4);

INSERT INTO foto (id, ruta_archivo, nombre_archivo, actividad_id) VALUES (5,'uploads/het-hondenplein-01-de-zwitserse-wi.jpg','het-hondenplein-01-de-zwitserse-wi.jpg',5);

