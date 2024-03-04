const DownloadIcon = (props) => {
    const id = props?.id || "";
    const className = props?.class || "";
    const color = props?.color || "";
    const size = props?.size || "md";
    return /*html*/`<svg id="${id}"  class="icon-${color} ${className} icon-size-${size}" focusable="false" aria-hidden="true" viewBox="0 0 24 24" data-testid="FileDownloadOutlinedIcon" tabindex="-1" title="FileDownloadOutlined"><path d="M18 15v3H6v-3H4v3c0 1.1.9 2 2 2h12c1.1 0 2-.9 2-2v-3zm-1-4-1.41-1.41L13 12.17V4h-2v8.17L8.41 9.59 7 11l5 5z"></path></svg>`
}

export default DownloadIcon
