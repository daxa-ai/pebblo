const StraightIcon = (props) => {
    const id = props?.id || "";
    const className = props?.class || "";
    const color = props?.color || "";
    const size = props?.size || "md";
    return /*html*/`<svg id="${id}"  class="icon-${color} ${className} icon-size-${size}" focusable="false" aria-hidden="true" viewBox="0 0 24 24" data-testid="StraightIcon" tabindex="-1" title="Straight"><path d="M11 6.83 9.41 8.41 8 7l4-4 4 4-1.41 1.41L13 6.83V21h-2z"></path></svg>`
}

export default StraightIcon