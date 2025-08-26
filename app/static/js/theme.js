// Persisted theme with prefers-color-scheme fallback
(function () {
  const root = document.documentElement;
  const key = 'theme';
  function setTheme(mode) {
    if (mode === 'light') {
      root.classList.remove('dark');
      localStorage.setItem(key, 'light');
    } else {
      root.classList.add('dark');
      localStorage.setItem(key, 'dark');
    }
  }
  function init() {
    const stored = localStorage.getItem(key);
    const prefersDark = window.matchMedia('(prefers-color-scheme: dark)').matches;
    const mode = stored || (prefersDark ? 'dark' : 'light');
    setTheme(mode);
    const btn = document.getElementById('theme-toggle');
    if (btn) {
      btn.addEventListener('click', function () {
        const isDark = root.classList.contains('dark');
        setTheme(isDark ? 'light' : 'dark');
      });
    }
  }
  document.addEventListener('DOMContentLoaded', init);
})();


