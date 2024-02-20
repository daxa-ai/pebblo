export function Tooltip(props) {
  const { children, title } = props;
  return /*html*/ `
    <div class="tooltip"> ${children}
        <span class="tooltip-text">${title}</span>
    </div>
    `;
}
