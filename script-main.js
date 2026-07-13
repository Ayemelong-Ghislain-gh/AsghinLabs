(function () {
  // ========== EMAIL COPY FALLBACK ==========
  // mailto: links depend on the visitor having a default mail app set up.
  // When there isn't one, clicking silently does nothing. This copies the
  // address to the clipboard as a backup, alongside letting mailto: try
  // normally — whichever one works, the visitor still gets your email.
  let toastEl = null;
  function showCopyToast(message) {
    if (!toastEl) {
      toastEl = document.createElement('div');
      toastEl.className = 'copy-toast';
      document.body.appendChild(toastEl);
    }
    toastEl.textContent = message;
    toastEl.classList.add('show');
    clearTimeout(toastEl._hideTimer);
    toastEl._hideTimer = setTimeout(() => toastEl.classList.remove('show'), 3000);
  }

  document.querySelectorAll('a[href^="mailto:"]').forEach(link => {
    link.addEventListener('click', () => {
      const email = link.getAttribute('href').replace('mailto:', '').split('?')[0];
      if (navigator.clipboard && window.isSecureContext) {
        navigator.clipboard.writeText(email)
          .then(() => showCopyToast(`📋 Copied ${email} — paste it into any email app`))
          .catch(() => {});
      }
      // mailto: is left to fire normally too — if a mail app is set up,
      // it will still open alongside the copy.
    });
  });

  // ========== HAMBURGER MENU ==========
  const hamburger = document.getElementById('hamburgerBtn');
  const navLinks = document.getElementById('navLinks');

  function toggleMenu() {
    hamburger.classList.toggle('active');
    navLinks.classList.toggle('active');
    document.body.style.overflow = navLinks.classList.contains('active') ? 'hidden' : '';
  }

  if (hamburger) hamburger.addEventListener('click', toggleMenu);

  document.querySelectorAll('.nav-links a').forEach(link => {
    link.addEventListener('click', () => {
      if (navLinks && navLinks.classList.contains('active')) toggleMenu();
      const targetId = link.getAttribute('href');
      // Only intercept in-page anchors (#section). Links to other pages (e.g. team.html)
      // are left alone so the browser navigates normally.
      if (targetId && targetId.startsWith('#') && targetId !== '#') {
        const targetSection = document.querySelector(targetId);
        if (targetSection) targetSection.scrollIntoView({ behavior: 'smooth' });
      }
    });
  });

  // ========== INTERACTIVE SERVICE BUTTONS (What We Do) ==========
  const serviceHeaders = document.querySelectorAll('.service-header');

  function closeAllPanels() {
    serviceHeaders.forEach(header => {
      header.classList.remove('active');
      const panelId = header.getAttribute('data-service');
      const panel = document.getElementById(`panel-${panelId}`);
      if (panel) panel.classList.remove('open');
    });
  }

  serviceHeaders.forEach(header => {
    header.addEventListener('click', (e) => {
      e.stopPropagation();
      const service = header.getAttribute('data-service');
      const panel = document.getElementById(`panel-${service}`);
      const isOpen = panel.classList.contains('open');
      closeAllPanels();
      if (!isOpen) {
        header.classList.add('active');
        panel.classList.add('open');
      }
    });
  });

  // ========== COLOR THEMES & CUBE LOGIC (only runs if a cube is present) ==========
  const cube = document.getElementById('magicCube');
  if (!cube) return; // Team page and other pages without a hero cube stop here.

  const logos = ["images/logo-blue.jpeg", "images/logo-green.jpeg", "images/logo-violet.jpeg"];
  const themeMap = {
    "images/logo-blue.jpeg": { primary: "#00d4ff", glow: "rgba(0, 212, 255, 0.4)", rgb: [0, 212, 255] },
    "images/logo-green.jpeg": { primary: "#2ee68b", glow: "rgba(46, 230, 139, 0.45)", rgb: [46, 230, 139] },
    "images/logo-violet.jpeg": { primary: "#b56aff", glow: "rgba(181, 106, 255, 0.5)", rgb: [181, 106, 255] }
  };

  function setBrandTheme(logoPath) {
    const theme = themeMap[logoPath];
    if (!theme) return;
    const root = document.documentElement;
    root.style.setProperty('--brand-primary', theme.primary);
    root.style.setProperty('--brand-glow', theme.glow);
    root.style.setProperty('--border-glow', theme.primary + "cc");
    root.style.setProperty('--brand-rgb', `${theme.rgb[0]}, ${theme.rgb[1]}, ${theme.rgb[2]}`);
    const heroTitle = document.querySelector('.hero h1');
    if (heroTitle) {
      heroTitle.style.background = `linear-gradient(135deg, #ffffff 25%, ${theme.primary} 80%)`;
      heroTitle.style.backgroundClip = 'text';
    }
    const navImg = document.getElementById('navLogoImg');
    if (navImg && !navImg.src.includes(logoPath.split('/').pop())) navImg.src = logoPath;
    document.body.style.background = `radial-gradient(circle at 20% 30%, rgba(${theme.rgb[0]}, ${theme.rgb[1]}, ${theme.rgb[2]}, 0.12), transparent 65%), #050816`;
  }

  const faceLogoMap = {
    front: "images/logo-blue.jpeg",
    back: "images/logo-green.jpeg",
    left: "images/logo-violet.jpeg",
    right: "images/logo-blue.jpeg",
    top: "images/logo-green.jpeg",
    bottom: "images/logo-violet.jpeg"
  };

  function applyPerFaceImages() {
    document.querySelectorAll('.face').forEach(face => {
      const side = face.getAttribute('data-side');
      if (side && faceLogoMap[side]) face.style.backgroundImage = `url('${faceLogoMap[side]}')`;
    });
  }

  let rotX = -18, rotY = 0, targetRotX = -18, targetRotY = 0;
  let isDragging = false, lastMouseX = 0, lastMouseY = 0, velocityX = 0, velocityY = 0, lastTimestamp = 0;
  let autoSpinActive = true, autoSpinSpeedY = 0.3, autoSpinSpeedX = 0.05;

  function updateThemeFromRotation(yAngle) {
    let angle = ((yAngle % 360) + 360) % 360;
    let activeFace = 'front';
    if (angle >= 45 && angle < 135) activeFace = 'right';
    else if (angle >= 135 && angle < 225) activeFace = 'back';
    else if (angle >= 225 && angle < 315) activeFace = 'left';
    const activeLogo = faceLogoMap[activeFace] || logos[0];
    setBrandTheme(activeLogo);
    document.querySelectorAll('.face').forEach(face => {
      if (face.getAttribute('data-side') === activeFace) face.style.filter = 'brightness(1.1) contrast(1.05)';
      else face.style.filter = '';
    });
  }

  function updateCubeTransform() {
    rotX += (targetRotX - rotX) * 0.12;
    rotY += (targetRotY - rotY) * 0.12;
    cube.style.transform = `rotateX(${rotX}deg) rotateY(${rotY}deg)`;
    updateThemeFromRotation(rotY);
  }

  function animate() {
    updateCubeTransform();
    if (!isDragging && autoSpinActive) {
      targetRotY += autoSpinSpeedY;
      targetRotX += autoSpinSpeedX;
      if (targetRotX > 15) targetRotX = 15;
      if (targetRotX < -40) targetRotX = -40;
    }
    if (!isDragging && (Math.abs(velocityX) > 0.05 || Math.abs(velocityY) > 0.05)) {
      targetRotY += velocityX;
      targetRotX += velocityY;
      velocityX *= 0.96;
      velocityY *= 0.96;
    }
    requestAnimationFrame(animate);
  }

  function getClientCoords(e) {
    if (e.touches) return { x: e.touches[0].clientX, y: e.touches[0].clientY };
    return { x: e.clientX, y: e.clientY };
  }

  function onPointerStart(e) {
    e.preventDefault();
    isDragging = true;
    autoSpinActive = false;
    const coords = getClientCoords(e);
    lastMouseX = coords.x; lastMouseY = coords.y;
    lastTimestamp = performance.now();
    velocityX = velocityY = 0;
    cube.style.cursor = 'grabbing';
  }

  function onPointerMove(e) {
    if (!isDragging) return;
    e.preventDefault();
    const coords = getClientCoords(e);
    const deltaX = coords.x - lastMouseX, deltaY = coords.y - lastMouseY;
    if (deltaX !== 0 || deltaY !== 0) {
      targetRotY += deltaX * 0.7;
      targetRotX += deltaY * 0.5;
      const now = performance.now();
      const dt = Math.min(100, now - lastTimestamp);
      if (dt > 0) {
        velocityX = deltaX * 0.7 * (16 / dt);
        velocityY = deltaY * 0.5 * (16 / dt);
        velocityX = Math.min(8, Math.max(-8, velocityX));
        velocityY = Math.min(5, Math.max(-5, velocityY));
      }
      lastMouseX = coords.x; lastMouseY = coords.y;
      lastTimestamp = now;
      if (targetRotX > 25) targetRotX = 25;
      if (targetRotX < -50) targetRotX = -50;
    }
  }

  function onPointerEnd() {
    isDragging = false;
    cube.style.cursor = 'grab';
    setTimeout(() => { if (!isDragging) autoSpinActive = true; }, 1500);
  }

  cube.addEventListener('mousedown', onPointerStart);
  window.addEventListener('mousemove', onPointerMove);
  window.addEventListener('mouseup', onPointerEnd);
  cube.addEventListener('touchstart', onPointerStart, { passive: false });
  window.addEventListener('touchmove', onPointerMove, { passive: false });
  window.addEventListener('touchend', onPointerEnd);

  let hoverActive = false;
  cube.addEventListener('mouseenter', () => { hoverActive = true; });
  cube.addEventListener('mousemove', (e) => {
    if (!hoverActive) return;
    const rect = cube.getBoundingClientRect();
    let relX = (e.clientX - rect.left - rect.width / 2) / (rect.width / 2);
    let relY = (e.clientY - rect.top - rect.height / 2) / (rect.height / 2);
    relX = Math.min(0.8, Math.max(-0.8, relX));
    relY = Math.min(0.8, Math.max(-0.8, relY));
    if (!isDragging) { autoSpinSpeedY = relX * 1.2; autoSpinSpeedX = relY * 0.8; }
  });
  cube.addEventListener('mouseleave', () => {
    hoverActive = false;
    if (!isDragging) { autoSpinSpeedY = 0.3; autoSpinSpeedX = 0.05; }
  });

  cube.addEventListener('click', (e) => {
    if (Math.abs(velocityX) > 0.5 || Math.abs(velocityY) > 0.5) return;
    cube.style.transform += ' scale(1.08)';
    setTimeout(() => { cube.style.transform = `rotateX(${rotX}deg) rotateY(${rotY}deg)`; }, 180);
    const sides = ['front', 'back', 'left', 'right', 'top', 'bottom'];
    sides.forEach(side => {
      const randomLogo = logos[Math.floor(Math.random() * logos.length)];
      faceLogoMap[side] = randomLogo;
      const faceDiv = document.querySelector(`.face[data-side="${side}"]`);
      if (faceDiv) faceDiv.style.backgroundImage = `url('${randomLogo}')`;
    });
    updateThemeFromRotation(rotY);
  });

  applyPerFaceImages();
  setBrandTheme(faceLogoMap.front);
  targetRotX = -18; targetRotY = 0; rotX = -18; rotY = 0;
  updateCubeTransform();
  animate();
})();
