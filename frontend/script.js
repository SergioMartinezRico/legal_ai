const API_URL = 'http://localhost:8000'

// --- FUNCIÓN 1: SUBIR DOCUMENTO ---
async function uploadDocument() {
  const fileInput = document.getElementById('pdfFile')
  const statusMsg = document.getElementById('statusMsg')
  const btnUpload = document.getElementById('btnUpload')
  const chatSection = document.getElementById('chatSection')

  if (fileInput.files.length === 0) {
    alert('⚠️ Por favor selecciona un PDF primero.')
    return
  }

  // UI: Mostrar carga
  btnUpload.disabled = true
  btnUpload.innerText = 'Procesando...'
  statusMsg.innerText = '⏳ Leyendo documento y vectorizando...'
  statusMsg.className = 'mt-3 text-sm font-medium text-blue-600 animate-pulse'

  const formData = new FormData()
  formData.append('file', fileInput.files[0])

  try {
    const response = await fetch(`${API_URL}/upload`, {
      method: 'POST',
      body: formData
    })

    const data = await response.json()

    if (response.ok) {
      // ÉXITO
      statusMsg.innerHTML =
        '✅ <b>Documento listo.</b> Ya puedes hacer preguntas.'
      statusMsg.className = 'mt-3 text-sm text-green-600'

      // Desbloquear chat visualmente
      chatSection.classList.remove(
        'opacity-50',
        'pointer-events-none',
        'blur-[1px]'
      )
      document.getElementById('questionInput').focus()
    } else {
      throw new Error(data.detail || 'Error desconocido')
    }
  } catch (error) {
    statusMsg.innerText = '❌ Error: ' + error.message
    statusMsg.className = 'mt-3 text-sm font-medium text-red-600'
  } finally {
    btnUpload.disabled = false
    btnUpload.innerText = 'Analizar PDF'
  }
}

// --- FUNCIÓN 2: PREGUNTAR ---
async function askQuestion() {
  const input = document.getElementById('questionInput')
  const btnAsk = document.getElementById('btnAsk')
  const responseContainer = document.getElementById('responseContainer')
  const responseText = document.getElementById('responseText')

  const question = input.value.trim()
  if (!question) return

  // UI: Preparar para respuesta
  btnAsk.disabled = true
  btnAsk.innerText = 'Pensando...'
  responseContainer.classList.add('hidden') // Ocultar anterior

  try {
    const response = await fetch(`${API_URL}/ask`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ query: question })
    })

    const data = await response.json()

    if (response.ok) {
      // Mostrar respuesta con efecto de escritura simple o directa
      responseContainer.classList.remove('hidden')
      // Convertir saltos de línea en <br> para que se lea bien
      responseText.innerHTML = data.answer.replace(/\n/g, '<br>')
    } else {
      alert('Error: ' + data.detail)
    }
  } catch (error) {
    alert('Error de conexión: ' + error.message)
  } finally {
    btnAsk.disabled = false
    btnAsk.innerText = 'Preguntar'
  }
}

// Permitir pulsar ENTER para enviar
function handleEnter(e) {
  if (e.key === 'Enter') askQuestion()
}
