from pathlib import Path
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
if old not in s: raise SystemExit('viewer toolbar template not found')
s = s.replace(old, new, 1)
needle = "  if (a === 'close') popOverlay();\\n"
if needle not in s: raise SystemExit('viewer click handler not found')
s = s.replace(needle, needle + "  if (a === 'zoomin') viewer?.setZoom(viewer.z + .25);\\n  if (a === 'zoomout') viewer?.setZoom(viewer.z - .25);\\n", 1)
p.write_text(s)

p = Path('src/style.css')
s = p.read_text()
needle = '.vtool[aria-pressed=true]{color:var(--gold)}'
if needle not in s: raise SystemExit('viewer tool style not found')
p.write_text(s.replace(needle, needle + '\\n.zglyph{font-size:23px;line-height:20px;font-weight:500}', 1))

# The uploaded source archive intentionally contains app source, not repository CI files.
# Keep project tests independent of a workflow file that only exists in the outer repo.
p = Path('tests/project-config.test.mjs')
if p.exists():
    s = p.read_text()
    s = s.replace("const workflow = await readFile(new URL('../.github/workflows/android-debug-apk.yml', import.meta.url), 'utf8');\\n", '')
    start = s.find("test('Android cloud build disables OS auto-backup")
    end = s.find("\\ntest('offline OCR build copies", start)
    if start >= 0 and end >= 0:
        s = s[:start] + "test('Android app disables OS auto-backup', () => {\\n  assert.match(manifest, /android:allowBackup=\"false\"/);\\n});\\n" + s[end+1:]
    p.write_text(s)
