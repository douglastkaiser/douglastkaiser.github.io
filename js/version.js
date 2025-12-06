// Version footer script - fetches commit info from GitHub API
(function() {
    const REPO_OWNER = 'douglastkaiser';
    const REPO_NAME = 'douglastkaiser.github.io';
    const BASE_VERSION = '1.0';

    async function fetchVersionInfo() {
        const footer = document.getElementById('version-footer');
        if (!footer) return;

        try {
            const response = await fetch(
                `https://api.github.com/repos/${REPO_OWNER}/${REPO_NAME}/commits?per_page=1`,
                { headers: { 'Accept': 'application/vnd.github.v3+json' } }
            );

            if (!response.ok) {
                throw new Error('Failed to fetch commit info');
            }

            const commits = await response.json();
            if (commits.length === 0) {
                throw new Error('No commits found');
            }

            const commit = commits[0];
            const sha = commit.sha;
            const shortSha = sha.substring(0, 7);
            const commitDate = new Date(commit.commit.committer.date);
            const dateStr = commitDate.toISOString().split('T')[0].replace(/-/g, '');

            // Get commit count for build number
            const countResponse = await fetch(
                `https://api.github.com/repos/${REPO_OWNER}/${REPO_NAME}/commits?per_page=1`,
                { headers: { 'Accept': 'application/vnd.github.v3+json' } }
            );

            // Use link header to get total count (approximate)
            const linkHeader = countResponse.headers.get('Link');
            let buildNumber = 1;
            if (linkHeader) {
                const match = linkHeader.match(/page=(\d+)>; rel="last"/);
                if (match) {
                    buildNumber = parseInt(match[1], 10);
                }
            }

            const versionString = `v${BASE_VERSION}.${buildNumber}+g${shortSha}.d${dateStr}`;
            const commitUrl = `https://github.com/${REPO_OWNER}/${REPO_NAME}/commit/${sha}`;

            footer.innerHTML = `<a href="${commitUrl}" target="_blank" rel="noopener noreferrer">${versionString} (${shortSha})</a>`;

        } catch (error) {
            console.warn('Version info unavailable:', error.message);
            footer.innerHTML = '<span>Version info unavailable</span>';
        }
    }

    // Run when DOM is ready
    if (document.readyState === 'loading') {
        document.addEventListener('DOMContentLoaded', fetchVersionInfo);
    } else {
        fetchVersionInfo();
    }
})();
