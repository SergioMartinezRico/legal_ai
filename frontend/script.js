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
      responseContainer.classList.remove('hidden')

      // 1. Renderizar texto (Markdown)
      responseText.innerHTML = marked.parse(data.answer)

      // 2. Renderizar Fuentes (NUEVO)
      // Borramos fuentes anteriores si las hubiera
      const existingSources = document.getElementById('sourcesBox')
      if (existingSources) existingSources.remove()

      // Si hay fuentes, las mostramos
      if (data.sources && data.sources.length > 0) {
        // Quitamos duplicados (Set) y ordenamos
        const uniquePages = [...new Set(data.sources)].sort((a, b) => a - b)

        // Las páginas en PDF suelen empezar en 0 internamente, sumamos 1 para que sea humano
        const pagesHtml = uniquePages
          .map(
            (p) =>
              `<span class="bg-indigo-100 text-indigo-800 text-xs font-semibold mr-2 px-2.5 py-0.5 rounded border border-indigo-200">Pág. ${
                p + 1
              }</span>`
          )
          .join('')

        const sourcesDiv = document.createElement('div')
        sourcesDiv.id = 'sourcesBox'
        sourcesDiv.className = 'mt-4 pt-4 border-t border-slate-200'
        sourcesDiv.innerHTML = `
                    <p class="text-xs text-slate-500 mb-2 font-bold uppercase">Fuentes consultadas:</p>
                    <div class="flex flex-wrap gap-2">${pagesHtml}</div>
                `

        responseText.parentElement.appendChild(sourcesDiv)
      }
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
