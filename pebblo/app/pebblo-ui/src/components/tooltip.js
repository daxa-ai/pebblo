export function Tooltip(props) {
  const { children, title } = props;
  // return /*html*/ `
  //   <div class="tooltip"> ${children}
  //       <span class="tooltip-text">${title}</span>
  //   </div>
  //   `;

  return /*html*/ `
  <div class="tooltip">
  <div class="tooltip-content">${children}</div>
  <span class="tooltip-wrapper"><span class="tooltip-title">${title}</span></span></div>
   `;
}
