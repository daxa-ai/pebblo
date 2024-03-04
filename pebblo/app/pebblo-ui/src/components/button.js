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
    className,
    style = '',
    color = "primary"
  } = props;

  return /*html*/ `
  <button ${id ? `id="${id}"` : ""} class="btn btn-${variant}-${color} ${className ? className : ""
    } relative" style="${style}">
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
