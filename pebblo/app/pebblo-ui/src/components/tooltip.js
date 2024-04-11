// PROPS {
//   children: string | HTMLElement,
//   title: string,
//   variant?: string,
// }

export function Tooltip(props) {
  const { children, title, variant = "top" } = props;
  return /*html*/ `
  <div class="tooltip">
  <div class="tooltip-content">${children}</div>
  <span class="tooltip-wrapper tooltip-wrapper-${variant}"><span class="tooltip-title-${variant}">${title}</span></span></div>
   `;
}
