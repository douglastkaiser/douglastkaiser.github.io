#!/usr/bin/env python3
from html.parser import HTMLParser
from urllib.parse import urljoin, urlparse, urldefrag
from urllib.request import Request, urlopen
from urllib.error import HTTPError, URLError
import ssl
import sys

BASE = 'https://www.douglastkaiser.com/'
EXPECTED_RESUME = '/assets/resume.pdf'
UAS = {
    'desktop': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 Chrome/124.0.0.0 Safari/537.36',
    'mobile': 'Mozilla/5.0 (iPhone; CPU iPhone OS 17_0 like Mac OS X) AppleWebKit/605.1.15 Version/17.0 Mobile/15E148 Safari/604.1',
}

class AnchorParser(HTMLParser):
    def __init__(self):
        super().__init__()
        self.anchors = []

    def handle_starttag(self, tag, attrs):
        if tag.lower() == 'a':
            attrs_dict = dict(attrs)
            href = attrs_dict.get('href')
            if href:
                self.anchors.append(href)

def fetch(url: str, ua: str):
    req = Request(url, headers={'User-Agent': ua})
    with urlopen(req, timeout=20, context=ssl.create_default_context()) as resp:
        body = resp.read().decode('utf-8', errors='replace')
        return resp.status, body

def check_status(url: str, ua: str):
    req = Request(url, headers={'User-Agent': ua}, method='HEAD')
    try:
        with urlopen(req, timeout=20, context=ssl.create_default_context()) as resp:
            return resp.status, None
    except HTTPError as e:
        if e.code in (405, 501):
            try:
                req = Request(url, headers={'User-Agent': ua}, method='GET')
                with urlopen(req, timeout=20, context=ssl.create_default_context()) as resp:
                    return resp.status, None
            except Exception as inner:
                return None, str(inner)
        return e.code, None
    except URLError as e:
        return None, str(e)
    except Exception as e:
        return None, str(e)

def classify(href: str):
    if href.startswith(('mailto:', 'tel:', 'javascript:')):
        return 'skip'
    abs_url = urldefrag(urljoin(BASE, href)).url
    parsed = urlparse(abs_url)
    if parsed.scheme not in ('http', 'https'):
        return 'skip'
    if parsed.netloc == urlparse(BASE).netloc:
        return 'internal', abs_url
    return 'external', abs_url

def run():
    failed_internal = []
    failed_external = []
    resume_assertions = []
    resume_target_checks = []

    for label, ua in UAS.items():
        status, body = fetch(BASE, ua)
        print(f'[{label}] homepage status: {status}')
        parser = AnchorParser()
        parser.feed(body)
        hrefs = parser.anchors
        print(f'[{label}] anchors found: {len(hrefs)}')

        resume_links = [h for h in hrefs if urldefrag(h).url == EXPECTED_RESUME or urldefrag(urlparse(h).path).url == EXPECTED_RESUME]
        resume_visible = len(resume_links) > 0
        resume_assertions.append((label, resume_visible, resume_links))

        resume_url = urljoin(BASE, EXPECTED_RESUME.lstrip('/'))
        resume_code, resume_err = check_status(resume_url, ua)
        resume_target_checks.append((label, resume_url, resume_code, resume_err))

        internal_urls, external_urls = set(), set()
        for href in hrefs:
            result = classify(href)
            if result == 'skip':
                continue
            kind, abs_url = result
            if kind == 'internal':
                internal_urls.add(abs_url)
            else:
                external_urls.add(abs_url)

        for link in sorted(internal_urls):
            code, err = check_status(link, ua)
            if err or code is None or code >= 400:
                failed_internal.append((label, link, code, err))

        for link in sorted(external_urls):
            code, err = check_status(link, ua)
            if err or code is None or code >= 400:
                failed_external.append((label, link, code, err))

    print('\nResume assertions:')
    resume_ok = True
    for label, visible, links in resume_assertions:
        ok = visible and any(urldefrag(urlparse(h).path).url == EXPECTED_RESUME or urldefrag(h).url == EXPECTED_RESUME for h in links)
        resume_ok = resume_ok and ok
        print(f'- [{label}] visible={visible}, matches_target={ok}, hrefs={links}')

    print('\nResume target status checks:')
    resume_target_ok = True
    for label, url, code, err in resume_target_checks:
        ok = (err is None and code is not None and code < 400)
        resume_target_ok = resume_target_ok and ok
        print(f'- [{label}] url={url}, status={code}, err={err}, ok={ok}')

    print('\nExternal link failures (non-blocking):')
    if failed_external:
        for item in failed_external:
            print(' -', item)
    else:
        print(' - none')

    print('\nInternal link failures (blocking):')
    if failed_internal:
        for item in failed_internal:
            print(' -', item)
    else:
        print(' - none')

    if not resume_ok:
        print('\nFAIL: Resume link assertion failed.')
        return 2
    if not resume_target_ok:
        print('\nFAIL: Resume target URL is not reachable.')
        return 3
    if failed_internal:
        print('\nFAIL: Internal broken links detected.')
        return 1
    print('\nPASS: No internal broken links detected and resume assertion passed.')
    return 0

if __name__ == '__main__':
    sys.exit(run())
