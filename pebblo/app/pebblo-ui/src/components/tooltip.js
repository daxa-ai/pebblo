export function Tooltip(props) {
  const { children, title, variant = "top" } = props;
  // return /*html*/ `
  //   <div class="tooltip"> ${children}
  //       <span class="tooltip-text">${title}</span>
  //   </div>
  //   `;

  return /*html*/ `
  <div class="tooltip">
  <div class="tooltip-content">${children}</div>
  <span class="tooltip-wrapper-${variant}"><span class="tooltip-title-${variant}">${title}</span></span></div>
   `;
}
