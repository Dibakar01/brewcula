import { useEffect, useRef, useState } from 'react';
import { useReducedMotion } from 'motion/react';
import RotatingText from './bits/RotatingText';
import CircularText from './bits/CircularText';
import ClickSpark from './bits/ClickSpark';
import awakeSrc from './art/mascot-awake.svg';
import asleepSrc from './art/mascot-asleep.svg';
import stageSrc from './art/stage.svg';

const REPO = 'https://github.com/Dibakar01/brewcula';
const RAW = 'https://raw.githubusercontent.com/Dibakar01/brewcula/main/install.sh';
const INSTALL = `curl -fsSL ${RAW} | sh`;

type Wake = 'idle' | 'awake' | 'unsupported' | 'refused';
const STATUS: Record<Wake, string> = {
  idle: 'Click the mug to keep this screen awake while the tab is open.',
  awake: 'This tab is keeping your screen awake. Click again to let it sleep.',
  unsupported: "Your browser can't hold a wake lock. The app can.",
  refused: "Your browser said no this time. The app doesn't need to ask."
};

function useWakeLock() {
  const [state, setState] = useState<Wake>('idle');
  const lock = useRef<WakeLockSentinel | null>(null);
  const want = useRef(false);

  const acquire = async () => {
    if (!('wakeLock' in navigator)) return setState('unsupported');
    try {
      lock.current = await navigator.wakeLock.request('screen');
      // The browser drops the lock when the tab is hidden; we take it back on return.
      lock.current.addEventListener('release', () => { if (!want.current) setState('idle'); });
      setState('awake');
    } catch {
      want.current = false;
      setState('refused');
    }
  };

  useEffect(() => {
    const onVisible = () => { if (want.current && document.visibilityState === 'visible') acquire(); };
    document.addEventListener('visibilitychange', onVisible);
    return () => { document.removeEventListener('visibilitychange', onVisible); lock.current?.release(); };
  }, []);

  const toggle = () => {
    if (want.current) {
      want.current = false;
      lock.current?.release();
      lock.current = null;
      setState('idle');
    } else {
      want.current = true;
      acquire();
    }
  };
  return [state, toggle] as const;
}

function Code({ children }: { children: string }) {
  return <pre className="code"><code>{children}</code></pre>;
}

function CopyInstall({ reduce }: { reduce: boolean }) {
  const [label, setLabel] = useState('Copy');
  const text = useRef<HTMLElement>(null);

  const copy = async () => {
    try {
      await navigator.clipboard.writeText(INSTALL);
      setLabel('Copied');
    } catch {
      const r = document.createRange();
      r.selectNodeContents(text.current!);
      getSelection()?.removeAllRanges();
      getSelection()?.addRange(r);
      setLabel('Press ⌘C');
    }
    setTimeout(() => setLabel('Copy'), 2400);
  };

  return (
    <div className="install">
      <code ref={text}><span aria-hidden="true">$ </span>{INSTALL}</code>
      <ClickSpark disabled={reduce} sparkColor="#d92819" sparkCount={10} sparkRadius={22} style={{ width: 'auto', height: 'auto' }}>
        <button type="button" className="btn" onClick={copy}>
          <span aria-live="polite">{label}</span>
        </button>
      </ClickSpark>
    </div>
  );
}

export default function App() {
  const reduce = useReducedMotion() ?? false;
  const [wake, toggle] = useWakeLock();
  const awake = wake === 'awake';

  return (
    <>
      <header className="nav wrap">
        <a className="brand" href="./">
          <img src={awakeSrc} alt="" width="30" height="31" />
          brewCula
        </a>
        <a className="link" href={REPO}>GitHub</a>
      </header>

      <main>
        <section className="hero wrap">
          <div className="hero__copy">
            <h1>
              Keep your Mac awake for{' '}
              <RotatingText
                texts={['the download.', 'the render.', 'the build.', 'the call.']}
                effect="slide"
                highlight
                highlightColor="#d92819"
                auto={!reduce}
                rotationInterval={2400}
                staggerDuration={0.02}
                mainClassName="rotator"
              />
            </h1>
            <p className="lede">A menu bar mug that does what <code>caffeinate -dims</code> does. Sandboxed, one click, nothing else.</p>
            <CopyInstall reduce={reduce} />
            <p className="small">
              No admin password. Installs to <code>~/Applications</code> and opens at login on macOS 13+.{' '}
              <a className="link" href={`${REPO}/blob/main/install.sh`}>Read the script</a> or{' '}
              <a className="link" href={REPO}>view source</a>.
            </p>
          </div>

          <div className="stage" style={{ backgroundImage: `url(${stageSrc})` }}>
            <CircularText
              text="CLICK THE MUG ✦ NO SUDO ✦ NO NETWORK ✦ "
              size={300}
              fontSize={15}
              letterSpacing={2}
              spinDuration={awake ? 8 : 26}
              onHover="slowDown"
              color="#fdf3f2"
            >
              <button
                type="button"
                className={`mug${awake ? ' is-awake' : ''}`}
                aria-pressed={awake}
                aria-label="Keep this screen awake"
                onClick={toggle}
              >
                <img src={awake ? awakeSrc : asleepSrc} alt="" width="128" height="132" />
              </button>
            </CircularText>
            <p className="status" aria-live="polite">{STATUS[wake]}</p>
          </div>
        </section>

        <section className="wrap split reveal">
          <div>
            <h2>It can't do anything else.</h2>
            <p>
              brewCula runs inside the macOS App Sandbox with nothing granted. macOS enforces that, not this page.
              Check your own copy:
            </p>
            <Code>codesign -d --entitlements - ~/Applications/brewCula.app</Code>
            <p className="small">The only key it prints is <code>com.apple.security.app-sandbox</code>.</p>
          </div>
          <ul className="rules">
            <li className="can">keep the display and the Mac awake</li>
            <li className="can">keep disks from spinning down</li>
            <li className="can">open at login, if you leave that on</li>
            <li className="cant"><s>open a network connection</s></li>
            <li className="cant"><s>read or write your files</s></li>
            <li className="cant"><s>install a background daemon</s></li>
            <li className="cant"><s>ask for your password</s></li>
          </ul>
        </section>

        <section className="wrap reveal">
          <h2>How it works</h2>
          <p className="intro">
            The same four power assertions as <code>caffeinate -dims</code>, asked for directly through IOKit. When it
            quits, macOS drops them with the process, so it can't leave your Mac stuck awake.
          </p>
          <div className="tiles">
            <article className="tile tile--ink">
              <b>-d</b><span>PreventUserIdleDisplaySleep</span><p>The display stays lit.</p>
            </article>
            <article className="tile tile--red">
              <b>-i</b><span>PreventUserIdleSystemSleep</span><p>The Mac doesn't idle to sleep.</p>
            </article>
            <article className="tile tile--paper">
              <b>-m</b><span>PreventDiskIdle</span><p>Disks keep spinning.</p>
            </article>
            <article className="tile tile--blush">
              <b>-s</b><span>PreventSystemSleep</span><p>No system sleep on AC power. That part is a macOS rule.</p>
            </article>
          </div>
          <p className="small">Watch them come and go as you click:</p>
          <Code>pmset -g assertions | grep brewCula</Code>
        </section>

        <section className="wrap ways reveal">
          <h2>Other ways in</h2>
          <div className="ways__grid">
            <div>
              <h3>Download the zip</h3>
              <p>
                From <a className="link" href={`${REPO}/releases/latest`}>the latest release</a>. It isn't notarized, so
                macOS blocks it once: System Settings › Privacy &amp; Security › Open Anyway.
              </p>
              <Code>gh attestation verify brewCula-1.0.0.zip --repo Dibakar01/brewcula</Code>
            </div>
            <div>
              <h3>Build it yourself</h3>
              <p>One Swift file. Xcode Command Line Tools, nothing else.</p>
              <Code>{`git clone ${REPO} && cd brewcula\n./build.sh\nbuild/brewCula.app/Contents/MacOS/brewCula --check`}</Code>
            </div>
            <div>
              <h3>Uninstall</h3>
              <p>Removes the app and its login item.</p>
              <Code>{`curl -fsSL ${RAW} | sh -s -- --uninstall`}</Code>
            </div>
          </div>
        </section>
      </main>

      <footer className="wrap foot">
        <span>MIT licensed. Made because <code>caffeinate</code> deserved a cape.</span>
        <span>
          <a className="link" href={REPO}>GitHub</a> · Text effects from{' '}
          <a className="link" href="https://reactbits.dev">React Bits</a>
        </span>
      </footer>
    </>
  );
}
