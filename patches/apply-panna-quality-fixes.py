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

# Apply the Panna premium navy/blue visual system while preserving layout and behavior.
p = Path('src/style.css')
s = p.read_text()
palette = {
    '--paper:#F4F7F5': '--paper:#F4F7FC',
    '--surface-2:#E9F0EC': '--surface-2:#EAF0F8',
    '--ink:#13221C': '--ink:#142238',
    '--ink-2:#4B5E56': '--ink-2:#526176',
    '--line:#D5E0DA': '--line:#D8E0EC',
    '--emerald:#0B7A55': '--emerald:#155EEF',
    '--emerald-deep:#064532': '--emerald-deep:#123B78',
    '--tint:#DDEFE6': '--tint:#E8F0FF',
    '--paper:#0C1512': '--paper:#0B1220',
    '--surface:#15211C': '--surface:#111C2F',
    '--surface-2:#1C2B25': '--surface-2:#1B2A43',
    '--ink:#E4EEE9': '--ink:#EAF0FA',
    '--ink-2:#9DB2A8': '--ink-2:#A8B6CC',
    '--line:#25362F': '--line:#263650',
    '--emerald:#3FC496': '--emerald:#6EA0FF',
    '--emerald-deep:#1E7A5A': '--emerald-deep:#2D5FC0',
    '--tint:#163A2C': '--tint:#1A3158',
}
for old, new in palette.items():
    s = s.replace(old, new)
p.write_text(s)

print('Applied viewer zoom controls and made source tests archive-safe.')
