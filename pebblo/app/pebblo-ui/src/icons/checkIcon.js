const CheckIcon = (props) => {
    const id = props?.id || "";
    const className = props?.class || "";
    const color = props?.color || "";
    const size = props?.size || "md";
    return /*html*/`<svg id="${id}" class="icon-${color} ${className} icon-size-${size}" focusable="false" aria-hidden="true" viewBox="0 0 24 24" data-testid="CheckIcon" tabindex="-1" title="Check"><path d="M9 16.17 4.83 12l-1.42 1.41L9 19 21 7l-1.41-1.41z"></path></svg>`
}

export default CheckIcon