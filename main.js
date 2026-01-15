// =====================================================
// TSAS – FINAL MAIN.JS (RESET-ONLY, CONTINUOUS SIMULATION)
// =====================================================

// ===============================
// BASIC SETUP
// ===============================
const container = document.getElementById("scene-container");

const scene = new THREE.Scene();
scene.background = new THREE.Color(0x000000);

const camera = new THREE.PerspectiveCamera(
  60,
  window.innerWidth / window.innerHeight,
  0.1,
  1000
);

camera.position.set(0, 80, 140);
camera.lookAt(0, 0, 0);

const renderer = new THREE.WebGLRenderer({ antialias: true });
renderer.setSize(window.innerWidth, window.innerHeight);
renderer.setPixelRatio(window.devicePixelRatio);
container.appendChild(renderer.domElement);

// ===============================
// SIMULATION STATE
// ===============================
let isPaused = false;

// ===============================
// LIGHTS
// ===============================
scene.add(new THREE.AmbientLight(0xffffff, 0.6));

const light = new THREE.DirectionalLight(0xffffff, 0.8);
light.position.set(50, 100, 50);
scene.add(light);

// ===============================
// ZONE CONFIG
// ===============================
const ZONE_RADIUS = 25;
const MAX_RANGE = 130;

// ===============================
// PROTECTED ZONE
// ===============================
const zone = new THREE.Mesh(
  new THREE.SphereGeometry(ZONE_RADIUS, 32, 32),
  new THREE.MeshPhongMaterial({
    color: 0x00ffff,
    transparent: true,
    opacity: 0.3,
  })
);
scene.add(zone);

// ===============================
// DISTANCE RINGS
// ===============================
function createRing(radius, color) {
  const ring = new THREE.Mesh(
    new THREE.RingGeometry(radius - 0.3, radius + 0.3, 64),
    new THREE.MeshBasicMaterial({
      color,
      side: THREE.DoubleSide,
      transparent: true,
      opacity: 0.8,
    })
  );
  ring.rotation.x = Math.PI / 2;
  scene.add(ring);
}

createRing(60, 0x00ff00);   // SAFE
createRing(40, 0xffff00);   // WARNING
createRing(25, 0xff0000);   // CRITICAL

// ===============================
// INTRUDERS
// ===============================
const intruders = [];

function randomSpawn() {
  const angle = Math.random() * Math.PI * 2;
  return new THREE.Vector3(
    Math.cos(angle) * MAX_RANGE,
    0,
    Math.sin(angle) * MAX_RANGE
  );
}

function randomVelocity() {
  return new THREE.Vector3(
    (Math.random() - 0.5) * 0.6,
    0,
    (Math.random() - 0.5) * 0.6
  );
}

function createIntruder() {
  const mesh = new THREE.Mesh(
    new THREE.SphereGeometry(3, 16, 16),
    new THREE.MeshPhongMaterial({ color: 0x00ff00 })
  );

  mesh.position.copy(randomSpawn());
  scene.add(mesh);

  return {
    mesh,
    velocity: randomVelocity(),
    probs: [0.25, 0.25, 0.25, 0.25], // mock ANN probabilities
    threatScore: 0,
  };
}

// Spawn intruders
for (let i = 0; i < 3; i++) {
  intruders.push(createIntruder());
}

// ===============================
// ALERT UI
// ===============================
const alertDiv = document.createElement("div");
alertDiv.style.position = "absolute";
alertDiv.style.bottom = "20px";
alertDiv.style.left = "20px";
alertDiv.style.color = "white";
alertDiv.style.fontFamily = "monospace";
alertDiv.style.fontSize = "16px";
document.body.appendChild(alertDiv);

// ===============================
// CONTROL PANEL
// ===============================
const controlDiv = document.createElement("div");
controlDiv.style.position = "absolute";
controlDiv.style.top = "20px";
controlDiv.style.right = "20px";
controlDiv.style.background = "rgba(0,0,0,0.6)";
controlDiv.style.padding = "10px";
controlDiv.style.borderRadius = "8px";
controlDiv.style.fontFamily = "monospace";

controlDiv.innerHTML = `
  <button id="pauseBtn">⏸ Pause</button>
  <button id="resumeBtn">▶ Resume</button>
  <button id="resetBtn">🔄 Reset</button>
`;

document.body.appendChild(controlDiv);

document.querySelectorAll("#pauseBtn, #resumeBtn, #resetBtn").forEach(btn => {
  btn.style.margin = "4px";
  btn.style.padding = "6px 10px";
  btn.style.cursor = "pointer";
});

document.getElementById("pauseBtn").onclick = () => isPaused = true;
document.getElementById("resumeBtn").onclick = () => isPaused = false;
document.getElementById("resetBtn").onclick = () => {
  intruders.forEach(i => {
    i.mesh.position.copy(randomSpawn());
    i.velocity.copy(randomVelocity());
    i.threatScore = 0;
  });
};

// ===============================
// THREAT SCORE FUNCTION
// ===============================
function computeThreatScore(probs, distance) {
  const weights = [0.2, 0.5, 0.8, 1.0];
  const base = probs.reduce((s, p, i) => s + p * weights[i], 0);
  const distanceWeight = Math.max(0, 1 - distance / 120);
  return Math.min(100, base * distanceWeight * 100);
}

// ===============================
// RESIZE HANDLING
// ===============================
window.addEventListener("resize", () => {
  camera.aspect = window.innerWidth / window.innerHeight;
  camera.updateProjectionMatrix();
  renderer.setSize(window.innerWidth, window.innerHeight);
});

// ===============================
// ANIMATION LOOP (RESET-ONLY)
// ===============================
function animate() {
  requestAnimationFrame(animate);

  let totalThreat = 0;
  let text = "";

  intruders.forEach((intruder, index) => {

    if (!isPaused) {
      intruder.mesh.position.add(intruder.velocity);
    }

    const distance = intruder.mesh.position.length();

    // ✅ RESET ONLY WHEN OUT OF RANGE
    if (distance > MAX_RANGE) {
      intruder.mesh.position.copy(randomSpawn());
      intruder.velocity.copy(randomVelocity());
      intruder.threatScore = 0;
      return;
    }

    const score = computeThreatScore(intruder.probs, distance);
    intruder.threatScore = score;
    totalThreat += score;

    let label = "SAFE";
    let color = 0x00ff00;

    if (distance < 25) {
      label = "CRITICAL";
      color = 0xff0000;
    } else if (distance < 40) {
      label = "WARNING";
      color = 0xffff00;
    } else if (distance < 60) {
      label = "MEDIUM";
      color = 0x00ffff;
    }

    intruder.mesh.material.color.setHex(color);

    text += `Intruder ${index + 1}: ${distance.toFixed(1)} —
      <span style="color:${
        label === "CRITICAL" ? "red" :
        label === "WARNING" ? "yellow" :
        label === "MEDIUM" ? "cyan" : "lime"
      }">${label}</span><br/>`;
  });

  const globalThreat = totalThreat / intruders.length;

  // ===============================
  // COLOR-BASED SCENE FEEDBACK
  // ===============================
  if (globalThreat > 70) {
    zone.material.color.setHex(0xff0000);
  } else if (globalThreat > 40) {
    zone.material.color.setHex(0xffff00);
  } else {
    zone.material.color.setHex(0x00ffff);
  }

  alertDiv.innerHTML = `
    ${text}
    <br/>
    <b>GLOBAL THREAT SCORE:</b>
    <span style="color:${
      globalThreat > 70 ? "red" :
      globalThreat > 40 ? "yellow" : "lime"
    }">${globalThreat.toFixed(1)} / 100</span>
  `;

  renderer.render(scene, camera);
}

animate();
