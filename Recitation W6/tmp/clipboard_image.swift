import AppKit
import Foundation
import PDFKit
let destination = URL(fileURLWithPath: CommandLine.arguments[1])
let board = NSPasteboard.general
if let data = board.data(forType: .pdf), let document = PDFDocument(data: data), let page = document.page(at: 0) {
    let box = page.bounds(for: .mediaBox)
    let image = page.thumbnail(of: NSSize(width: box.width * 3, height: box.height * 3), for: .mediaBox)
    let bitmap = NSBitmapImageRep(data: image.tiffRepresentation!)!
    try bitmap.representation(using: .png, properties: [:])!.write(to: destination)
} else if let data = board.data(forType: .png) {
    try data.write(to: destination)
} else if let data = board.data(forType: .tiff), let image = NSBitmapImageRep(data: data), let png = image.representation(using: .png, properties: [:]) {
    try png.write(to: destination)
} else {
    fatalError("Excel did not supply an image to the clipboard")
}
