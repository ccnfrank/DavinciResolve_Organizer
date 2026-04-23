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