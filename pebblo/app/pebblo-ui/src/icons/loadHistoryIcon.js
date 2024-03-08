const LoadHistoryIcon = (props) => {
    const id = props?.id || "";
    const className = props?.class || "";
    const color = props?.color || "";
    const size = props?.size || "md";
    return /*html*/`<svg id="${id}"  class="icon-${color} ${className} icon-size-${size}" focusable="false" aria-hidden="true" viewBox="0 0 24 24" data-testid="HistoryOutlinedIcon" tabindex="-1" title="HistoryOutlined" style="
    "><path d="M13 3c-4.97 0-9 4.03-9 9H1l3.89 3.89.07.14L9 12H6c0-3.87 3.13-7 7-7s7 3.13 7 7-3.13 7-7 7c-1.93 0-3.68-.79-4.94-2.06l-1.42 1.42C8.27 19.99 10.51 21 13 21c4.97 0 9-4.03 9-9s-4.03-9-9-9m-1 5v5l4.25 2.52.77-1.28-3.52-2.09V8z"></path></svg>`
}

export default LoadHistoryIcon