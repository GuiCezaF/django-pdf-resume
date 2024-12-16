function createLoader() {
  const overlay = document.createElement('div');
  overlay.id = 'loader-overlay';
  overlay.className = 'loader-overlay';

  const spinner = document.createElement('div');
  spinner.id = 'loader';
  spinner.className = 'loader';

  overlay.appendChild(spinner);

  document.body.appendChild(overlay);

  return overlay;
}

function startLoader() {
  let overlay = document.getElementById('loader-overlay');
  if (!overlay) {
    overlay = createLoader();
  }
  overlay.style.display = 'block'; 
}

function stopLoader() {
  const overlay = document.getElementById('loader-overlay');
  if (overlay) {
    overlay.style.display = 'none'; 
  }
}
