// PROPS {
//   href?: string,
//   variant?: string,
//   btnText: string || HTMLElement,
//   startIcon?: HTMLElement,
//   endIcon?: HTMLElement,
//   id?:string,
//   className?:string,
//   style?:string,
//   color?:string,
// }

export function Button(props) {
  const { href } = props;
  if (href) {
    return /*html*/ `
    <a href="${href}" class="link w-fit">
      ${getButton(props)}
    </a>  
        `;
  }
  return getButton(props);
}

const getButton = (props) => {
  const {
    variant = "text",
    btnText,
    startIcon,
    endIcon,
    id,
    className = "",
    style = '',
    color = "primary"
  } = props;

  return /*html*/ `
  <button ${id ? `id="${id}"` : ""} class="btn btn-${variant}-${color} ${className} relative" style="${style}">
        <div class="flex gap-1 items-center">
        ${startIcon
      ? startIcon
      : ""
    }
         <span>${btnText}</span>
         ${endIcon ? endIcon : ""}
       </div>
  </button>`;
};
