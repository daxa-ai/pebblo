// PROPS {
//   className:string,
//   id: string,
//   children: HTMLElement
// }
export const IconButton = (props) => {
  const { className = "", id, children } = props;
  return /*html*/ `
      <button ${id ? `id="${id}"` : ""} class="icon-button ${className}">
         ${children}
      </button>
    `;
};
