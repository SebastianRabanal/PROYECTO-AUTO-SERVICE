// Catálogo base para los cálculos visuales en el frontend
const catalogo = {
    'prod-hamburguesa': { nombre: 'Hamburguesa Clásica', precioBase: 15.00 },
    'prod-pizza': { nombre: 'Pizza Personal', precioBase: 12.00 },
    'prod-cafe': { nombre: 'Café Pasado', precioBase: 6.00 }
};

const preciosExtras = {
    'papas': 4.00,
    'queso': 2.50
};

// Estado del pedido
let ticketPedido = [];
let productoActualSeleccionado = null;
let totalPagar = 0;

// Referencias al DOM
const zonaPersonalizacion = document.getElementById('zona-personalizacion');
const listaTicket = document.getElementById('lista-ticket');
const montoTotalDOM = document.getElementById('monto-total');
const btnAgregarTicket = document.querySelector('.btn-agregar-ticket');
const btnGenerarVoucher = document.getElementById('btn-generar-voucher');

// 1. Lógica para seleccionar un producto y mostrar personalización
document.querySelectorAll('.btn-seleccionar').forEach(boton => {
    boton.addEventListener('click', (e) => {
        // Obtener el ID del producto clickeado (el div padre)
        const tarjeta = e.target.closest('.tarjeta-producto');
        productoActualSeleccionado = catalogo[tarjeta.id];
        productoActualSeleccionado.idHtml = tarjeta.id;

        // Actualizar título de la zona de personalización
        zonaPersonalizacion.querySelector('h3').textContent = `Personaliza tu ${productoActualSeleccionado.nombre}`;
        
        // Desmarcar checkboxes anteriores
        document.querySelectorAll('input[type="checkbox"]').forEach(cb => cb.checked = false);

        // Mostrar la zona de personalización
        zonaPersonalizacion.classList.remove('oculto');
    });
});

// 2. Lógica para agregar el producto personalizado al ticket
btnAgregarTicket.addEventListener('click', () => {
    if (!productoActualSeleccionado) return;

    let subtotal = productoActualSeleccionado.precioBase;
    let cremasSeleccionadas = [];
    let extrasSeleccionados = [];

    // Capturar cremas (Gratis)
    document.querySelectorAll('input[name="crema"]:checked').forEach(cb => {
        cremasSeleccionadas.push(cb.parentNode.textContent.trim());
    });

    // Capturar extras (Con costo)
    document.querySelectorAll('input[name="extra"]:checked').forEach(cb => {
        extrasSeleccionados.push(cb.parentNode.textContent.trim());
        subtotal += preciosExtras[cb.value];
    });

    // Crear objeto del ítem para el ticket
    const nuevoItem = {
        nombre: productoActualSeleccionado.nombre,
        cremas: cremasSeleccionadas,
        extras: extrasSeleccionados,
        subtotal: subtotal
    };

    ticketPedido.push(nuevoItem);
    actualizarTicketDOM();

    // Ocultar personalización tras agregar
    zonaPersonalizacion.classList.add('oculto');
    productoActualSeleccionado = null;
});

// 3. Lógica para actualizar la vista del ticket en la derecha
function actualizarTicketDOM() {
    listaTicket.innerHTML = ''; // Limpiar lista
    totalPagar = 0;

    ticketPedido.forEach((item, index) => {
        totalPagar += item.subtotal;

        const divItem = document.createElement('div');
        divItem.className = 'item-ticket';
        
        let htmlDetalles = '';
        if (item.cremas.length > 0) htmlDetalles += `<p class="detalle-item">- ${item.cremas.join(', ')}</p>`;
        if (item.extras.length > 0) htmlDetalles += `<p class="detalle-item">- ${item.extras.join(', ')}</p>`;

        divItem.innerHTML = `
            <p class="nombre-item">1x ${item.nombre}</p>
            ${htmlDetalles}
            <p class="precio-item">S/ ${item.subtotal.toFixed(2)}</p>
        `;
        listaTicket.appendChild(divItem);
    });

    montoTotalDOM.textContent = `S/ ${totalPagar.toFixed(2)}`;
}

// 4. Lógica para procesar el pago y enviar al backend (Python)
btnGenerarVoucher.addEventListener('click', () => {
    if (ticketPedido.length === 0) {
        alert('El ticket está vacío. Selecciona un producto.');
        return;
    }

    const metodoPago = document.querySelector('input[name="pago"]:checked');
    if (!metodoPago) {
        alert('Por favor, selecciona un método de pago.');
        return;
    }

    // Estructurar el JSON que se enviará al Backend
    const payloadBackend = {
        fecha: new Date().toISOString(),
        metodo_pago: metodoPago.value,
        total_pagado: totalPagar,
        detalle_pedido: ticketPedido
    };

    // Simulación del envío al backend
    console.log("Datos listos para enviar a Python:", JSON.stringify(payloadBackend, null, 2));
    
    alert(`¡Pago procesado con ${metodoPago.value.toUpperCase()}!\nTotal: S/ ${totalPagar.toFixed(2)}\nGenerando voucher...`);
    
    // Limpiar el sistema para el siguiente cliente
    ticketPedido = [];
    actualizarTicketDOM();
    document.querySelector('input[name="pago"]:checked').checked = false;
});

// Limpiar el ticket de ejemplo del HTML al cargar la página
document.addEventListener('DOMContentLoaded', () => {
    listaTicket.innerHTML = ''; 
    montoTotalDOM.textContent = 'S/ 0.00';
});