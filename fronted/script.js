const API_URL = "http://recigana-env.eba-hzu6u3jk.us-east-2.elasticbeanstalk.com";

document.getElementById("form-usuario").addEventListener("submit", async function(evento) {
  evento.preventDefault();

  const datos = {
    nombre: document.getElementById("nombre").value,
    email: document.getElementById("email").value,
    ciudad: document.getElementById("ciudad").value
  };

  try {
    const respuesta = await fetch(`${API_URL}/usuarios/`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(datos)
    });

    const resultado = await respuesta.json();
    const div = document.getElementById("resultado-usuario");

    if (respuesta.ok) {
      div.innerHTML = `<p class="exito">✅ Usuario registrado: ${resultado.nombre}</p>`;
      document.getElementById("form-usuario").reset();
      cargarUsuarios();
    } else {
      div.innerHTML = `<p class="error">❌ Error: ${resultado.detail}</p>`;
    }

  } catch (error) {
    document.getElementById("resultado-usuario").innerHTML =
      `<p class="error">❌ No se pudo conectar al servidor</p>`;
  }
});

async function cargarUsuarios() {
  try {
    const respuesta = await fetch(`${API_URL}/usuarios/`);
    const usuarios = await respuesta.json();
    const cuerpo = document.getElementById("cuerpo-tabla");
    cuerpo.innerHTML = "";

    usuarios.forEach(usuario => {
      const fila = document.createElement("tr");
      fila.innerHTML = `
        <td>${usuario.id}</td>
        <td>${usuario.nombre}</td>
        <td>${usuario.email}</td>
        <td>${usuario.ciudad}</td>
        <td>${usuario.puntos_totales} pts</td>
      `;
      cuerpo.appendChild(fila);
    });

  } catch (error) {
    console.error("Error cargando usuarios:", error);
  }
}

cargarUsuarios();