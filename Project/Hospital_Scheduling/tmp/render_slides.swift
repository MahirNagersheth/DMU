import AppKit
import WebKit
import Foundation

// Local artifact renderer: loads only the authored HTML file into an offscreen view.
let root = URL(fileURLWithPath: "/Users/mahir/Downloads/DMU/Project/Hospital_Scheduling")
let output = root.appendingPathComponent("tmp/rendered")
try! FileManager.default.createDirectory(at: output, withIntermediateDirectories: true)
let app = NSApplication.shared
app.setActivationPolicy(.prohibited)
let config = WKWebViewConfiguration()
config.websiteDataStore = .nonPersistent()
let web = WKWebView(frame: NSRect(x:0,y:0,width:1280,height:720), configuration:config)
let win = NSWindow(contentRect:NSRect(x:0,y:0,width:1280,height:720),styleMask:[.borderless],backing:.buffered,defer:false)
win.contentView = web
win.orderBack(nil)

class Renderer: NSObject, WKNavigationDelegate {
    var page=0
    var checks:[Any]=[]
    func webView(_ webView: WKWebView, didFinish navigation: WKNavigation!) { render() }
    func render() {
        if page==11 {
            let data=try! JSONSerialization.data(withJSONObject:checks,options:[.prettyPrinted,.sortedKeys])
            try! data.write(to:output.appendingPathComponent("layout.json"))
            print("Rendered all 11 slides at 1280x720.")
            exit(0)
        }
        let js = """
        document.body.classList.add('rendering');show(\(page));
        JSON.stringify((()=>{const s=document.querySelector('.slide.active');return {slide:\(page+1),title:s.querySelector('h1,h2').innerText,items:[...s.querySelectorAll('header, h1,h2,h3,p,table,blockquote,.human-line,.takeaway,.legend,.badge,.closing-flow,.closing-evidence,.night-counts,.rules-row,.scorecard tr')].filter(e=>e.getClientRects().length&& !e.closest('.notes')).map(e=>{let r=e.getBoundingClientRect();return {tag:e.tagName,class:e.className,text:e.innerText,x:r.x,y:r.y,w:r.width,h:r.height,scrollW:e.scrollWidth,clientW:e.clientWidth,scrollH:e.scrollHeight,clientH:e.clientHeight}})}})());
        """
        web.evaluateJavaScript(js) { result,error in
            if let error=error {print(error);exit(2)}
            if let str=result as? String, let data=str.data(using:.utf8),let obj=try? JSONSerialization.jsonObject(with:data) {self.checks.append(obj)}
            DispatchQueue.main.asyncAfter(deadline:.now()+0.15) {
                let c=WKSnapshotConfiguration();c.rect=CGRect(x:0,y:0,width:1280,height:720);c.snapshotWidth=1280
                web.takeSnapshot(with:c) { image,error in
                    guard let image=image else {print("Snapshot failed: \(String(describing:error))");exit(3)}
                    let bitmap=NSBitmapImageRep(bitmapDataPlanes:nil,pixelsWide:1280,pixelsHigh:720,bitsPerSample:8,samplesPerPixel:4,hasAlpha:true,isPlanar:false,colorSpaceName:.deviceRGB,bytesPerRow:0,bitsPerPixel:0)!
                    NSGraphicsContext.saveGraphicsState();NSGraphicsContext.current=NSGraphicsContext(bitmapImageRep:bitmap)
                    image.draw(in:NSRect(x:0,y:0,width:1280,height:720));NSGraphicsContext.restoreGraphicsState()
                    try! bitmap.representation(using:.png,properties:[:])!.write(to:output.appendingPathComponent(String(format:"slide-%02d.png",self.page+1)))
                    print("Slide \(self.page+1)")
                    self.page+=1;self.render()
                }
            }
        }
    }
}
let renderer=Renderer();web.navigationDelegate=renderer
web.loadFileURL(root.appendingPathComponent("presentation.html"),allowingReadAccessTo:root)
DispatchQueue.main.asyncAfter(deadline:.now()+50) {print("Renderer timed out");exit(4)}
app.run()
