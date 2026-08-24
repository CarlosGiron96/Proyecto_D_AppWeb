document.addEventListener("DOMContentLoaded", () => {
    
    // --- 1. COLECCIÓN DE DATOS EN MEMORIA (Base de datos simulada) ---
    const catalogoDatos = [
        {
            id: 101,
            nombre: "Cafetería El Gran Grano",
            tipo: "Café Arábigo (Loja)",
            descripcion: "Pedido prioritario de 5 quintales de café lavado de altura para distribución exclusiva de fin de mes comercial."
        },
        {
            id: 102,
            nombre: "Corporación Horeca",
            tipo: "Café Blend Tradicional (Manabí)",
            descripcion: "Sugerencia de empaque biodegradable hermético para los granos artesanales despachados a la costa del país."
        }
    ];

    // --- 2. CAPTURA DE NODOS ELEMENTALES DEL DOM ---
    const formulario = document.getElementById("formulario-dinamico");
    const inputNombre = document.getElementById("reg-nombre");
    const selectTipo = document.getElementById("reg-tipo");
    const areaDescripcion = document.getElementById("reg-descripcion");
    
    const contenedorLista = document.getElementById("lista-registros");
    const contadorHTML = document.getElementById("contador-registros");
    const alertaContenedor = document.getElementById("alerta-contenedor");
    const spinnerCarga = document.getElementById("spinner-carga");

    // Instancia nativa de Bootstrap Modal para control programático
    const modalBootstrap = new bootstrap.Modal(document.getElementById('modalDetalles'));

    // --- 3. LOGÍSITCA DE RENDERIZADO DINÁMICO (Semana 7) ---
    function renderizarCatalogo() {
        contenedorLista.innerHTML = "";

        // CONDICIÓN: Si el arreglo central carece de elementos
        if (catalogoDatos.length === 0) {
            const mensajeVacio = document.createElement("div");
            mensajeVacio.className = "col-12 animate-fade-in";
            mensajeVacio.innerHTML = `
                <div class="alert alert-warning text-center p-4 rounded-3 border-warning border-opacity-50" role="alert">
                    <i class="bi bi-exclamation-triangle fs-4 mb-2 d-block text-warning"></i>
                    <h6 class="fw-bold mb-1">Estructura de Datos Vacía</h6>
                    <p class="mb-0 small text-muted">No existen lotes registrados. Agregue uno nuevo usando el panel de inserción.</p>
                </div>
            `;
            contenedorLista.appendChild(mensajeVacio);
            contadorHTML.textContent = 0;
            return;
        }

        // BUCLE REPETITIVO: Iterar sobre la colección para armar el catálogo de Cards Bootstrap
        catalogoDatos.forEach((registro) => {
            const colDiv = document.createElement("div");
            colDiv.className = "col-sm-6 animate-fade-in";
            colDiv.innerHTML = `
                <div class="card h-100 border-0 bg-light p-2 shadow-sm rounded-3 border-start border-success border-3">
                    <div class="card-body d-flex flex-column justify-content-between">
                        <div>
                            <h6 class="fw-bold text-dark mb-1 text-truncate"><i class="bi bi-building"></i> ${registro.nombre}</h6>
                            <span class="badge bg-dark text-warning extra-small mb-3">${registro.tipo}</span>
                            <p class="card-text extra-small text-muted text-justify line-clamp">${registro.descripcion}</p>
                        </div>
                        <div class="row g-2 mt-2">
                            <div class="col-6">
                                <button class="btn btn-primary btn-sm w-100 fw-bold extra-small btn-detalles" data-id="${registro.id}">
                                    <i class="bi bi-eye"></i> Detalles
                                </button>
                            </div>
                            <div class="col-6">
                                <button class="btn btn-outline-danger btn-sm w-100 fw-bold extra-small btn-eliminar" data-id="${registro.id}">
                                    <i class="bi bi-trash"></i> Quitar
                                </button>
                            </div>
                        </div>
                    </div>
                </div>
            `;

            // Escuchadores internos integrados a los botones de la Card
            colDiv.querySelector(".btn-detalles").addEventListener("click", () => mostrarModalDetalles(registro.id));
            colDiv.querySelector(".btn-eliminar").addEventListener("click", () => eliminarRegistro(registro.id));

            contenedorLista.appendChild(colDiv);
        });

        contadorHTML.textContent = catalogoDatos.length;
    }

    // --- 4. ACCIONES INTERACTIVAS (Modal y Eliminación) ---
    function mostrarModalDetalles(id) {
        const item = catalogoDatos.find(r => r.id === id);
        if (item) {
            document.getElementById("modal-nombre").textContent = item.nombre;
            document.getElementById("modal-tipo").textContent = item.tipo;
            document.getElementById("modal-descripcion").textContent = item.descripcion;
            modalBootstrap.show(); // Despliega el modal de Bootstrap
        }
    }

    function eliminarRegistro(id) {
        const indice = catalogoDatos.findIndex(item => item.id === id);
        if (indice !== -1) {
            catalogoDatos.splice(indice, 1);
            renderizarCatalogo();
            mostrarAlertaGlobal("Registro removido del esquema analítico.", "danger");
        }
    }

    // --- 5. VALIDACIONES DINÁMICAS EN TIEMPO REAL (Semana 6) ---
    function validarNombre() {
        const valor = inputNombre.value.trim();
        return marcarEstado(inputNombre, (valor !== "" && valor.length >= 5));
    }

    function validarTipo() {
        return marcarEstado(selectTipo, (selectTipo.value !== ""));
    }

    function validarDescripcion() {
        const valor = areaDescripcion.value.trim();
        return marcarEstado(areaDescripcion, (valor !== "" && valor.length >= 15));
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

    inputNombre.addEventListener("input", validarNombre);
    inputNombre.addEventListener("blur", validarNombre);
    selectTipo.addEventListener("change", validarTipo);
    selectTipo.addEventListener("blur", validarTipo);
    areaDescripcion.addEventListener("input", validarDescripcion);
    areaDescripcion.addEventListener("blur", validarDescripcion);

    // --- 6. GESTIÓN DEL ENVIÓ (Manejo de Alertas y Spinner) ---
    formulario.addEventListener("submit", (evento) => {
        evento.preventDefault();

        const vNom = validarNombre();
        const vTip = validarTipo();
        const vDes = validarDescripcion();

        // Si existen campos erróneos, despliega Alerta Bootstrap de error
        if (!vNom || !vTip || !vDes) {
            mostrarAlertaGlobal("No se pudo registrar. Verifique las celdas en rojo.", "warning");
            return;
        }

        // Ocultar catálogo momentáneamente y mostrar Spinner Bootstrap simulando persistencia asíncrona
        contenedorLista.classList.add("d-none");
        spinnerCarga.classList.remove("d-none");

        setTimeout(() => {
            // Empujar nuevo objeto mapeado al arreglo
            catalogoDatos.push({
                id: Date.now(),
                nombre: inputNombre.value.trim(),
                tipo: selectTipo.value,
                descripcion: areaDescripcion.value.trim()
            });

            // Reestablecer estados visuales
            spinnerCarga.classList.add("d-none");
            contenedorLista.classList.remove("d-none");
            
            renderizarCatalogo();
            mostrarAlertaGlobal("¡Excelente Lote indexado con éxito a la colección de datos!", "success");

            formulario.reset();
            [inputNombre, selectTipo, areaDescripcion].forEach(el => el.classList.remove("is-valid", "is-invalid"));
        }, 800); // Demora intencional controlada para apreciar la animación de carga del spinner
    });

    function mostrarAlertaGlobal(mensaje, clase) {
        // Inyecta dinámicamente un componente Alert de Bootstrap autocerrable
        alertaContenedor.innerHTML = `
            <div class="alert alert-${clase} alert-dismissible fade show my-2 fw-semibold extra-small" role="alert">
                <i class="bi bi-info-circle-fill"></i> ${mensaje}
                <button type="button" class="btn-close" data-bs-dismiss="alert" aria-label="Close"></button>
            </div>
        `;
    }

    // Inicialización al arranque
    renderizarCatalogo();
});