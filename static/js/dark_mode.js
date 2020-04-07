if (localStorage.getItem('mode') === 'dark'){
  document.body.setAttribute('data-theme', 'dark');
  document.getElementById('darkMode').checked = true;
}

document.getElementById('darkMode').addEventListener('change', function(event){
  if (event.target.checked){
    document.body.setAttribute('data-theme', 'dark');
    localStorage.setItem('mode', 'dark');
  } else {
    document.body.removeAttribute('data-theme');
    localStorage.setItem('mode', 'light');
  }
});