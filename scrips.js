document.addEventListener("DOMContentLoaded", () => {
    
    // --- 1. BASE DE DATOS DE SIFRADO SIMULADA (Arreglo de Objetos) ---
    // Datos cargados por defecto para evitar repetir bloques manuales en el HTML
    const catalogoDatos = [
        {
            id: 1,
            nombre: "Cafetería El Gran Grano",
            tipo: "Café Arábigo (Loja)",
            descripcion: "Pedido prioritario de 5 quintales de café lavado de altura para distribución exclusiva de fin de mes."
        },
        {
            id: 2,
            nombre: "Corporación Horeca",
            tipo: "Café Blend Tradicional (Manabí)",
            descripcion: "Sugerencia de empaque biodegradable para los granos artesanales despachados a la costa del país."
        }
    ];

    // --- 2. ELEMENTOS DE CONTROL DEL DOM ---
    const formulario = document.getElementById("formulario-dinamico");
    const inputNombre = document.getElementById("reg-nombre");
    const selectTipo = document.getElementById("reg-tipo");
    const areaDescripcion = document.getElementById("reg-descripcion");
    
    const contenedorLista = document.getElementById("lista-registros");
    const contadorHTML = document.getElementById("contador-registros");
    const alertaContenedor = document.getElementById("alerta-contenedor");

    // --- 3. FUNCIONES DE RENDERIZADO MODULAR (Estructura Repetitiva y Condicional) ---
    
    function renderizarCatalogo() {
        // Limpiar contenedor para evitar duplicaciones
        contenedorLista.innerHTML = "";

        // IMPLEMENTACIÓN DE CONDICIÓN: Si no existen registros en el arreglo
        if (catalogoDatos.length === 0) {
            const mensajeVacio = document.createElement("div");
            mensajeVacio.className = "col-12 animate-fade-in";
            mensajeVacio.innerHTML = `
                <div class="alert alert-warning text-center p-4 rounded border border-warning" role="alert">
                    <h5 class="fw-bold mb-1">⚠️ Sin registros en el sistema</h5>
                    <p class="mb-0 small">El almacén de datos conceptual está vacío. Inserte nueva información usando el formulario superior.</p>
                </div>
            `;
            contenedorLista.appendChild(mensajeVacio);
            actualizarContadorUI(0);
            return;
        }

        // IMPLEMENTACIÓN DE ESTRUCTURA REPETITIVA: Recorrer arreglo con forEach
        catalogoDatos.forEach((registro) => {
            const colDiv = document.createElement("div");
            colDiv.className = "col-md-6 animate-fade-in";

            colDiv.innerHTML = `
                <div class="card border-start border-success border-3 h-100 p-3 shadow-sm">
                    <div class="card-body d-flex flex-column justify-content-between">
                        <div>
                            <h5 class="card-title fw-bold text-dark mb-1">🏢 ${registro.nombre}</h5>
                            <span class="badge bg-secondary mb-3">${registro.tipo}</span>
                            <p class="card-text small text-muted text-justify">${registro.descripcion}</p>
                        </div>
                        <button class="btn btn-outline-danger btn-sm w-100 mt-3 fw-bold btn-eliminar" data-id="${registro.id}">
                            🗑️ Eliminar Registro
                        </button>
                    </div>
                </div>
            `;

            // Asignación del evento Click para eliminar registro específico
            colDiv.querySelector(".btn-eliminar").addEventListener("click", (e) => {
                const idAEliminar = parseInt(e.target.getAttribute("data-id"));
                eliminarRegistro(idAEliminar);
            });

            contenedorLista.appendChild(colDiv);
        });

        actualizarContadorUI(catalogoDatos.length);
    }

    function eliminarRegistro(id) {
        // Buscar índice del objeto dentro del arreglo
        const indice = catalogoDatos.findIndex(item => item.id === id);
        if (indice !== -1) {
            catalogoDatos.splice(indice, 1); // Quitar del arreglo
            renderizarCatalogo(); // Re-renderizar colección actualizada
            mostrarAlertaGlobal("Registro eliminado de la colección interna.", "warning");
        }
    }

    function actualizarContadorUI(total) {
        contadorHTML.textContent = total;
    }

    // --- 4. CONSERVACIÓN DE VALIDACIONES DINÁMICAS (Semana 6) ---
    
    function validarNombre() {
        const valor = inputNombre.value.trim();
        if (valor === "" || valor.length < 5) { return marcarEstado(inputNombre, false); }
        return marcarEstado(inputNombre, true);
    }

    function validarTipo() {
        if (selectTipo.value === "") { return marcarEstado(selectTipo, false); }
        return marcarEstado(selectTipo, true);
    }

    function validarDescripcion() {
        const valor = areaDescripcion.value.trim();
        if (valor === "" || valor.length < 15) { return marcarEstado(areaDescripcion, false); }
        return marcarEstado(areaDescripcion, true);
    }

    function marcarEstado(elemento, esValido) {
        if (esValido) {
            elemento.classList.remove("is-invalid");
            elemento.classList.add("is-valid");
            return true;
        } else {
            elemento.classList.remove("is-valid");
            elemento.classList.add("is-invalid");
            return false;
        }
    }

    function limpiarClasesValidacion(elemento) {
        elemento.classList.remove("is-valid", "is-invalid");
    }

    // Escucha en tiempo real mediante addEventListener
    inputNombre.addEventListener("input", validarNombre);
    inputNombre.addEventListener("blur", validarNombre);
    selectTipo.addEventListener("change", validarTipo);
    selectTipo.addEventListener("blur", validarTipo);
    areaDescripcion.addEventListener("input", validarDescripcion);
    areaDescripcion.addEventListener("blur", validarDescripcion);

    // --- 5. MANEJO DEL EVENTO SUBMIT (Inserción en Arreglo) ---
    formulario.addEventListener("submit", (evento) => {
        evento.preventDefault(); // Evita recarga de página

        const vNom = validarNombre();
        const vTip = validarTipo();
        const vDes = validarDescripcion();

        // Control estricto de ingreso
        if (!vNom || !vTip || !vDes) {
            mostrarAlertaGlobal("No se pudo registrar. Corrija los campos marcados en rojo.", "danger");
            return;
        }

        // Crear un nuevo objeto representando el registro ingresado
        const nuevoRegistro = {
            id: Date.now(), // Genera ID único basado en tiempo
            nombre: inputNombre.value.trim(),
            tipo: selectTipo.value,
            descripcion: areaDescripcion.value.trim()
        };

        // Adicionar el objeto al arreglo central de datos
        catalogoDatos.push(nuevoRegistro);
        
        // Ejecutar re-renderizado completo de la sección de datos
        renderizarCatalogo();

        mostrarAlertaGlobal("¡Lote agregado con éxito a la colección de datos!", "success");

        // Limpieza de campos
        formulario.reset();
        limpiarClasesValidacion(inputNombre);
        limpiarClasesValidacion(selectTipo);
        limpiarClasesValidacion(areaDescripcion);
    });

    function mostrarAlertaGlobal(mensaje, clase) {
        alertaContenedor.innerHTML = "";
        const alertDiv = document.createElement("div");
        alertDiv.className = `alert alert-${clase} alert-dismissible fade show my-2 fw-bold small`;
        alertDiv.role = "alert";
        alertDiv.textContent = mensaje;
        alertaContenedor.appendChild(alertDiv);
    }

    // --- INTERRUPTOR DE ARRANQUE INICIAL ---
    // Carga los datos por defecto al abrir la aplicación
    renderizarCatalogo();
});