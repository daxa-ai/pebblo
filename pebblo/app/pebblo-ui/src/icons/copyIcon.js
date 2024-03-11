const CopyIcon = (props) => {
    const id = props?.id || "";
    const className = props?.class || "";
    const color = props?.color || "";
    const size = props?.size || "md";
    return /*html*/`<svg id="${id}"  class="icon-${color} ${className} icon-size-${size}" focusable="false" aria-hidden="true" viewBox="0 0 24 24" data-testid="ContentCopyIcon" tabindex="-1" title="ContentCopy"><path d="M16 1H4c-1.1 0-2 .9-2 2v14h2V3h12zm3 4H8c-1.1 0-2 .9-2 2v14c0 1.1.9 2 2 2h11c1.1 0 2-.9 2-2V7c0-1.1-.9-2-2-2m0 16H8V7h11z"></path></svg>`
}

export default CopyIcon
