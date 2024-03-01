import { MEDIA_URL } from "../constants/constant.js";
import { CLICK, LOAD } from "../constants/enums.js";
import { IconButton } from "./IconButton.js";

const Dialog = (props) => {
  const {
    dialogBody,
    fullWidth,
    maxWidth,
    title = "Dialog",
    btnId,
    dialogId,
  } = props;

  window.addEventListener(LOAD, function () {
    const DIALOG__BTN = document.getElementById(btnId);
    const DIALOG = document.getElementById(dialogId);
    const CLOSE__DIALOG__BUTTON = document.getElementById(
      `${dialogId}_close_modal`
    );
    DIALOG__BTN.addEventListener(CLICK, () => DIALOG.showModal());
    CLOSE__DIALOG__BUTTON.addEventListener(CLICK, () => DIALOG.close());
  });

  return /*html*/ `
    <dialog id="${dialogId}" class="flex flex-col gap-3 pt-4 pb-4 pr-4 pl-4 ${
    fullWidth ? "dialog-full" : ""
  } ${maxWidth ? `dialog-${maxWidth}` : ""}">
        <div class="flex justify-between items-center">
          <div class="font-16 inter medium surface-10">${title}</div>
          ${IconButton({
            id: `${dialogId}_close_modal`,
            children: `
              <img
                src="${MEDIA_URL}/static/close.png"
                alt="Close icon"
                height="14"
                width="14"
                class="cursor-pointer"
              />
            `,
          })}
        </div>
        <div class="dialog-body">${dialogBody}</div>
    </dialog>`;
};

export default Dialog;
