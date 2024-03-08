const LeftArrowIcon = (props) => {
    const id = props?.id || "";
    const className = props?.class || "";
    const color = props?.color || ""
    const size = props?.size || "md";
    return /*html*/`
    <svg id="${id}" class="icon-${color} ${className} icon-size-${size}" focusable="false" aria-hidden="true" viewBox="0 0 24 24" data-testid="ArrowBackOutlinedIcon" tabindex="-1" title="ArrowBackOutlined"><path d="M20 11H7.83l5.59-5.59L12 4l-8 8 8 8 1.41-1.41L7.83 13H20z"></path></svg>
    `
}
export default LeftArrowIcon
