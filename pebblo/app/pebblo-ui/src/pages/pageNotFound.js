import { MEDIA_URL } from "../constants/constant.js";

export const PageNotFound = () => {
  return /*html*/ `
        <div class="inter w-100 h-full flex flex-col gap-4 items-center justify-center">
            <img src=${`${MEDIA_URL}/static/not-found.png`} alt="page-not-found" height=${150} />
            <div class="flex flex-col gap-5 items-center">
                <div class="font-24 medium">This page is not available</div>
                <div class="font-18">Kindly check the URL you entered</div>
            </div>
        </div>
    `;
};
