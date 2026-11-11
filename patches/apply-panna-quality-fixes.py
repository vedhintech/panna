from pathlib import Path
nl = chr(10)
p = Path('src/main.js')
s = p.read_text()
old = '''    <div class="vbottom"><button class="vtool" data-v="edit">${I.edit}<span>${L('एडिट', 'Edit')}</span></button>
      <button class="vtool" data-v="sign">${I.sign}<span>${L('साइन', 'Sign')}</span></button>
      <button class="pchip" data-v="goto"><span id="pcur">1</span> / ${doc.numPages}</button>
      <button class="vtool" data-v="read">${I.speaker}<span>${L('सुनें', 'Listen')}</span></button>
      <button class="vtool" data-v="night" aria-pressed="${night}">${I.moon}<span>${L('रात', 'Night')}</span></button></div>`;'''
new = '''    <div class="vbottom"><button class="vtool" data-v="zoomout" aria-label="Zoom out"><b class="zglyph">−</b><span>Zoom out</span></button>
      <button class="vtool" data-v="zoomin" aria-label="Zoom in"><b class="zglyph">＋</b><span>Zoom in</span></button>
      <button class="vtool" data-v="edit">${I.edit}<span>${L('एडिट', 'Edit')}</span></button>
      <button class="pchip" data-v="goto"><span id="pcur">1</span> / ${doc.numPages}</button>
      <button class="vtool" data-v="sign">${I.sign}<span>${L('साइन', 'Sign')}</span></button>
      <button class="vtool" data-v="night" aria-pressed="${night}">${I.moon}<span>${L('रात', 'Night')}</span></button></div>`;'''
if old in s:
    s = s.replace(old, new, 1)
elif 'data-v="zoomout"' not in s:
    raise SystemExit('viewer toolbar template not found')
needle = "  if (a === 'close') popOverlay();" + nl
if "if (a === 'zoomin')" not in s:
    if needle not in s: raise SystemExit('viewer click handler not found')
    s = s.replace(needle, needle + "  if (a === 'zoomin') viewer?.setZoom(viewer.z + .25);" + nl + "  if (a === 'zoomout') viewer?.setZoom(viewer.z - .25);" + nl, 1)
p.write_text(s)

p = Path('src/style.css')
s = p.read_text()
needle = '.vtool[aria-pressed=true]{color:var(--gold)}'
if '.zglyph{' not in s:
    if needle not in s: raise SystemExit('viewer tool style not found')
    s = s.replace(needle, needle + nl + '.zglyph{font-size:23px;line-height:20px;font-weight:500}', 1)
p.write_text(s)

# App archive does not contain the outer repository's CI workflow file.
p = Path('tests/project-config.test.mjs')
if p.exists():
    s = p.read_text()
    s = s.replace("const workflow = await readFile(new URL('../.github/workflows/android-debug-apk.yml', import.meta.url), 'utf8');" + nl, '')
    start = s.find("test('Android cloud build disables OS auto-backup")
    end = s.find(nl + "test('offline OCR build copies", start)
    if start >= 0 and end >= 0:
        replacement = "test('Android app disables OS auto-backup', () => {" + nl + "  assert.match(manifest, /android:allowBackup=\"false\"/);" + nl + "});" + nl
        s = s[:start] + replacement + s[end+1:]
    p.write_text(s)
print('Applied viewer zoom controls and made source tests archive-safe.')
