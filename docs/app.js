/* ==========================================================================
   Toolbelt CLI - Documentation App JavaScript
   Interactive Simulator, Search Modal, Theme Switcher, Tabs & Copy
   ========================================================================== */

document.addEventListener('DOMContentLoaded', () => {
  initTheme();
  initTabs();
  initCopyButtons();
  initScrollSpy();
  initMobileNav();
  initSearch();
  initTerminalSimulator();
});

/* ==========================================================================
   1. Theme Management (Dark / Light with LocalStorage)
   ========================================================================== */
function initTheme() {
  const themeToggle = document.getElementById('theme-toggle');
  const storedTheme = localStorage.getItem('toolbelt-theme') || 'dark';

  document.documentElement.setAttribute('data-theme', storedTheme);
  updateThemeIcon(storedTheme);

  if (themeToggle) {
    themeToggle.addEventListener('click', () => {
      const current = document.documentElement.getAttribute('data-theme');
      const next = current === 'dark' ? 'light' : 'dark';
      document.documentElement.setAttribute('data-theme', next);
      localStorage.setItem('toolbelt-theme', next);
      updateThemeIcon(next);
    });
  }
}

function updateThemeIcon(theme) {
  const icon = document.querySelector('#theme-toggle span');
  if (icon) {
    icon.textContent = theme === 'dark' ? '🌙' : '☀️';
  }
}

/* ==========================================================================
   2. Code Tabs Switcher
   ========================================================================== */
function initTabs() {
  const tabContainers = document.querySelectorAll('.tabs-container');

  tabContainers.forEach((container) => {
    const buttons = container.querySelectorAll('.tab-btn');
    const contents = container.querySelectorAll('.tab-content');

    buttons.forEach((btn) => {
      btn.addEventListener('click', () => {
        const target = btn.getAttribute('data-tab');

        buttons.forEach((b) => b.classList.remove('active'));
        contents.forEach((c) => c.classList.remove('active'));

        btn.classList.add('active');
        const targetEl = container.querySelector(`[data-tab-content="${target}"]`);
        if (targetEl) targetEl.classList.add('active');
      });
    });
  });
}

/* ==========================================================================
   3. Copy-to-Clipboard Functionality
   ========================================================================== */
function initCopyButtons() {
  document.querySelectorAll('.copy-btn').forEach((btn) => {
    btn.addEventListener('click', async () => {
      const targetId = btn.getAttribute('data-target');
      let textToCopy = '';

      if (targetId) {
        const targetEl = document.getElementById(targetId);
        textToCopy = targetEl ? targetEl.innerText.trim() : '';
      } else {
        const codeEl = btn.closest('.code-block').querySelector('code');
        textToCopy = codeEl ? codeEl.innerText.trim() : '';
      }

      try {
        await navigator.clipboard.writeText(textToCopy);
        const originalText = btn.innerHTML;
        btn.classList.add('copied');
        btn.innerHTML = '<span>✓</span> Copied!';
        setTimeout(() => {
          btn.classList.remove('copied');
          btn.innerHTML = originalText;
        }, 2000);
      } catch (err) {
        console.error('Failed to copy text: ', err);
      }
    });
  });
}

/* ==========================================================================
   4. ScrollSpy for TOC & Sidebar Highlights
   ========================================================================== */
function initScrollSpy() {
  const sections = document.querySelectorAll('section[id], h2[id], h3[id]');
  const navLinks = document.querySelectorAll('.sidebar-nav .nav-link, .toc-link');

  if (!sections.length) return;

  const observer = new IntersectionObserver(
    (entries) => {
      entries.forEach((entry) => {
        if (entry.isIntersecting) {
          const id = entry.target.getAttribute('id');
          navLinks.forEach((link) => {
            const href = link.getAttribute('href');
            if (href === `#${id}`) {
              link.classList.add('active');
            } else if (href && href.startsWith('#')) {
              link.classList.remove('active');
            }
          });
        }
      });
    },
    {
      rootMargin: '-80px 0px -70% 0px',
      threshold: 0,
    }
  );

  sections.forEach((sec) => observer.observe(sec));
}

/* ==========================================================================
   5. Mobile Drawer Navigation
   ========================================================================== */
function initMobileNav() {
  const menuBtn = document.getElementById('mobile-menu-toggle');
  const sidebar = document.querySelector('.docs-sidebar');

  if (menuBtn && sidebar) {
    menuBtn.addEventListener('click', () => {
      sidebar.classList.toggle('open');
    });

    document.querySelectorAll('.sidebar-nav a').forEach((link) => {
      link.addEventListener('click', () => {
        if (window.innerWidth <= 860) {
          sidebar.classList.remove('open');
        }
      });
    });
  }
}

/* ==========================================================================
   6. Search Modal (Ctrl+K / Cmd+K)
   ========================================================================== */
const SEARCH_INDEX = [
  {
    title: 'Installation',
    snippet: 'Install via pipx, uv, pip, or git clone source setup.',
    url: '#installation',
  },
  {
    title: 'Quickstart & CLI Overview',
    snippet: 'Run toolbelt --help to view arguments, commands, and subcommands.',
    url: '#quickstart',
  },
  {
    title: 'toolbelt new (Scaffolder)',
    snippet: 'Scaffold new Python, Node.js/TypeScript, or Java Maven projects.',
    url: '#cmd-new',
  },
  {
    title: 'toolbelt commit (AI Git Commits)',
    snippet: 'Generate Conventional Commit messages using Claude API or offline fallback.',
    url: '#cmd-commit',
  },
  {
    title: 'toolbelt audit (Repository Auditor)',
    snippet: '10-point repository standards check with auto-fix (--fix) and JSON output.',
    url: '#cmd-audit',
  },
  {
    title: 'toolbelt version (PyPI Checker)',
    snippet: 'Check current version and query PyPI release registry for updates.',
    url: '#cmd-version',
  },
  {
    title: 'Configuration & Environment',
    snippet: 'Configure ANTHROPIC_API_KEY, LOG_LEVEL, and .env settings.',
    url: '#configuration',
  },
  {
    title: 'Architecture & Tech Stack',
    snippet: 'Built with Python 3.11, Typer, Rich, Jinja2, HTTPX, and Anthropic SDK.',
    url: '#architecture',
  },
  {
    title: 'PyPI Trusted Publishing (OIDC)',
    snippet: 'Automated release workflow with GitHub Actions OpenID Connect.',
    url: '#publishing',
  },
  {
    title: 'Contributing Guide',
    snippet: 'Fork repository, run pytest, lint with Ruff, and type check with MyPy.',
    url: '#contributing',
  },
];

function initSearch() {
  const triggerBtn = document.getElementById('search-trigger');
  const modalBackdrop = document.getElementById('search-modal-backdrop');
  const searchInput = document.getElementById('search-modal-input');
  const searchResults = document.getElementById('search-results');

  if (!triggerBtn || !modalBackdrop || !searchInput) return;

  function openSearch() {
    modalBackdrop.classList.add('open');
    searchInput.value = '';
    renderSearchResults('');
    setTimeout(() => searchInput.focus(), 50);
  }

  function closeSearch() {
    modalBackdrop.classList.remove('open');
  }

  triggerBtn.addEventListener('click', openSearch);

  modalBackdrop.addEventListener('click', (e) => {
    if (e.target === modalBackdrop) closeSearch();
  });

  window.addEventListener('keydown', (e) => {
    if ((e.ctrlKey || e.metaKey) && e.key === 'k') {
      e.preventDefault();
      modalBackdrop.classList.contains('open') ? closeSearch() : openSearch();
    }
    if (e.key === 'Escape' && modalBackdrop.classList.contains('open')) {
      closeSearch();
    }
  });

  searchInput.addEventListener('input', (e) => {
    renderSearchResults(e.target.value);
  });

  function renderSearchResults(query) {
    const q = query.trim().toLowerCase();
    const matches = !q
      ? SEARCH_INDEX.slice(0, 5)
      : SEARCH_INDEX.filter(
          (item) =>
            item.title.toLowerCase().includes(q) ||
            item.snippet.toLowerCase().includes(q)
        );

    if (matches.length === 0) {
      searchResults.innerHTML = `
        <div style="padding: 24px; text-align: center; color: var(--text-dim);">
          No matching documentation found for "${query}"
        </div>`;
      return;
    }

    searchResults.innerHTML = matches
      .map(
        (m, idx) => `
        <a href="${m.url}" class="search-item ${idx === 0 ? 'selected' : ''}" onclick="document.getElementById('search-modal-backdrop').classList.remove('open')">
          <span class="search-item-title">${m.title}</span>
          <span class="search-item-snippet">${m.snippet}</span>
        </a>
      `
      )
      .join('');
  }
}

/* ==========================================================================
   7. Interactive Terminal Simulator
   ========================================================================== */
const SIMULATED_RESPONSES = {
  'toolbelt --help': `Usage: toolbelt [OPTIONS] COMMAND [ARGS]...

  Toolbelt – developer productivity CLI: scaffolding, AI commits, and audits.

Options:
  --install-completion          Install completion for the current shell.
  --show-completion             Show completion for the current shell.
  --help                        Show this message and exit.

Commands:
  audit    Audit repo for README sections, .gitignore, licenses, and CI.
  commit   Generate Conventional Commit messages from diff using Claude API.
  new      Scaffold a new project (python, node, java) with opinionated defaults.
  version  Print installed version and check PyPI for updates.`,

  'toolbelt new python demo_app': `Author name [Developer]: Christopher
License [MIT]: MIT
Include CI? (y/n) [True]: y
Include Docker? (y/n) [False]: y

┌──────────────────────────── 🎉 Toolbelt Scaffold ────────────────────────────┐
│ ✨ Project successfully scaffolded!                                         │
│                                                                             │
│ Next steps:                                                                 │
│ cd demo_app && make install && make test                                    │
└─────────────────────────────────────────────────────────────────────────────┘`,

  'toolbelt new node web_app': `Author name [Developer]: Developer
License [MIT]: MIT
Include CI? (y/n) [True]: y
Include Docker? (y/n) [False]: n

┌──────────────────────────── 🎉 Toolbelt Scaffold ────────────────────────────┐
│ ✨ Project successfully scaffolded!                                         │
│                                                                             │
│ Next steps:                                                                 │
│ cd web_app && npm install && npm test                                       │
└─────────────────────────────────────────────────────────────────────────────┘`,

  'toolbelt commit': `┌────────────────────────── Proposed Commit Message ──────────────────────────┐
│ feat(auth): add bearer token validator and refresh middleware              │
└─────────────────────────────────────────────────────────────────────────────┘

Apply commit? [y/n/edit] (y): y
[bold green]✅ Commit created successfully![/bold green]`,

  'toolbelt commit --dry-run': `┌────────────────────────── Proposed Commit Message ──────────────────────────┐
│ fix(cli): handle non-zero exit code on git subprocess failure               │
└─────────────────────────────────────────────────────────────────────────────┘

Dry run – commit not performed.`,

  'toolbelt audit .': `                    Repository Audit: toolbelt-cli                     
┌────────────────────────────┬──────────┬──────────────────────────┐
│ Check                      │  Status  │ Details                  │
├────────────────────────────┼──────────┼──────────────────────────┤
│ README.md exists           │    ✅    │ 344 lines                │
│ README has Install         │    ✅    │ found "## Installation"  │
│ README has Usage           │    ✅    │ found "## Usage"         │
│ README has License         │    ✅    │ found "## License"       │
│ LICENSE file               │    ✅    │ MIT                      │
│ .gitignore exists          │    ✅    │ 29 entries               │
│ .gitignore has __pycache__ │    ✅    │                          │
│ Tests directory            │    ✅    │ tests/ found             │
│ CI config                  │    ✅    │ .github/workflows/ci.yml │
│ pyproject.toml             │    ✅    │                          │
└────────────────────────────┴──────────┴──────────────────────────┘`,

  'toolbelt version': `╭───────────────────────────────╮
│ toolbelt-cli version: 0.2.0   │
╰───────────────────────────────╯
A newer version 0.2.0 is available!
Run: pip install -U toolbelt-cli`,

  'clear': '__CLEAR__',
};

function initTerminalSimulator() {
  const screen = document.getElementById('term-screen');
  const input = document.getElementById('term-input');
  const simButtons = document.querySelectorAll('.sim-btn');

  if (!screen || !input) return;

  function runSimulatedCommand(cmd) {
    const trimmed = cmd.trim();
    if (!trimmed) return;

    if (trimmed.toLowerCase() === 'clear') {
      screen.innerHTML = '';
      return;
    }

    // Append command prompt
    const cmdRow = document.createElement('div');
    cmdRow.innerHTML = `<span style="color:#10b981;font-weight:700;">$</span> <span style="color:#f8fafc;font-weight:600;">${escapeHtml(trimmed)}</span>`;
    screen.appendChild(cmdRow);

    // Find response or default
    let output = SIMULATED_RESPONSES[trimmed];
    if (!output) {
      if (trimmed.startsWith('toolbelt new')) {
        output = SIMULATED_RESPONSES['toolbelt new python demo_app'];
      } else if (trimmed.startsWith('toolbelt commit')) {
        output = SIMULATED_RESPONSES['toolbelt commit'];
      } else if (trimmed.startsWith('toolbelt audit')) {
        output = SIMULATED_RESPONSES['toolbelt audit .'];
      } else if (trimmed.startsWith('toolbelt version')) {
        output = SIMULATED_RESPONSES['toolbelt version'];
      } else {
        output = `toolbelt: command not recognized: "${trimmed}". Type "toolbelt --help" or click one of the quick test buttons above.`;
      }
    }

    const outBlock = document.createElement('div');
    outBlock.style.color = '#cbd5e1';
    outBlock.style.margin = '6px 0 16px';
    outBlock.innerHTML = formatRichOutput(output);
    screen.appendChild(outBlock);

    screen.scrollTop = screen.scrollHeight;
  }

  input.addEventListener('keydown', (e) => {
    if (e.key === 'Enter') {
      runSimulatedCommand(input.value);
      input.value = '';
    }
  });

  simButtons.forEach((btn) => {
    btn.addEventListener('click', () => {
      const cmd = btn.getAttribute('data-cmd');
      if (cmd) {
        runSimulatedCommand(cmd);
      }
    });
  });
}

function escapeHtml(text) {
  const map = { '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;', "'": '&#039;' };
  return text.replace(/[&<>"']/g, (m) => map[m]);
}

function formatRichOutput(text) {
  let formatted = escapeHtml(text);
  formatted = formatted.replace(/✅/g, '<span style="color:#10b981;">✅</span>');
  formatted = formatted.replace(/❌/g, '<span style="color:#f43f5e;">❌</span>');
  formatted = formatted.replace(/\[bold green\](.*?)\[\/bold green\]/g, '<span style="color:#10b981;font-weight:bold;">$1</span>');
  formatted = formatted.replace(/(Next steps:)/g, '<span style="color:#94a3b8;">$1</span>');
  formatted = formatted.replace(/(cd [^\n]+)/g, '<span style="color:#06b6d4;font-weight:bold;">$1</span>');
  formatted = formatted.replace(/(toolbelt-cli version:[^\n]+)/g, '<span style="color:#10b981;font-weight:bold;">$1</span>');
  formatted = formatted.replace(/(A newer version [^\n]+ is available!)/g, '<span style="color:#f59e0b;font-weight:bold;">$1</span>');
  formatted = formatted.replace(/(pip install -U toolbelt-cli)/g, '<span style="color:#06b6d4;font-weight:bold;">$1</span>');
  return formatted;
}
