// A second entrance to the same site. No duplicated content or page reloads.
(() => {
    const root = document.documentElement;
    const storageKey = 'douglas-kaiser-retro';
    const siteRoot = new URL('../', document.currentScript.src);
    let enabled = false;
    try { enabled = localStorage.getItem(storageKey) === 'on'; } catch {}
    root.classList.toggle('retro-mode', enabled);

    document.addEventListener('DOMContentLoaded', () => {
        const sections = [...document.querySelectorAll('section.resume-section')];
        if (!sections.length) return;

        const header = document.createElement('header');
        header.className = 'retro-header retro-only';
        header.innerHTML = `
            <div class="retro-titlebar"><span>DK / PERSONAL HOME PAGE</span><span>FLIGHT · SOFTWARE · OTHER PURSUITS</span></div>
            <div class="retro-masthead"><a class="retro-wordmark" data-path="">Douglas T. Kaiser<span>Engineer. Builder. Curious person.</span></a><span class="retro-edition">A PERSONAL WEB DIRECTORY<br>Same person. Different entrance.</span></div>
            <nav class="retro-global" aria-label="Site directory"><a data-path="">Home</a><a data-path="projects/">Projects</a><a data-path="blog/">Writing</a><a data-path="resume/">Résumé ↗</a></nav>`;
        header.querySelectorAll('[data-path]').forEach(link => {
            link.href = new URL(link.dataset.path, siteRoot).href;
        });

        const directory = document.createElement('nav');
        directory.className = 'retro-directory retro-only';
        directory.setAttribute('aria-label', 'Page sections');
        const directoryTitle = document.createElement('p');
        directoryTitle.className = 'retro-directory-title';
        directoryTitle.textContent = 'IN THIS DIRECTORY';
        directory.append(directoryTitle);
        const list = document.createElement('ol');
        directory.append(list);
        const labels = {
            about: 'Start here', 'selected-work': 'Engineering strengths',
            experience: 'Work history', education: 'Education', skills: 'The toolbox',
            projects: 'Personal projects', blog: 'Writing', workoutPlanner: 'Kaiserlift',
            stones: 'Stones', civicPulse: 'Civic Pulse', mfatf1: 'MFAT F1',
            reknown: 'Reknown', bayesianCalc: 'Bayesian calculator', Woodworking: 'Woodworking',
        };
        sections.forEach(section => {
            const item = document.createElement('li');
            const link = document.createElement('a');
            link.href = `#${section.id}`;
            link.textContent = labels[section.id] ||
                section.querySelector('h2, h1')?.textContent.replace(/\s+/g, ' ').trim() || section.id;
            item.append(link);
            list.append(item);
        });
        const note = document.createElement('p');
        note.className = 'retro-directory-note';
        note.textContent = 'A small corner of the web. Pick a file. Stay a while.';
        directory.append(note);
        document.body.prepend(header, directory);

        const toggle = document.createElement('button');
        toggle.type = 'button';
        toggle.className = 'era-switch';
        document.body.append(toggle);
        let current = sections[0];

        function selectSection(focus = false) {
            let target;
            try { target = document.getElementById(decodeURIComponent(location.hash.slice(1))); } catch {}
            current = target?.closest('section.resume-section') || sections[0];
            sections.forEach(section => section.classList.toggle('retro-current', section === current));
            directory.querySelectorAll('a').forEach(link => {
                if (link.hash === `#${current.id}`) link.setAttribute('aria-current', 'location');
                else link.removeAttribute('aria-current');
            });
            if (enabled && focus) {
                current.tabIndex = -1;
                current.focus({ preventScroll: true });
                window.scrollTo({ top: 0, behavior: 'instant' });
            }
        }

        function updateMode() {
            root.classList.toggle('retro-mode', enabled);
            toggle.textContent = enabled ? '[ return to the present ]' : '[1994]';
            toggle.setAttribute('aria-pressed', String(enabled));
            toggle.setAttribute('aria-label', enabled ? 'Return to the modern website' : 'Switch to neo-retro 90s minimalism');
            toggle.title = enabled ? 'Return to the present' : 'A different entrance. Try 1994.';
            selectSection();
        }

        toggle.addEventListener('click', () => {
            enabled = !enabled;
            try { localStorage.setItem(storageKey, enabled ? 'on' : 'off'); } catch {}
            updateMode();
            if (enabled) window.scrollTo({ top: 0, behavior: 'instant' });
            else if (location.hash) current.scrollIntoView({ behavior: 'instant' });
        });
        directory.addEventListener('click', event => {
            const link = event.target.closest('a');
            if (!link || event.button !== 0 || event.metaKey || event.ctrlKey || event.shiftKey || event.altKey) return;
            event.preventDefault();
            history.pushState(null, '', link.hash);
            selectSection(true);
        });
        window.addEventListener('hashchange', () => selectSection(enabled));
        window.addEventListener('popstate', () => selectSection(enabled));
        updateMode();
    });
})();
