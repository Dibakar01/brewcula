// brewCula: a menu bar toggle that keeps your Mac up all night.
//
// It takes the same four power assertions as `caffeinate -dims`, directly through IOKit,
// so there is no child process and the app can run inside the App Sandbox with zero
// entitlements: no network, no files, no privileges; one optional login item.
// macOS drops every assertion when the process exits, so a quit or a crash can never
// leave your Mac stuck awake.
//
// Click the mug: toggle. Right-click or Control-click: menu.
//
// Flags (used by install.sh): --setup turns on Open at Login and shows a one-time welcome
// bubble; --remove-login-item turns it off and exits; --check runs the self-test.
import Cocoa
import IOKit.pwr_mgt
import ServiceManagement

// caffeinate -d, -i, -m, -s. The last one only has an effect on AC power (macOS rule, not ours).
let assertionKinds = [
    kIOPMAssertionTypePreventUserIdleDisplaySleep,
    kIOPMAssertionTypePreventUserIdleSystemSleep,
    "PreventDiskIdle",
    kIOPMAssertionTypePreventSystemSleep,
]

final class BrewCula: NSObject, NSApplicationDelegate {
    let item = NSStatusBar.system.statusItem(withLength: NSStatusItem.squareLength)
    var assertions: [IOPMAssertionID] = []
    var since = Date()
    var steam: CGFloat = 0          // 0 = cold mug, 1 = steaming. Drives the icon.
    var animation: Timer?
    var on: Bool { !assertions.isEmpty }

    func applicationDidFinishLaunching(_ n: Notification) {
        guard let b = item.button else { return }
        b.target = self
        b.action = #selector(click)
        b.sendAction(on: [.leftMouseUp, .rightMouseUp])
        render()
        if CommandLine.arguments.contains("--setup") {
            setOpenAtLogin(true)
            DispatchQueue.main.asyncAfter(deadline: .now() + 0.4) { self.welcome() }
        }
    }

    func applicationWillTerminate(_ n: Notification) { setAwake(false) }

    @objc func click() {
        let e = NSApp.currentEvent
        let wantsMenu = e?.type == .rightMouseUp || e?.modifierFlags.contains(.control) == true
        guard wantsMenu else { return toggle() }
        let m = NSMenu()
        let status = NSMenuItem(title: statusLine(), action: nil, keyEquivalent: "")
        status.isEnabled = false
        m.addItem(status)
        m.addItem(.separator())
        m.addItem(withTitle: on ? "Allow Sleep" : "Keep Awake", action: #selector(toggle), keyEquivalent: "").target = self
        m.addItem(.separator())
        if #available(macOS 13, *) {
            let login = NSMenuItem(title: "Open at Login", action: #selector(toggleOpenAtLogin), keyEquivalent: "")
            login.target = self
            login.state = SMAppService.mainApp.status == .enabled ? .on : .off
            m.addItem(login)
        }
        m.addItem(withTitle: "Quit brewCula", action: #selector(NSApplication.terminate(_:)), keyEquivalent: "q")
        item.menu = m
        item.button?.performClick(nil)
        item.menu = nil
    }

    @objc func toggle() {
        setAwake(!on)
        animateSteam(to: on ? 1 : 0)
    }

    @objc func toggleOpenAtLogin() {
        if #available(macOS 13, *) { setOpenAtLogin(SMAppService.mainApp.status != .enabled) }
    }

    // A plain login item through ServiceManagement (macOS 13+). macOS shows its own notice
    // and lists it in System Settings > General > Login Items, where you can also remove it.
    func setOpenAtLogin(_ enabled: Bool) {
        guard #available(macOS 13, *) else { return }
        let s = SMAppService.mainApp
        try? enabled ? s.register() : s.unregister()
    }

    // First-run bubble under the mug, so a menu bar app isn't invisible after install.
    func welcome() {
        guard let b = item.button else { return }
        let p = NSPopover()
        p.behavior = .transient
        p.contentViewController = NSViewController()
        p.contentViewController?.view = welcomeView()
        NSApp.activate(ignoringOtherApps: true)
        p.show(relativeTo: b.bounds, of: b, preferredEdge: .minY)
        DispatchQueue.main.asyncAfter(deadline: .now() + 12) { p.performClose(nil) }
    }

    func setAwake(_ awake: Bool) {
        if awake == on { return }
        if awake {
            for kind in assertionKinds {
                var id = IOPMAssertionID(0)
                let r = IOPMAssertionCreateWithName(kind as CFString, IOPMAssertionLevel(kIOPMAssertionLevelOn),
                                                    "brewCula is keeping this Mac awake" as CFString, &id)
                if r == kIOReturnSuccess { assertions.append(id) }
            }
            since = Date()
        } else {
            assertions.forEach { IOPMAssertionRelease($0) }
            assertions = []
        }
    }

    func statusLine() -> String {
        guard on else { return "Your Mac can sleep normally" }
        let s = Date().timeIntervalSince(since)
        if s < 60 { return "Awake for under a minute" }
        let f = DateComponentsFormatter()
        f.allowedUnits = [.hour, .minute]
        f.unitsStyle = .abbreviated
        return "Awake for " + (f.string(from: s) ?? "a while")
    }

    // Steam rises slowly (450 ms) and leaves quickly (180 ms). Reduce Motion: no animation.
    func animateSteam(to target: CGFloat) {
        animation?.invalidate()
        let from = steam, duration = target > from ? 0.45 : 0.18
        if NSWorkspace.shared.accessibilityDisplayShouldReduceMotion { steam = target; return render() }
        let start = CACurrentMediaTime()
        let t = Timer(timeInterval: 1.0 / 60, repeats: true) { [weak self] t in
            guard let self else { return t.invalidate() }
            let p = min(1, (CACurrentMediaTime() - start) / duration)
            self.steam = from + (target - from) * CGFloat(1 - pow(1 - p, 3))   // ease-out cubic
            self.render()
            if p >= 1 { t.invalidate() }
        }
        RunLoop.main.add(t, forMode: .common)
        animation = t
    }

    func render() {
        guard let b = item.button else { return }
        b.image = mugIcon(awake: on, steam: steam)
        b.toolTip = on ? "brewCula is keeping your Mac awake. Click to let it sleep."
                       : "Click to keep your Mac awake."
        b.setAccessibilityLabel(on ? "brewCula, keeping Mac awake" : "brewCula, sleep allowed")
    }
}

// The menu bar icon: brewCula's mug, kept plain so it reads at 18 points. Template image, so macOS tints it for light,
// dark and tinted menu bars. Awake: filled, eyes open, steam. Asleep: outline, eyes closed.
func mugIcon(awake: Bool, steam: CGFloat) -> NSImage {
    let img = NSImage(size: NSSize(width: 18, height: 18), flipped: false) { _ in
        NSColor.black.set()
        let body = NSBezierPath(roundedRect: NSRect(x: 2.6, y: 1.4, width: 9.8, height: 9.4), xRadius: 2.2, yRadius: 2.2)
        let handle = NSBezierPath()
        handle.move(to: NSPoint(x: 12.4, y: 8.6))
        handle.curve(to: NSPoint(x: 12.4, y: 3.6), controlPoint1: NSPoint(x: 16.4, y: 8.8), controlPoint2: NSPoint(x: 16.4, y: 3.4))
        handle.lineWidth = 1.5
        handle.lineCapStyle = .round
        handle.stroke()
        let ctx = NSGraphicsContext.current
        if awake {
            body.fill()
            ctx?.compositingOperation = .clear                         // punch the eyes out
            NSBezierPath(ovalIn: NSRect(x: 4.6, y: 5.4, width: 2.0, height: 2.5)).fill()
            NSBezierPath(ovalIn: NSRect(x: 8.4, y: 5.4, width: 2.0, height: 2.5)).fill()
            ctx?.compositingOperation = .sourceOver
        } else {
            NSBezierPath(roundedRect: NSRect(x: 3.35, y: 2.15, width: 8.3, height: 7.9), xRadius: 1.6, yRadius: 1.6).stroke()
            for x in [4.4, 8.2] {                                        // sleepy eyes
                let eye = NSBezierPath()
                eye.move(to: NSPoint(x: x, y: 6.6))
                eye.curve(to: NSPoint(x: x + 2.4, y: 6.6), controlPoint1: NSPoint(x: x + 0.6, y: 5.6), controlPoint2: NSPoint(x: x + 1.8, y: 5.6))
                eye.lineWidth = 1.2
                eye.lineCapStyle = .round
                eye.stroke()
            }
        }
        guard steam > 0.01 else { return true }
        NSGraphicsContext.saveGraphicsState()
        NSRect(x: 0, y: 0, width: 18, height: 11.6 + 6.4 * steam).clip()  // rises as it appears
        NSColor.black.withAlphaComponent(steam).set()
        for x in [6.2, 8.9] {
            let w = NSBezierPath()
            w.move(to: NSPoint(x: x, y: 11.8))
            w.curve(to: NSPoint(x: x, y: 17.4), controlPoint1: NSPoint(x: x - 1.6, y: 13.6), controlPoint2: NSPoint(x: x + 1.6, y: 15.6))
            w.lineWidth = 1.2
            w.lineCapStyle = .round
            w.stroke()
        }
        NSGraphicsContext.restoreGraphicsState()
        return true
    }
    img.isTemplate = true
    img.accessibilityDescription = awake ? "Steaming mug" : "Sleeping mug"
    return img
}

func welcomeView() -> NSView {
    let icon = NSImageView(image: NSApp.applicationIconImage ?? NSImage())
    icon.widthAnchor.constraint(equalToConstant: 52).isActive = true
    icon.heightAnchor.constraint(equalToConstant: 52).isActive = true
    let title = NSTextField(labelWithString: "brewCula is up here")
    title.font = .boldSystemFont(ofSize: 13)
    var lines = "Click the mug to keep your Mac awake.\nClick again to let it sleep."
    if #available(macOS 13, *) { lines += "\nIt opens at login. Right-click the mug to change that." }
    let body = NSTextField(wrappingLabelWithString: lines)
    body.font = .systemFont(ofSize: 12)
    body.textColor = .secondaryLabelColor
    body.preferredMaxLayoutWidth = 330
    let text = NSStackView(views: [title, body])
    text.orientation = .vertical
    text.alignment = .leading
    text.spacing = 4
    let row = NSStackView(views: [icon, text])
    row.alignment = .top
    row.spacing = 12
    row.edgeInsets = NSEdgeInsets(top: 14, left: 14, bottom: 14, right: 16)
    return row
}

let app = NSApplication.shared
let brewcula = BrewCula()
app.delegate = brewcula
app.setActivationPolicy(.accessory)

// `brewCula.app/Contents/MacOS/brewCula --check`: proves the toggle takes and releases exactly the
// four assertions, and that the app is running inside the sandbox. No UI needed.
if CommandLine.arguments.contains("--remove-login-item") {
    brewcula.setOpenAtLogin(false)
    exit(0)
}

if CommandLine.arguments.contains("--check") {
    func held() -> Int {
        var d: Unmanaged<CFDictionary>?
        IOPMCopyAssertionsByProcess(&d)
        let all = d?.takeRetainedValue() as? [NSNumber: [Any]] ?? [:]
        return all[NSNumber(value: getpid())]?.count ?? 0
    }
    precondition(ProcessInfo.processInfo.environment["APP_SANDBOX_CONTAINER_ID"] != nil, "not sandboxed")
    precondition(held() == 0, "assertions held before toggle")
    brewcula.toggle()
    precondition(brewcula.on && held() == assertionKinds.count, "expected \(assertionKinds.count) assertions, got \(held())")
    brewcula.toggle()
    precondition(!brewcula.on && held() == 0, "assertions not released: \(held())")
    print("OK: sandboxed, took \(assertionKinds.count) assertions, released all")
    exit(0)
}

app.run()
