import { Button } from "../components/index.js";
import { MEDIA_URL } from "../constants/constant.js";
import { DASHBOARD_ROUTE } from "../constants/routesConstant.js";

export const PageNotFound = () => {
  return /*html*/ `
        <div class="inter w-100 h-full flex flex-col gap-6 items-center justify-center">
            <img src=${`${MEDIA_URL}/static/not-found.png`} alt="page-not-found" height=${180} />
            <div class="flex flex-col items-center font-20">
                <div>Uh-oh! It seems you've stumbled upon a lost page.</div>
                <div>Let's help you find your way.</div>
            </div>
            ${Button({
              variant: "contained",
              btnText: "Click Here!",
              href: DASHBOARD_ROUTE,
              className: "font-16",
            })}
        </div>
    `;
};
