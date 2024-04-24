import { CLICK, LOAD } from "../constants/enums.js";
import CloseIcon from "../icons/closeIcon.js";
import { waitForElement } from "../util.js";
import { IconButton } from "./IconButton.js";

// PROPS {
//   dialogBody: HTMLElement,
//   fullWidth?:boolean,
//   maxWidth?: string,
//   title:string,
//   btnId:string
//   dialogId: string
//  }

const Dialog = (props) => {
  const {
    dialogBody,
    fullWidth,
    maxWidth = "md",
    title = "Dialog",
    btnId,
    dialogId,
  } = props;

  waitForElement(`#${dialogId}`, 500).then(function () {
    const DIALOG__BTN = document.getElementById(btnId);
    const DIALOG = document.getElementById(dialogId);
    DIALOG.style.display = "none";
    const CLOSE__DIALOG__BUTTON = document.getElementById(
      `${dialogId}_close_modal`
    );
    DIALOG__BTN.addEventListener(CLICK, (event) => {
      event.stopPropagation();
      DIALOG.style.display = "block";
      DIALOG.showModal();
    });
    CLOSE__DIALOG__BUTTON.addEventListener(CLICK, () => {
      DIALOG.style.display = "none";
      DIALOG.close();
    });
  });

  return /*html*/ `
    <dialog id="${dialogId}" class="flex flex-col gap-3 pt-4 pb-4 pr-4 pl-4 ${
    fullWidth ? "dialog-full" : ""
  } ${maxWidth ? `dialog-${maxWidth}` : ""}">
        <div class="flex justify-between items-center">
          <div class="font-16 inter medium surface-10">${title}</div>
          ${IconButton({
            id: `${dialogId}_close_modal`,
            children: CloseIcon({ class: "cursor-pointer" }),
          })}
        </div>
        <div class="dialog-body">${dialogBody}</div>
    </dialog>`;
};

export default Dialog;
