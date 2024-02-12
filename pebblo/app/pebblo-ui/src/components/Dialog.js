import { MEDIA_URL } from "../constants/constant.js";
import IconButton from "./IconButton.js";

const Dialog = (props) => {
  const { children, fullWidth, maxWidth } = props;
  window.addEventListener("load", function () {
    const showDialogBtn = document.getElementById("showDialogBtn");
    const dialog = document.getElementById("dialog");
    const closeDialogBtn = this.document.getElementById("close-modal");
    showDialogBtn.addEventListener("click", () => dialog.showModal());
    closeDialogBtn.addEventListener("click", () => dialog.close());
  });

  return /*html*/ `
    <dialog id="dialog" class="pt-4 pb-4 pr-4 pl-4 ${
      fullWidth ? "dialog-full" : ""
    } ${maxWidth ? `dialog-${maxWidth}` : ""}">
        <div class="flex justify-between items-center">
          <div class="font-16 inter medium surface-10">Dialog</div>
          ${IconButton({
            children: `
              <img
                src="${MEDIA_URL}/static/close.png"
                alt="Close icon"
                height="14"
                width="14"
                class="cursor-pointer"
              />
            `,
            id: "close-modal",
          })}
        </div>
    </dialog>`;
};

export default Dialog;
