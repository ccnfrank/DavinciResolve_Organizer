#!/usr/bin/env python3
"""
Resolve Organizer — abre no navegador, sem dependências externas.
Uso: python3 resolve_organizer.py
"""

import http.server
import json
import os
import threading
import webbrowser

SUBFOLDERS = ["Footage", "Audio", "Export", "Graphics", "Project"]
PORT = 8765

HTML = """<!DOCTYPE html>
<html lang="pt-BR">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Resolve Organizer</title>
<style>
  @import url('https://fonts.googleapis.com/css2?family=IBM+Plex+Mono:wght@400;600;700&display=swap');

  *, *::before, *::after { box-sizing: border-box; margin: 0; padding: 0; }

  :root {
    --bg: #141414;
    --surface: #1e1e1e;
    --border: #2e2e2e;
    --accent: #e8a020;
    --accent-dim: #a06e10;
    --text: #efefef;
    --dim: #666;
    --success: #4caf7d;
    --error: #e05a5a;
  }

  body {
    font-family: 'IBM Plex Mono', monospace;
    background: var(--bg);
    color: var(--text);
    min-height: 100vh;
    display: flex;
    align-items: center;
    justify-content: center;
    padding: 24px;
  }

  .card {
    width: 100%;
    max-width: 480px;
    background: var(--surface);
    border: 1px solid var(--border);
    border-top: 3px solid var(--accent);
  }

  .card-header {
    padding: 28px 32px 22px;
    border-bottom: 1px solid var(--border);
  }

  .card-header h1 {
    font-size: 22px;
    font-weight: 700;
    color: var(--accent);
    letter-spacing: 0.12em;
  }

  .card-header p {
    font-size: 11px;
    color: var(--dim);
    margin-top: 4px;
    letter-spacing: 0.05em;
  }

  .card-body {
    padding: 28px 32px;
    display: flex;
    flex-direction: column;
    gap: 20px;
  }

  .field label {
    display: block;
    font-size: 9px;
    font-weight: 700;
    color: var(--dim);
    letter-spacing: 0.12em;
    margin-bottom: 8px;
  }

  .field input {
    width: 100%;
    background: var(--bg);
    border: 1px solid var(--border);
    color: var(--text);
    font-family: 'IBM Plex Mono', monospace;
    font-size: 13px;
    padding: 11px 14px;
    outline: none;
    transition: border-color 0.15s;
  }

  .field input:focus { border-color: var(--accent); }
  .field input::placeholder { color: var(--dim); }

  .preview {
    background: var(--bg);
    border: 1px solid var(--border);
    padding: 16px;
  }

  .preview-title {
    font-size: 9px;
    font-weight: 700;
    color: var(--dim);
    letter-spacing: 0.12em;
    margin-bottom: 12px;
  }

  .preview-tree { font-size: 12px; line-height: 2; }
  .preview-tree .project-name { color: var(--text); font-weight: 600; }
  .preview-tree .folder { color: var(--accent); padding-left: 16px; }

  .btn {
    width: 100%;
    background: var(--accent);
    color: #111;
    border: none;
    font-family: 'IBM Plex Mono', monospace;
    font-size: 12px;
    font-weight: 700;
    letter-spacing: 0.1em;
    padding: 14px;
    cursor: pointer;
    transition: background 0.15s;
  }

  .btn:hover { background: #f0b84a; }
  .btn:active { background: var(--accent-dim); }

  .status {
    font-size: 11px;
    text-align: center;
    min-height: 18px;
    letter-spacing: 0.04em;
  }

  .status.success { color: var(--success); }
  .status.error   { color: var(--error); }

  .card-footer {
    padding: 14px 32px;
    border-top: 1px solid var(--border);
    font-size: 9px;
    color: var(--dim);
    text-align: center;
    letter-spacing: 0.06em;
  }
</style>
</head>
<body>
<div class="card">
  <div class="card-header">
    <h1>RESOLVE</h1>
    <p>Project Organizer</p>
  </div>

  <div class="card-body">
    <div class="field">
      <label>NOME DO PROJETO</label>
      <input type="text" id="projectName" placeholder="Ex: Campanha_ClienteX" autofocus>
    </div>

    <div class="field">
      <label>CAMINHO DESTINO</label>
      <input type="text" id="destPath" placeholder="Ex: /Users/christian/Projetos">
    </div>

    <div class="preview">
      <div class="preview-title">ESTRUTURA QUE SERÁ CRIADA</div>
      <div class="preview-tree" id="tree">
        <div class="project-name">📁 Nome_do_Projeto/</div>
        <div class="folder">├─ Footage/</div>
        <div class="folder">├─ Audio/</div>
        <div class="folder">├─ Export/</div>
        <div class="folder">├─ Graphics/</div>
        <div class="folder">└─ Project/</div>
      </div>
    </div>

    <button class="btn" onclick="criar()">CRIAR PROJETO</button>
    <div class="status" id="status"></div>
  </div>

  <div class="card-footer">localhost:8765 — feche o terminal para encerrar</div>
</div>

<script>
  const nameInput = document.getElementById('projectName');

  nameInput.addEventListener('input', () => {
    const n = nameInput.value.trim() || 'Nome_do_Projeto';
    document.getElementById('tree').innerHTML = `
      <div class="project-name">📁 ${n}/</div>
      <div class="folder">├─ Footage/</div>
      <div class="folder">├─ Audio/</div>
      <div class="folder">├─ Export/</div>
      <div class="folder">├─ Graphics/</div>
      <div class="folder">└─ Project/</div>
    `;
  });

  async function criar() {
    const name = document.getElementById('projectName').value.trim();
    const dest = document.getElementById('destPath').value.trim();

    if (!name) { setStatus('⚠ Digite o nome do projeto.', 'error'); return; }
    if (!dest) { setStatus('⚠ Digite o caminho de destino.', 'error'); return; }

    setStatus('…', '');

    const res = await fetch('/criar', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ name, dest })
    });

    const data = await res.json();
    if (data.ok) {
      setStatus('✓ ' + data.msg, 'success');
      document.getElementById('projectName').value = '';
      document.getElementById('tree').innerHTML = `
        <div class="project-name">📁 Nome_do_Projeto/</div>
        <div class="folder">├─ Footage/</div>
        <div class="folder">├─ Audio/</div>
        <div class="folder">├─ Export/</div>
        <div class="folder">├─ Graphics/</div>
        <div class="folder">└─ Project/</div>
      `;
    } else {
      setStatus('⚠ ' + data.msg, 'error');
    }
  }

  function setStatus(msg, cls) {
    const s = document.getElementById('status');
    s.textContent = msg;
    s.className = 'status ' + (cls || '');
  }

  document.addEventListener('keydown', e => { if (e.key === 'Enter') criar(); });
</script>
</body>
</html>
"""


class Handler(http.server.BaseHTTPRequestHandler):
    def log_message(self, format, *args):
        pass  # silencia logs no terminal

    def do_GET(self):
        self.send_response(200)
        self.send_header("Content-Type", "text/html; charset=utf-8")
        self.end_headers()
        self.wfile.write(HTML.encode())

    def do_POST(self):
        if self.path != "/criar":
            self.send_response(404)
            self.end_headers()
            return

        length = int(self.headers.get("Content-Length", 0))
        body = json.loads(self.rfile.read(length))

        name = body.get("name", "").strip()
        dest = body.get("dest", "").strip()
        result = {"ok": False, "msg": ""}

        if not name:
            result["msg"] = "Nome do projeto está vazio."
        elif not dest:
            result["msg"] = "Caminho de destino está vazio."
        elif not os.path.isdir(dest):
            result["msg"] = f"Diretório não encontrado: {dest}"
        else:
            project_path = os.path.join(dest, name)
            if os.path.exists(project_path):
                result["msg"] = f"Já existe uma pasta chamada '{name}' nesse destino."
            else:
                try:
                    os.makedirs(project_path)
                    for folder in SUBFOLDERS:
                        os.makedirs(os.path.join(project_path, folder))
                    result["ok"] = True
                    result["msg"] = f"Projeto '{name}' criado em {dest}"
                except Exception as e:
                    result["msg"] = str(e)

        self.send_response(200)
        self.send_header("Content-Type", "application/json")
        self.end_headers()
        self.wfile.write(json.dumps(result).encode())


def main():
    server = http.server.HTTPServer(("localhost", PORT), Handler)
    url = f"http://localhost:{PORT}"
    print(f"✓ Resolve Organizer rodando em {url}")
    print("  Abrindo navegador automaticamente...")
    print("  Para encerrar: Ctrl+C\n")
    threading.Timer(0.5, lambda: webbrowser.open(url)).start()
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\n✓ Encerrado.")


if __name__ == "__main__":
    main()
