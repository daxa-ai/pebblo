// PROPS {
//   children: string | HTMLElement,
//   title: string,
//   variant?: string,
// }

export function Tooltip(props) {
  const { children, title, variant = "top", inline } = props;
  return /*html*/ `
  <span class="tooltip ${inline ? "tooltip-inline" : ""}">
  <span class="tooltip-content">${children}</span>
  <span class="tooltip-wrapper tooltip-wrapper-${variant}"><span class="tooltip-title-${variant}">${title}</span></span></span>
   `;
}
