const fs = require('fs');
const logic = fs.readFileSync('part2_logic.html', 'utf8');   // <script id="logic"> ... </script>
const p1 = fs.readFileSync('part1.html', 'utf8');
const p3 = fs.readFileSync('part3.html', 'utf8');
const art = p1 + '\n' + logic + '\n' + p3;
fs.writeFileSync('kkeutmal.html', art);           // Claude artifact
const head = (extra) => '<!doctype html><html lang="ko"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1,viewport-fit=cover,interactive-widget=resizes-content"><meta name="theme-color" content="#0D1A1D"><style>:root{color-scheme:light;padding-top:env(safe-area-inset-top,0px);padding-bottom:env(safe-area-inset-bottom,0px)}body{margin:0;font:14px system-ui}[hidden]{display:none!important}</style>' + (extra || '') + '</head><body>';
fs.writeFileSync('끝말잇기.html', head() + art + '</body></html>');   // phone browser file
// Android app: native.js must load before the game script
fs.mkdirSync('kkeutmal-app/www', { recursive: true });
fs.writeFileSync('kkeutmal-app/www/index.html', head('<script src="native.js"></script>') + art + '</body></html>');
