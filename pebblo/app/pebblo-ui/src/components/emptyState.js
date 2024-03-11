import { EMPTY_STATES } from "../constants/constant.js";
import { Button } from "./index.js";

export const EmptyState = (props) => {
  const { image, heading, subHeading, buttonNodes } =
    EMPTY_STATES[props?.variant];

  return /*html*/ `
  <div class="inter flex flex-col gap-4 justify-center items-center">
    <img src=${image} alt="pebblo" height=${180} />
    <div class="flex flex-col gap-6">
      <div class="flex flex-col gap-3">
        <div class="font-24 medium">${heading}</div>
        <div class="font-16 surface-80">${subHeading}</div>
      </div>
      ${
        buttonNodes?.length
          ? `<div class="flex justify-center gap-2">
            ${buttonNodes?.myMap((btnDetails) => Button({ ...btnDetails }))}
          </div>`
          : ""
      }
    </div>
  </div>`;
};
