/*
 * Vizualizator 3D — WebGL2, fără nicio librărie externă.
 *
 * Încarcă fişiere .glb exportate din Blender (doar POSITION + indici, materiale
 * PBR metallic-roughness cu culori constante) şi le desenează într-un canvas
 * rotibil cu mouse-ul sau cu degetul.
 *
 * Modelul se încarcă abia când blocul intră în ecran. Dacă browserul nu are
 * WebGL2, rămâne poza de rezervă din <img>.
 *
 * Markup aşteptat:
 *   <div class="viz3d" data-viz3d
 *        data-stari='[{"eticheta":"…","fisier":"…glb"}, …]'
 *        data-eticheta="descriere pentru cititoarele de ecran">
 *     <canvas></canvas>
 *     <img src="…poster.jpg" alt="…">   ← rezerva
 *   </div>
 */
(function () {
  'use strict';

  /* ═══════════════════ 1. citirea fişierului GLB ═══════════════════ */

  var MAGIC_GLB  = 0x46546C67; // "glTF"
  var CHUNK_JSON = 0x4E4F534A; // "JSON"
  var CHUNK_BIN  = 0x004E4942; // "BIN\0"

  var MARIME_COMPONENTA = { 5120: 1, 5121: 1, 5122: 2, 5123: 2, 5125: 4, 5126: 4 };
  var NR_COMPONENTE     = { SCALAR: 1, VEC2: 2, VEC3: 3, VEC4: 4, MAT4: 16 };
  var CONSTRUCTOR       = {
    5120: Int8Array, 5121: Uint8Array, 5122: Int16Array,
    5123: Uint16Array, 5125: Uint32Array, 5126: Float32Array
  };

  function citesteGLB(arrayBuffer) {
    var dv = new DataView(arrayBuffer);
    if (dv.getUint32(0, true) !== MAGIC_GLB) throw new Error('nu e fişier GLB');

    var lungimeTotala = dv.getUint32(8, true);
    var json = null, bin = null;
    var pozitie = 12;

    while (pozitie + 8 <= lungimeTotala && pozitie + 8 <= arrayBuffer.byteLength) {
      var lungime = dv.getUint32(pozitie, true);
      var tip     = dv.getUint32(pozitie + 4, true);
      var start   = pozitie + 8;
      if (tip === CHUNK_JSON) {
        json = JSON.parse(new TextDecoder('utf-8').decode(
          new Uint8Array(arrayBuffer, start, lungime)));
      } else if (tip === CHUNK_BIN) {
        bin = { offset: start, length: lungime };
      }
      pozitie = start + lungime + ((4 - (lungime % 4)) % 4); // aliniere la 4 octeţi
    }
    if (!json) throw new Error('GLB fără bloc JSON');
    return { json: json, bin: bin, buffer: arrayBuffer };
  }

  // scoate datele unui accessor ca TypedArray, tratând şi byteStride
  function citesteAccessor(glb, index) {
    var acc = glb.json.accessors[index];
    var nrComp = NR_COMPONENTE[acc.type];
    var Ctor   = CONSTRUCTOR[acc.componentType];
    var total  = acc.count * nrComp;

    if (acc.bufferView === undefined) return new Ctor(total); // umplut cu zerouri

    var bv     = glb.json.bufferViews[acc.bufferView];
    var baza   = glb.bin.offset + (bv.byteOffset || 0) + (acc.byteOffset || 0);
    var octet  = MARIME_COMPONENTA[acc.componentType];
    var stride = bv.byteStride || 0;

    if (!stride || stride === octet * nrComp) {
      return new Ctor(glb.buffer, baza, total); // strâns împachetat
    }
    var iesire = new Ctor(total); // întreţesut: îl desfac element cu element
    var dv = new DataView(glb.buffer);
    var citeste = {
      5120: dv.getInt8, 5121: dv.getUint8, 5122: dv.getInt16,
      5123: dv.getUint16, 5125: dv.getUint32, 5126: dv.getFloat32
    }[acc.componentType];
    for (var i = 0; i < acc.count; i++) {
      for (var c = 0; c < nrComp; c++) {
        iesire[i * nrComp + c] = citeste.call(dv, baza + i * stride + c * octet, true);
      }
    }
    return iesire;
  }

  /* ═══════════════════ 2. matrice 4×4 ═══════════════════ */

  function matUnitate() {
    return new Float32Array([1,0,0,0, 0,1,0,0, 0,0,1,0, 0,0,0,1]);
  }

  function matInmulteste(a, b) { // a·b, coloană-major
    var r = new Float32Array(16);
    for (var i = 0; i < 4; i++) {
      for (var j = 0; j < 4; j++) {
        r[i * 4 + j] = a[j] * b[i * 4] + a[4 + j] * b[i * 4 + 1] +
                       a[8 + j] * b[i * 4 + 2] + a[12 + j] * b[i * 4 + 3];
      }
    }
    return r;
  }

  function matDinTRS(t, r, s) {
    var x=r[0], y=r[1], z=r[2], w=r[3];
    var x2=x+x, y2=y+y, z2=z+z;
    var xx=x*x2, xy=x*y2, xz=x*z2, yy=y*y2, yz=y*z2, zz=z*z2;
    var wx=w*x2, wy=w*y2, wz=w*z2;
    return new Float32Array([
      (1-(yy+zz))*s[0], (xy+wz)*s[0],     (xz-wy)*s[0],     0,
      (xy-wz)*s[1],     (1-(xx+zz))*s[1], (yz+wx)*s[1],     0,
      (xz+wy)*s[2],     (yz-wx)*s[2],     (1-(xx+yy))*s[2], 0,
      t[0],             t[1],             t[2],             1
    ]);
  }

  function matPerspectiva(fovY, aspect, aproape, departe) {
    var f = 1 / Math.tan(fovY / 2);
    return new Float32Array([
      f / aspect, 0, 0, 0,
      0, f, 0, 0,
      0, 0, (departe + aproape) / (aproape - departe), -1,
      0, 0, (2 * departe * aproape) / (aproape - departe), 0
    ]);
  }

  function matPrivire(ochi, tinta, sus) {
    var zx=ochi[0]-tinta[0], zy=ochi[1]-tinta[1], zz=ochi[2]-tinta[2];
    var l = Math.hypot(zx, zy, zz) || 1; zx/=l; zy/=l; zz/=l;
    var xx = sus[1]*zz - sus[2]*zy, xy = sus[2]*zx - sus[0]*zz, xz = sus[0]*zy - sus[1]*zx;
    l = Math.hypot(xx, xy, xz) || 1; xx/=l; xy/=l; xz/=l;
    var yx = zy*xz - zz*xy, yy = zz*xx - zx*xz, yz = zx*xy - zy*xx;
    return new Float32Array([
      xx, yx, zx, 0,
      xy, yy, zy, 0,
      xz, yz, zz, 0,
      -(xx*ochi[0]+xy*ochi[1]+xz*ochi[2]),
      -(yx*ochi[0]+yy*ochi[1]+yz*ochi[2]),
      -(zx*ochi[0]+zy*ochi[1]+zz*ochi[2]), 1
    ]);
  }

  function matNormala3(m) { // inversa transpusă a colţului 3×3
    var a=m[0],b=m[1],c=m[2], d=m[4],e=m[5],f=m[6], g=m[8],h=m[9],i=m[10];
    var A=e*i-f*h, B=f*g-d*i, C=d*h-e*g;
    var det = a*A + b*B + c*C;
    if (!det) return new Float32Array([1,0,0, 0,1,0, 0,0,1]);
    var id = 1/det;
    return new Float32Array([
      A*id, B*id, C*id,
      (c*h-b*i)*id, (a*i-c*g)*id, (b*g-a*h)*id,
      (b*f-c*e)*id, (c*d-a*f)*id, (a*e-b*d)*id
    ]);
  }

  /* ═══════════════════ 3. shadere ═══════════════════ */

  var VERTEX = [
    '#version 300 es',
    'in vec3 pozitie;',
    'uniform mat4 uModel, uVedere, uProiectie;',
    'out vec3 vLume;',
    'void main() {',
    '  vec4 p = uModel * vec4(pozitie, 1.0);',
    '  vLume = p.xyz;',
    '  gl_Position = uProiectie * uVedere * p;',
    '}'
  ].join('\n');

  // normalele se deduc din derivatele poziţiei: umbrire plată, potrivită
  // pentru geometrie de construcţie şi fără costul stocării lor în fişier
  var FRAGMENT = [
    '#version 300 es',
    'precision highp float;',
    'in vec3 vLume;',
    'uniform vec3 uCuloare, uOchi;',
    'uniform float uRugozitate, uMetal;',
    'out vec4 culoareIesire;',
    '',
    'const vec3 CER    = vec3(0.42, 0.46, 0.54);',
    'const vec3 PAMANT = vec3(0.20, 0.19, 0.18);',
    '',
    'float ggx(vec3 N, vec3 V, vec3 L, float rug) {',
    '  vec3 H = normalize(V + L);',
    '  float a = max(rug * rug, 0.002);',
    '  float d = max(dot(N, H), 0.0);',
    '  float k = d * d * (a * a - 1.0) + 1.0;',
    '  float D = (a * a) / (3.14159265 * k * k);',
    '  float g = a * 0.5;',
    '  float gv = max(dot(N, V), 0.0) * (1.0 - g) + g;',
    '  float gl = max(dot(N, L), 0.0) * (1.0 - g) + g;',
    '  return D * 0.25 / max(gv * gl, 0.001);',
    '}',
    '',
    'vec3 lumina(vec3 N, vec3 V, vec3 dir, vec3 culoareLumina, vec3 difuz, vec3 spec, float rug) {',
    '  vec3 L = normalize(dir);',
    '  float nl = max(dot(N, L), 0.0);',
    '  vec3 F = spec + (1.0 - spec) * pow(1.0 - max(dot(normalize(V + L), V), 0.0), 5.0);',
    '  return culoareLumina * nl * (difuz / 3.14159265 + F * ggx(N, V, L, rug));',
    '}',
    '',
    'void main() {',
    '  vec3 N = normalize(cross(dFdx(vLume), dFdy(vLume)));',
    '  vec3 V = normalize(uOchi - vLume);',
    '  if (dot(N, V) < 0.0) N = -N;',
    '',
    '  vec3 culoare = uCuloare;',
    '  float rug = uRugozitate;',
    '',
    '  vec3 difuz = culoare * (1.0 - uMetal);',
    '  vec3 spec  = mix(vec3(0.04), culoare, uMetal);',
    '',
    '  vec3 c = vec3(0.0);',
    '  c += lumina(N, V, vec3(-0.55,  0.78,  0.55), vec3(2.55, 2.50, 2.42), difuz, spec, rug);',
    '  c += lumina(N, V, vec3( 0.86,  0.22,  0.40), vec3(0.62, 0.66, 0.74), difuz, spec, rug);',
    '  c += lumina(N, V, vec3( 0.10,  0.35, -0.95), vec3(0.80, 0.82, 0.88), difuz, spec, rug);',
    '',
    '  // difuz: cerul deasupra, podeaua dedesubt',
    '  c += difuz * mix(PAMANT, CER, N.y * 0.5 + 0.5) * 0.85;',
    '',
    '  // mediul văzut în oglindă: fără el, metalul iese negru',
    '  vec3 R = reflect(-V, N);',
    '  vec3 mediu = mix(PAMANT, CER, R.y * 0.5 + 0.5);',
    '  float lucios = 1.0 - rug;',
    '  mediu += vec3(2.30, 2.25, 2.15) * pow(max(dot(R, normalize(vec3(-0.55, 0.78, 0.55))), 0.0), 6.0) * lucios;',
    '  mediu += vec3(0.55, 0.58, 0.66) * pow(max(dot(R, normalize(vec3(0.86, 0.22, 0.40))), 0.0), 4.0) * lucios;',
    '  c += spec * mediu * mix(0.32, 1.15, uMetal);',
    '',
    '',
    '  c = (c * (2.51 * c + 0.03)) / (c * (2.43 * c + 0.59) + 0.14);',   // ACES aproximativ
    '  culoareIesire = vec4(pow(clamp(c, 0.0, 1.0), vec3(1.0 / 2.2)), 1.0);',
    '}'
  ].join('\n');

  function compileaza(gl, tip, sursa) {
    var s = gl.createShader(tip);
    gl.shaderSource(s, sursa);
    gl.compileShader(s);
    if (!gl.getShaderParameter(s, gl.COMPILE_STATUS)) {
      throw new Error('shader: ' + gl.getShaderInfoLog(s));
    }
    return s;
  }

  /* ═══════════════════ 4. vizualizatorul ═══════════════════ */

  function Vizualizator(radacina) {
    this.radacina = radacina;
    this.canvas   = radacina.querySelector('canvas');
    this.stari    = JSON.parse(radacina.getAttribute('data-stari') || '[]');
    this.modele   = {};      // fişier -> { primitive, min, max }
    this.stareCurenta = 0;
    this.azimutBaza = 0.62;
    this.azimut   = 0.62;
    this.inaltime = 0.17;
    this.faza     = 0;
    this.raza     = 1;
    this.rotesteSingur = true;
    this.ultimulCadru  = 0;
    this.gata     = false;
  }

  Vizualizator.prototype.porneste = function () {
    var self = this;
    var gl = this.canvas.getContext('webgl2', {
      antialias: true, alpha: true, powerPreference: 'low-power'
    });
    if (!gl) return false;                 // rămâne poza de rezervă
    this.gl = gl;

    var prog = gl.createProgram();
    gl.attachShader(prog, compileaza(gl, gl.VERTEX_SHADER, VERTEX));
    gl.attachShader(prog, compileaza(gl, gl.FRAGMENT_SHADER, FRAGMENT));
    gl.bindAttribLocation(prog, 0, 'pozitie');
    gl.linkProgram(prog);
    if (!gl.getProgramParameter(prog, gl.LINK_STATUS)) {
      throw new Error('program: ' + gl.getProgramInfoLog(prog));
    }
    this.prog = prog;
    this.u = {};
    ['uModel','uVedere','uProiectie','uCuloare','uOchi','uRugozitate','uMetal']
      .forEach(function (n) { self.u[n] = gl.getUniformLocation(prog, n); });

    gl.enable(gl.DEPTH_TEST);
    gl.enable(gl.CULL_FACE);
    gl.cullFace(gl.BACK);

    this.leagaComenzi();
    this.redimensioneaza();

    if (window.matchMedia && window.matchMedia('(prefers-reduced-motion: reduce)').matches) {
      this.rotesteSingur = false;
    }
    return true;
  };

  Vizualizator.prototype.incarca = function (fisier) {
    var self = this, gl = this.gl;
    if (this.modele[fisier]) return Promise.resolve(this.modele[fisier]);

    return fetch(fisier)
      .then(function (r) {
        if (!r.ok) throw new Error('nu pot lua ' + fisier + ' (' + r.status + ')');
        return r.arrayBuffer();
      })
      .then(function (buf) {
        var glb = citesteGLB(buf);
        var j = glb.json;
        var primitive = [];
        var min = [ 1e9, 1e9, 1e9], max = [-1e9,-1e9,-1e9];

        var noduri = (j.scenes && j.scenes[j.scene || 0].nodes) || [];
        function parcurge(indexNod, parinte) {
          var nod = j.nodes[indexNod];
          var local = nod.matrix ? new Float32Array(nod.matrix)
            : matDinTRS(nod.translation || [0,0,0],
                        nod.rotation    || [0,0,0,1],
                        nod.scale       || [1,1,1]);
          var lume = matInmulteste(parinte, local);

          if (nod.mesh !== undefined) {
            j.meshes[nod.mesh].primitives.forEach(function (pr) {
              if (pr.mode !== undefined && pr.mode !== 4) return; // doar triunghiuri
              var pozitii = citesteAccessor(glb, pr.attributes.POSITION);
              var accPoz  = j.accessors[pr.attributes.POSITION];
              var indici  = pr.indices !== undefined ? citesteAccessor(glb, pr.indices) : null;

              if (accPoz.min && accPoz.max) {
                for (var k = 0; k < 3; k++) {
                  min[k] = Math.min(min[k], accPoz.min[k]);
                  max[k] = Math.max(max[k], accPoz.max[k]);
                }
              }

              var vao = gl.createVertexArray();
              gl.bindVertexArray(vao);
              var vb = gl.createBuffer();
              gl.bindBuffer(gl.ARRAY_BUFFER, vb);
              gl.bufferData(gl.ARRAY_BUFFER, pozitii, gl.STATIC_DRAW);
              gl.enableVertexAttribArray(0);
              gl.vertexAttribPointer(0, 3, gl.FLOAT, false, 0, 0);

              var nrIndici = 0, tipIndici = gl.UNSIGNED_SHORT;
              if (indici) {
                var ib = gl.createBuffer();
                gl.bindBuffer(gl.ELEMENT_ARRAY_BUFFER, ib);
                gl.bufferData(gl.ELEMENT_ARRAY_BUFFER, indici, gl.STATIC_DRAW);
                nrIndici = indici.length;
                tipIndici = indici.BYTES_PER_ELEMENT === 4 ? gl.UNSIGNED_INT
                          : indici.BYTES_PER_ELEMENT === 1 ? gl.UNSIGNED_BYTE
                          : gl.UNSIGNED_SHORT;
              }
              gl.bindVertexArray(null);

              var mat = (pr.material !== undefined && j.materials) ? j.materials[pr.material] : null;
              var pbr = (mat && mat.pbrMetallicRoughness) || {};
              var bcf = pbr.baseColorFactor || [0.8, 0.8, 0.8, 1];

              primitive.push({
                vao: vao, model: lume,
                nrIndici: nrIndici, tipIndici: tipIndici,
                nrVertecsi: accPoz.count,
                culoare: [bcf[0], bcf[1], bcf[2]],
                rugozitate: pbr.roughnessFactor !== undefined ? pbr.roughnessFactor : 1,
                metal: pbr.metallicFactor !== undefined ? pbr.metallicFactor : 1,
                douaFete: !!(mat && mat.doubleSided)
              });
            });
          }
          (nod.children || []).forEach(function (c) { parcurge(c, lume); });
        }
        noduri.forEach(function (n) { parcurge(n, matUnitate()); });

        if (min[0] > max[0]) { min = [-1,-1,-1]; max = [1,1,1]; }
        var model = { primitive: primitive, min: min, max: max };
        self.modele[fisier] = model;
        return model;
      });
  };

  Vizualizator.prototype.arata = function (index) {
    var self = this;
    var stare = this.stari[index];
    if (!stare) return Promise.resolve();
    this.radacina.classList.add('viz3d--incarca');

    return this.incarca(stare.fisier).then(function (model) {
      self.stareCurenta = index;
      self.model = model;
      var d = [model.max[0]-model.min[0], model.max[1]-model.min[1], model.max[2]-model.min[2]];
      self.centru = [(model.max[0]+model.min[0])/2,
                     (model.max[1]+model.min[1])/2,
                     (model.max[2]+model.min[2])/2];
      self.dimensiune = Math.max(d[0], d[1], d[2]);
      self.latime = Math.hypot(d[0], d[2]);   // diagonala în plan, ca să încapă la orice rotaţie
      if (!self.gata) { self.raza = self.razaDeIncadrare(); self.gata = true; }
      self.radacina.classList.remove('viz3d--incarca');
      self.radacina.classList.add('viz3d--gata');
      self.actualizeazaButoane();
      self.deseneaza();
    }).catch(function (e) {
      self.radacina.classList.remove('viz3d--incarca');
      self.radacina.classList.add('viz3d--esuat');
      if (window.console) console.warn('vizualizator 3D:', e.message);
    });
  };

  Vizualizator.prototype.actualizeazaButoane = function () {
    var self = this;
    var butoane = this.radacina.querySelectorAll('[data-viz3d-stare]');
    Array.prototype.forEach.call(butoane, function (b) {
      var activ = parseInt(b.getAttribute('data-viz3d-stare'), 10) === self.stareCurenta;
      b.setAttribute('aria-pressed', activ ? 'true' : 'false');
      b.classList.toggle('este-activ', activ);
    });
    this.actualizeazaLegenda();
  };

  /* Legende opționale: [data-viz3d-legenda="0|1"] în același wrap — doar starea activă e vizibilă */
  Vizualizator.prototype.actualizeazaLegenda = function () {
    var wrap = this.radacina.closest('.wm-visual-wrap') || this.radacina.parentElement;
    if (!wrap) return;
    var liste = wrap.querySelectorAll('[data-viz3d-legenda]');
    var stare = this.stareCurenta;
    Array.prototype.forEach.call(liste, function (ul) {
      var s = parseInt(ul.getAttribute('data-viz3d-legenda'), 10);
      if (isNaN(s)) return;
      var activ = s === stare;
      ul.hidden = !activ;
      /* display:flex pe .viz3d-legenda bate [hidden] — forțăm ascunderea */
      ul.style.display = activ ? '' : 'none';
    });
  };

  Vizualizator.prototype.redimensioneaza = function () {
    var raport = Math.min(window.devicePixelRatio || 1, 2);
    var l = this.canvas.clientWidth  || 640;
    var i = this.canvas.clientHeight || 480;
    var nl = Math.max(1, Math.round(l * raport));
    var ni = Math.max(1, Math.round(i * raport));
    if (this.canvas.width !== nl || this.canvas.height !== ni) {
      this.canvas.width = nl; this.canvas.height = ni;
      // reîncadrez, atâta timp cât vizitatorul nu şi-a ales singur apropierea
      if (this.model && !this.zoomManual) this.raza = this.razaDeIncadrare();
    }
  };

  Vizualizator.prototype.deseneaza = function () {
    if (!this.model) return;
    var gl = this.gl;
    this.redimensioneaza();
    gl.viewport(0, 0, this.canvas.width, this.canvas.height);
    gl.clearColor(0, 0, 0, 0);
    gl.clear(gl.COLOR_BUFFER_BIT | gl.DEPTH_BUFFER_BIT);
    gl.useProgram(this.prog);

    var ci = Math.cos(this.inaltime), si = Math.sin(this.inaltime);
    var ochi = [
      this.centru[0] + this.raza * ci * Math.sin(this.azimut),
      this.centru[1] + this.raza * si,
      this.centru[2] + this.raza * ci * Math.cos(this.azimut)
    ];
    var vedere = matPrivire(ochi, this.centru, [0, 1, 0]);
    var proiectie = matPerspectiva(
      0.62, this.canvas.width / this.canvas.height,
      this.dimensiune * 0.02, this.dimensiune * 12);

    gl.uniformMatrix4fv(this.u.uVedere, false, vedere);
    gl.uniformMatrix4fv(this.u.uProiectie, false, proiectie);
    gl.uniform3fv(this.u.uOchi, ochi);

    for (var i = 0; i < this.model.primitive.length; i++) {
      var p = this.model.primitive[i];
      gl.uniformMatrix4fv(this.u.uModel, false, p.model);
      gl.uniform3fv(this.u.uCuloare, p.culoare);
      gl.uniform1f(this.u.uRugozitate, p.rugozitate);
      gl.uniform1f(this.u.uMetal, p.metal);
      if (p.douaFete) gl.disable(gl.CULL_FACE); else gl.enable(gl.CULL_FACE);
      gl.bindVertexArray(p.vao);
      if (p.nrIndici) gl.drawElements(gl.TRIANGLES, p.nrIndici, p.tipIndici, 0);
      else gl.drawArrays(gl.TRIANGLES, 0, p.nrVertecsi);
    }
    gl.bindVertexArray(null);
  };

  Vizualizator.prototype.bucla = function (acum) {
    var self = this;
    if (this.rotesteSingur && this.model) {
      // balans lent în jurul vederii de trei sferturi: panoul nu ajunge niciodată pe muchie
      var dt = this.ultimulCadru ? Math.min((acum - this.ultimulCadru) / 1000, 0.05) : 0;
      this.faza += dt * 0.34;
      this.azimut = this.azimutBaza + Math.sin(this.faza) * 0.5;
      this.deseneaza();
    }
    this.ultimulCadru = acum;
    this.cerere = requestAnimationFrame(function (t) { self.bucla(t); });
  };

  Vizualizator.prototype.leagaComenzi = function () {
    var self = this, c = this.canvas;
    var apasat = false, ultimX = 0, ultimY = 0, degete = {};

    function opresteRotatia() {
      if (self.rotesteSingur) {
        self.rotesteSingur = false;
        self.radacina.classList.add('viz3d--atins');
      }
    }

    c.addEventListener('pointerdown', function (e) {
      apasat = true; ultimX = e.clientX; ultimY = e.clientY;
      degete[e.pointerId] = { x: e.clientX, y: e.clientY };
      opresteRotatia();
      c.setPointerCapture(e.pointerId);
    });

    c.addEventListener('pointermove', function (e) {
      if (degete[e.pointerId]) { degete[e.pointerId].x = e.clientX; degete[e.pointerId].y = e.clientY; }
      var chei = Object.keys(degete);
      if (chei.length >= 2) {                        // ciupire = apropiere/depărtare
        var a = degete[chei[0]], b = degete[chei[1]];
        var d = Math.hypot(a.x - b.x, a.y - b.y);
        if (self.distantaAnterioara) {
          self.zoomManual = true;
          self.raza *= self.distantaAnterioara / Math.max(d, 1);
          self.limiteazaRaza();
          self.deseneaza();
        }
        self.distantaAnterioara = d;
        return;
      }
      if (!apasat) return;
      self.azimut  -= (e.clientX - ultimX) * 0.008;
      self.inaltime = Math.max(-1.25, Math.min(1.25, self.inaltime + (e.clientY - ultimY) * 0.006));
      ultimX = e.clientX; ultimY = e.clientY;
      self.deseneaza();
    });

    function sus(e) {
      apasat = false;
      delete degete[e.pointerId];
      if (Object.keys(degete).length < 2) self.distantaAnterioara = 0;
    }
    c.addEventListener('pointerup', sus);
    c.addEventListener('pointercancel', sus);

    c.addEventListener('wheel', function (e) {
      e.preventDefault();
      opresteRotatia();
      self.zoomManual = true;
      self.raza *= Math.exp(e.deltaY * 0.0012);
      self.limiteazaRaza();
      self.deseneaza();
    }, { passive: false });

    c.setAttribute('tabindex', '0');
    c.addEventListener('keydown', function (e) {
      var pas = 0.14, folosit = true;
      if (e.key === 'ArrowLeft')       self.azimut -= pas;
      else if (e.key === 'ArrowRight') self.azimut += pas;
      else if (e.key === 'ArrowUp')    self.inaltime = Math.min(1.25, self.inaltime + pas);
      else if (e.key === 'ArrowDown')  self.inaltime = Math.max(-1.25, self.inaltime - pas);
      else if (e.key === '+' || e.key === '=') { self.zoomManual = true; self.raza *= 0.88; self.limiteazaRaza(); }
      else if (e.key === '-' || e.key === '_') { self.zoomManual = true; self.raza *= 1.14; self.limiteazaRaza(); }
      else folosit = false;
      if (folosit) { e.preventDefault(); opresteRotatia(); self.deseneaza(); }
    });

    Array.prototype.forEach.call(
      this.radacina.querySelectorAll('[data-viz3d-stare]'),
      function (b) {
        b.addEventListener('click', function () {
          self.arata(parseInt(b.getAttribute('data-viz3d-stare'), 10));
        });
      });

    if (window.ResizeObserver) {
      new ResizeObserver(function () { self.deseneaza(); }).observe(this.canvas);
    } else {
      window.addEventListener('resize', function () { self.deseneaza(); });
    }
  };

  // distanţa la care modelul încape întreg, indiferent de forma canvasului
  Vizualizator.prototype.razaDeIncadrare = function () {
    var fovY = 0.62;
    var aspect = (this.canvas.width || 4) / (this.canvas.height || 3);
    var inaltime = this.model ? (this.model.max[1] - this.model.min[1]) : this.dimensiune;
    var pentruInaltime = (inaltime * 0.5) / Math.tan(fovY / 2);
    var pentruLatime   = (this.latime * 0.5) / (Math.tan(fovY / 2) * aspect);
    return Math.max(pentruInaltime, pentruLatime) * 1.24; // +~5% față de 1.18 — spațiu sub model pentru butoane
  };

  Vizualizator.prototype.limiteazaRaza = function () {
    var d = this.dimensiune || 1;
    this.raza = Math.max(d * 0.55, Math.min(d * 4.5, this.raza));
  };

  /* ═══════════════════ 5. pornire la intrarea în ecran ═══════════════════ */

  function initializeaza(radacina) {
    if (radacina.dataset.viz3dPornit) return;
    radacina.dataset.viz3dPornit = '1';
    var v = new Vizualizator(radacina);
    try {
      if (!v.porneste()) { radacina.classList.add('viz3d--fara-webgl'); return; }
    } catch (e) {
      radacina.classList.add('viz3d--fara-webgl');
      if (window.console) console.warn('vizualizator 3D:', e.message);
      return;
    }
    radacina.viz3d = v;   // pentru depanare din consolă
    v.arata(0).then(function () { v.bucla(0); });
  }

  function porneste() {
    var blocuri = document.querySelectorAll('[data-viz3d]');
    if (!blocuri.length) return;

    if (!('IntersectionObserver' in window)) {
      Array.prototype.forEach.call(blocuri, initializeaza);
      return;
    }
    var observator = new IntersectionObserver(function (intrari) {
      intrari.forEach(function (intrare) {
        if (intrare.isIntersecting) {
          observator.unobserve(intrare.target);
          initializeaza(intrare.target);
        }
      });
    }, { rootMargin: '200px' });
    Array.prototype.forEach.call(blocuri, function (b) { observator.observe(b); });
  }

  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', porneste);
  } else {
    porneste();
  }
})();
