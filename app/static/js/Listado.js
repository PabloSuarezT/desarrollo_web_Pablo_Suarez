
const avisosAdopcion = [
    {
        id: 1,
        fechaPublicacion: '2025-01-25 13:00',
        fechaEntrega: '2025-01-30 15:00',
        region: 'Región Metropolitana de Santiago', 
        comuna: 'Lo Barnechea',
        sector: 'La Dehesa',
        cantidad: 1,
        tipo: 'Perro',
        edad: '5 años',
        nombreContacto: 'Hector',
        email: 'terminhector@gmail..com', 
        celular: '+56 9 5652 5155', 
        contactoPor: 'Whatsapp',
        descripcion: 'Sam es un samoyedo muy juguetón y amigable. Le encanta correr y es muy bueno con los niños. Busca una familia que le dé mucho cariño.', // Agregado
        totalFotos: 1,
        fotos: [
            { src: 'https://www.publicdomainpictures.net/pictures/60000/nahled/het-hondenplein-01-de-zwitserse-wi.jpg', alt: 'Foto de Sam' }
        ]
    },
    {
        id: 2,
        fechaPublicacion: '2025-04-02 18:00',
        fechaEntrega: '2025-04-05 10:00',
        region: 'Región Metropolitana de Santiago',
        comuna: 'Peñalolén',
        sector: 'Lo Hermida',
        cantidad: 2,
        tipo: 'Perro',
        edad: '3 años',
        nombreContacto: 'Sofía',
        email: 'cssofia@gmail.com',
        celular: '+56 9 5398 2175', 
        contactoPor: 'Telegram', 
        descripcion: 'Brandon y Osha son hermanos, muy apegados entre sí. Boyeros de Berna que buscan un hogar con espacio para jugar y un dueño que los quiera a ambos.', // Agregado
        totalFotos: 1,
        fotos: [
            { src: 'https://www.patasencasa.com/sites/default/files/2024-08/boyer_de_berna_0.jpg', alt: 'Foto de Brandon y Osha' }
        ]
    },
    {
        id: 3,
        fechaPublicacion: '2025-03-30 9:00',
        fechaEntrega: '2025-04-03 12:00',
        region: 'Región Metropolitana de Santiago',
        comuna: 'Colina',
        sector: 'Chicureo',
        cantidad: 1,
        tipo: 'Perro',
        edad: '5 meses',
        nombreContacto: 'Millarai',
        email: 'htmllarai@gmail.com.com', 
        celular: '+56 9 1472 5223', 
        contactoPor: 'Whatsapp', 
        descripcion: 'Antupi es un cachorro de husky muy enérgico. Está listo para ser adoptado por una familia responsable.', // Agregado
        totalFotos: 1,
        fotos: [
            { src: 'https://www.publicdomainpictures.net/pictures/230000/nahled/red-siberian-husky-portrait.jpg', alt: 'Foto de Antupi' }
        ]
    },
    {
        id: 4,
        fechaPublicacion: '2025-05-01 19:00',
        fechaEntrega: '2025-05-05 16:00',
        region: 'Región Metropolitana de Santiago', 
        comuna: 'Estacion Central',
        sector: 'Villa Las Parcelas',
        cantidad: 1,
        tipo: 'Gato',
        edad: '2 años',
        nombreContacto: 'Pablo',
        email: 'phpablo@gmail.com',
        celular: '+56 9 9290 9125',
        contactoPor: 'Whatsapp',
        descripcion: 'Felicia es una gata siamesa tranquila y cariñosa. Le gusta estar en interiores y es perfecta para un apartamento.', // Agregado
        totalFotos: 1,
        fotos: [
            { src: 'https://www.publicdomainpictures.net/pictures/220000/nahled/siamese-cat.jpg', alt: 'Foto de Felicia' }
        ]
    },
    {
        id: 5,
        fechaPublicacion: '2025-07-07 15:32',
        fechaEntrega: '2025-07-10 11:00',
        region: 'Región Metropolitana de Santiago', 
        sector: 'El Golf',
        cantidad: 1,
        tipo: 'Gato',
        edad: '2 meses',
        nombreContacto: 'Javier',
        email: 'javaer@gmail.com', 
        celular: '+56 9 1632 5192',
        contactoPor: 'X',
        descripcion: 'Jeyne es una gata carey muy juguetona y curiosa. Ideal para una casa con jardín.',
        totalFotos: 1,
        fotos: [
            { src: 'https://www.publicdomainpictures.net/pictures/20000/nahled/tortoiseshell-sadie.jpg', alt: 'Foto de Jeyne' }
        ]
    }
];

// Espera a que el DOM esté completamente cargado.
document.addEventListener('DOMContentLoaded', () => {

    const listaAvisosDiv = document.getElementById('lista-avisos');
    const detalleAvisoDiv = document.getElementById('detalle-aviso');
    const listadoPrincipal = document.getElementById('listado-principal');

    // Agrega un 'event listener' al listado principal.
    listadoPrincipal.addEventListener('click', (event) => {
        // Identifica la fila (tr) más cercana al elemento clickeado.
        let filaClickeada = event.target.closest('tr');
        if (!filaClickeada) return;

        // Obtiene el ID del aviso desde el atributo 'data-id'.
        const avisoId = parseInt(filaClickeada.getAttribute('data-id'));
        // Busca el aviso correspondiente en el arreglo.
        const aviso = avisosAdopcion.find(av => av.id === avisoId);
        if (!aviso) return;

        // Oculta el listado y muestra la sección de detalles.
        listaAvisosDiv.style.display = 'none';
        detalleAvisoDiv.style.display = 'block';

        detalleAvisoDiv.innerHTML = `
            <h2>Detalles del Aviso</h2>
            <p><strong>Fecha de Publicación:</strong> ${aviso.fechaPublicacion}</p>
            <p><strong>Fecha de Entrega:</strong> ${aviso.fechaEntrega}</p>
            <p><strong>Región:</strong> ${aviso.region}</p>
            <p><strong>Comuna:</strong> ${aviso.comuna}</p>
            <p><strong>Sector:</strong> ${aviso.sector}</p>
            <p><strong>Cantidad/Tipo/Edad:</strong> ${aviso.cantidad} ${aviso.tipo}/${aviso.edad}</p>
            <p><strong>Nombre Contacto:</strong> ${aviso.nombreContacto}</p>
            <p><strong>Email:</strong> ${aviso.email}</p>
            <p><strong>Celular:</strong> ${aviso.celular}</p>
            <p><strong>Contactar por:</strong> ${aviso.contactoPor}</p>
            <p><strong>Descripción:</strong> ${aviso.descripcion}</p>
            <div>
                <img class="foto-small" src="${aviso.fotos[0].src}" alt="${aviso.fotos[0].alt}" style="width: 320px; height: 240px; cursor: pointer;">
            </div>
            <br>
            <button id="volver-listado">Volver al listado</button>
            <button id="volver-portada">Volver a la portada</button>
        `;

// Agrega 'event listeners' a los botones "Volver al listado" y "Volver a la portada".
        document.getElementById('volver-listado').addEventListener('click', () => {
            detalleAvisoDiv.style.display = 'none';
            listaAvisosDiv.style.display = 'block';
        });

        document.getElementById('volver-portada').addEventListener('click', () => {
            window.location.href = 'index.html';
        });

        // Agrega un 'event listener' para el clic en la foto pequeña.
        const fotoSmall = document.querySelector('.foto-small');
        fotoSmall.addEventListener('click', () => {
            // Crea un 'overlay' (superposición) para mostrar la imagen en grande.
            const overlay = document.createElement('div');
            overlay.className = 'overlay';
            overlay.innerHTML = `
                <img src="${aviso.fotos[0].src}" alt="${aviso.fotos[0].alt}" style="width: 800px; height: 600px; object-fit: contain;">
                <button id="cerrar-foto">Cerrar</button>
            `;
            document.body.appendChild(overlay);

            // Agrega un 'event listener' al botón para cerrar la superposición.
            document.getElementById('cerrar-foto').addEventListener('click', () => {
                document.body.removeChild(overlay);
            });
        });
    });
});
