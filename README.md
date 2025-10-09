# =============================================================
# 2️⃣ CÓMO CLONAR EL REPOSITORIO (CADA COMPAÑERO)
# =============================================================
# Una vez aceptada la invitación, cada integrante debe ejecutar:
git clone https://github.com/<tuUsuario>/<nombreDelRepositorio>.git

# Entrar a la carpeta descargada:
cd <nombreDelRepositorio>

# Verificar que Git funciona correctamente:
git status

# =============================================================
# 3️⃣ CREAR UNA NUEVA RAMA PARA TRABAJAR
# =============================================================
# Cada miembro del equipo debe trabajar en su propia rama.
# Esto evita que el código principal (main) se dañe.
git checkout -b rama-nombre

# Ejemplo:
git checkout -b rama-fabio

# =============================================================
# 4️⃣ GUARDAR Y SUBIR CAMBIOS
# =============================================================
# Después de hacer modificaciones en el proyecto:
git add .
git commit -m "Descripción de los cambios realizados"
git push origin rama-nombre

# Esto subirá la rama del integrante a GitHub sin afectar main.

# =============================================================
# 5️⃣ ACTUALIZAR SU PROYECTO CON LOS CAMBIOS DEL EQUIPO
# =============================================================
# Antes de seguir trabajando, cada integrante debe actualizar su copia:
git pull origin main

# (Esto descarga los últimos cambios que se hayan fusionado en la rama principal)

# =============================================================
# 6️⃣ HACER UN PULL REQUEST (SOLICITUD DE FUSIÓN)
# =============================================================
# Cuando un integrante termina su parte:
# 1. Entra al repositorio en GitHub.
# 2. Ve a la pestaña: Pull Requests → New Pull Request.
# 3. Selecciona su rama (rama-nombre) y compárala con “main”.
# 4. Crea el Pull Request.
# 5. El líder revisa y aprueba los cambios.

# =============================================================
# 7️⃣ DESCARGAR NUEVOS CAMBIOS DESPUÉS DE UNA FUSIÓN
# =============================================================
# Una vez fusionado un Pull Request, todos deben actualizar su proyecto:
git pull origin main

# Así todos mantienen el mismo código actualizado.
