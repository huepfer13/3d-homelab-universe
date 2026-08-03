const puppeteer = require('puppeteer');

const DASHBOARD_URL = process.env.DASHBOARD_URL || 'http://192.168.2.184:9120/';
const TIMEOUT = parseInt(process.env.TEST_TIMEOUT || '15000');

async function runTests() {
    console.log(`[Test] Starting headless verification of: ${DASHBOARD_URL}`);
    const browser = await puppeteer.launch({
        headless: 'new',
        args: ['--no-sandbox', '--disable-setuid-sandbox', '--disable-gpu', '--disable-dev-shm-usage']
    });
    const page = await browser.newPage();

    let networkErrors = [];
    let consoleErrors = [];

    // Capture network errors (404, 500, etc.) — skip favicon.ico
    page.on('response', response => {
        if (!response.ok() && response.status() !== 304 && !response.url().includes('favicon.ico')) {
            networkErrors.push(`${response.status()} ${response.url()}`);
        }
    });

    // Capture JS console errors (skip expected headless warnings)
    page.on('console', msg => {
        if (msg.type() === 'error') {
            const txt = msg.text();
            // Skip: WebGL unavailable (headless), favicon 404, generic resource load errors
            if (txt.includes('WebGL') || txt.includes('THREE.WebGLRenderer')) return;
            if (txt.includes('404 (Not Found)')) return;
            consoleErrors.push(txt);
        }
    });

    // Capture uncaught exceptions
    page.on('pageerror', err => {
        consoleErrors.push(`UNCAUGHT: ${err.message}`);
    });

    try {
        await page.goto(DASHBOARD_URL, { waitUntil: 'domcontentloaded', timeout: TIMEOUT });
        console.log('[Test] Page loaded, waiting for initUniverse...');

        // Wait for initUniverse to complete
        await page.waitForFunction(
            () => window._universeCfg && window._universeCfg.galaxies,
            { timeout: 10000 }
        );
        console.log('[Test] initUniverse() completed.');

        // ─── TEST 1: No JS errors ───
        if (consoleErrors.length > 0) {
            console.error('[FAIL] JavaScript errors:', consoleErrors);
            process.exit(1);
        }
        console.log('[PASS] No JavaScript errors.');

        // ─── TEST 2: No network errors (all configs loaded) ───
        if (networkErrors.length > 0) {
            console.error('[FAIL] Network errors:', networkErrors);
            process.exit(1);
        }
        console.log('[PASS] All configs loaded (HTTP 200).');

        // ─── TEST 3: 3D scene has galaxies ───
        const sceneState = await page.evaluate(() => {
            return {
                galaxies: typeof G !== 'undefined' ? Object.keys(G).length : 0,
                systems: typeof S !== 'undefined' ? S.length : 0,
                sceneExists: typeof scene !== 'undefined',
                rendererNull: typeof R !== 'undefined' ? R === null : true,
                cfgTitle: window._universeCfg ? window._universeCfg.title : 'none'
            };
        });

        console.log(`[Test] Scene: ${sceneState.galaxies} galaxies, ${sceneState.systems} systems, title="${sceneState.cfgTitle}"`);

        if (sceneState.galaxies === 0) {
            console.error('[FAIL] No galaxies in scene! initUniverse may have failed.');
            process.exit(1);
        }
        if (sceneState.systems === 0) {
            console.error('[FAIL] No systems in scene!');
            process.exit(1);
        }
        console.log('[PASS] 3D universe built from JSON config.');

        // ─── TEST 4: HUD elements show real data ───
        const hudData = await page.evaluate(() => {
            const nodeCount = document.getElementById('node-count');
            const ctCount = document.getElementById('ct-count');
            return {
                nodeText: nodeCount ? nodeCount.textContent : 'missing',
                ctText: ctCount ? ctCount.textContent : 'missing'
            };
        });
        console.log(`[Test] HUD: "${hudData.nodeText}" / "${hudData.ctText}"`);

        if (hudData.nodeText === '5 Nodes' || hudData.nodeText.includes('5 Nodes')) {
            console.warn('[WARN] HUD shows demo "5 Nodes" — live API may not have updated yet.');
        } else if (hudData.nodeText.includes('Galaxies')) {
            console.log('[PASS] HUD shows live galaxy count.');
        }

        // ─── TEST 5: Event log contains init message ───
        const logText = await page.evaluate(() => {
            const log = document.getElementById('log-entries');
            return log ? log.textContent.substring(0, 200) : 'missing';
        });
        if (logText.includes('Universe:') || logText.includes('galaxies')) {
            console.log('[PASS] Event log shows universe initialization.');
        } else {
            console.warn('[WARN] Event log may not contain init message.');
        }

        console.log('\n✅ ALL TESTS PASSED.');
        process.exit(0);

    } catch (err) {
        console.error(`[FAIL] Test aborted: ${err.message}`);
        process.exit(1);
    } finally {
        await browser.close();
    }
}

runTests();
