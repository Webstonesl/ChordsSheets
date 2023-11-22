function getCaretCharacterOffsetWithin(element) {
    var caretOffset = 0;
    var doc = element.ownerDocument || element.document;
    var win = doc.defaultView || doc.parentWindow;
    var sel;
    if (typeof win.getSelection != "undefined") {
        sel = win.getSelection();
        if (sel.rangeCount > 0) {
            var range = win.getSelection().getRangeAt(0);
            var preCaretRange = range.cloneRange();
            preCaretRange.selectNodeContents(element);
            preCaretRange.setEnd(range.endContainer, range.endOffset);
            caretOffset = preCaretRange.toString().length;
        }
    } else if ( (sel = doc.selection) && sel.type != "Control") {
        var textRange = sel.createRange();
        var preCaretTextRange = doc.body.createTextRange();
        preCaretTextRange.moveToElementText(element);
        preCaretTextRange.setEndPoint("EndToEnd", textRange);
        caretOffset = preCaretTextRange.text.length;
    }
    return caretOffset;
}
class SectionEditableElement extends HTMLElement {
    constructor() {
        super()
        this.contentEditable = true
        this.spellcheck = false
        this.addEventListener("beforeinput",this.beforeinput)
    }
    beforeinput(event) {
        if (event.inputType==="insertText") {

            if (event.data === "\\") {
                this.createChord(event)
                event.preventDefault();
                return
            }
        }
        if (event.inputType === "insertParagraph") {
            event.preventDefault()
            this.handleReturn()
            return;
        }
        if (event.inputType ==="deleteContentBackward") {
            if (this.parentNode.children.length>1)
            if(this.innerText === "") {
                this.previousElementSibling.focus()

                this.remove()
                event.preventDefault()
                return
            }

        }

        console.log(event)

    }
    
    createChord(event) {
        let n = getCaretCharacterOffsetWithin(this)
        let i = 0
        let sibling = this.nextSibling;
        let line = this.parentElement;
        while ((i<this.childNodes.length)&&(this.childNodes[i].textContent.length<n)) {
            n -= this.childNodes[i].textContent.length;
            i++;
            
        }
        if (n > 0) {
            if (i < this.childNodes.length ) {
                this.childNodes[i].splitText(n)
            }
            i++;
        }

        
        
        let chord = new SectionChordElement()
        let txt = new SectionTextElement()
        
        line.insertBefore(chord,sibling)
        while(i<this.childNodes.length) {
            txt.append(this.childNodes[i])
        }
        line.append(txt)
        chord.focus()
    }
    
}
class SectionTextElement extends SectionEditableElement {
    constructor() {
        super()
    }
    handleReturn() {
        console.log("text")
    }
    
}

class SectionChordElement extends SectionEditableElement {
    constructor() {
        super()
    }
    handleReturn() {
        let ns = this.nextSibling
        ns.focus()
    }
}

class SectionLineElement extends HTMLElement {
    constructor() {
        super()
        if (!this.hasChildNodes()) {
            let text = new SectionTextElement()
            this.appendChild(text)
        }
    }
}

class SectionContentElement extends HTMLElement {
    static n = 0;
    constructor() {
        super()
        this.value = this.n++;
        if (!this.hasChildNodes()) {
            let line = new SectionLineElement()
            this.appendChild(line)
        }
    }
    
}
window.customElements.define('section-chord',SectionChordElement)
window.customElements.define('section-text',SectionTextElement)
window.customElements.define('section-line',SectionLineElement)
window.customElements.define('section-content',SectionContentElement)
