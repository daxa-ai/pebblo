const MEDIA_URL = document.scripts[0].getAttribute("staticURL");

export function Button({
  variant = "text",
  btnText,
  startIcon,
  endIcon,
  href,
  style,
}) {
  if (href) {
    return `
    <a href="${href}" class="link w-fit">
      <button class="relative ${variant}" style="${style}">
          <div class="flex gap-1 items-center">
          ${
            startIcon
              ? `<img src="${MEDIA_URL}${startIcon}" alt="Start Icon" />`
              : ``
          }
          <span>${btnText}</span>
          ${
            endIcon ? `<img src="${MEDIA_URL}${endIcon}" alt="End Icon" />` : ``
          }
          </div>
        </button>
    </a>  
        `;
  }

  return `<button class="relative ${variant}">
        <div class="flex gap-1 items-center">
        ${
          startIcon
            ? `<img src="${MEDIA_URL}${startIcon}" alt="Start Icon" />`
            : ``
        }
         <span>${btnText}</span>
         ${endIcon ? `<img src="${MEDIA_URL}${endIcon}" alt="End Icon" />` : ``}
       </div>
        </button>`;
}
