import { MEDIA_URL } from "../constants/constant.js";

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
    style,
  } = props;

  return /*html*/ `
  <button ${id ? `id="${id}"` : ""} class="relative ${variant} ${
    className ? className : ""
  }" style="${style}">
        <div class="flex gap-1 items-center">
        ${
          startIcon
            ? `<img src="${MEDIA_URL}${startIcon}" alt="Start Icon" />`
            : ""
        }
         <span>${btnText}</span>
         ${endIcon ? `<img src="${MEDIA_URL}${endIcon}" alt="End Icon" />` : ""}
       </div>
  </button>`;
};
