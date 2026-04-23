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
