import {
  DOCUMENTATION_URL,
  MEDIA_URL,
  PEBBLO_TABS,
  SERVER_VERSION,
} from "../constants/constant.js";
import {
  DASHBOARD_ROUTE,
  SAFE_RETRIEVAL_ROUTE,
} from "../constants/routesConstant.js";
import { HelpIcon } from "../icons/index.js";
import { Navbar } from "./index.js";

export function Header() {
  const selectedTab = window.location.pathname?.includes(SAFE_RETRIEVAL_ROUTE)
    ? SAFE_RETRIEVAL_ROUTE
    : DASHBOARD_ROUTE;
  return /*html*/ ` 
  <div id="header" class="flex items-center relative pt-4 pb-4 pl-6 pr-6">
    <img class="cursor-pointer" src="${MEDIA_URL}/static/pebblo-icon.png" alt="Pebblo Icon" />
    <div class="pebblo-tabs ml-7">
      ${Navbar({ navItems: PEBBLO_TABS, selectedTab })}
    </div>
    <div class="mask absolute top-0 h-59 w-full left-0 -z-1"></div>
    <div class="surface-white font-12 inter flex gap-2 ml-auto">
      ${
        SERVER_VERSION
          ? `<div>Server Version ${SERVER_VERSION}</div><div class="divider bg-main"></div>`
          : ""
      }
      <a href="${DOCUMENTATION_URL}/safe_loader" target="_blank" class="cursor-pointer" >${HelpIcon(
    {
      color: "white",
      size: "sm",
    }
  )}</a>
    </div>
  </div>`;
}
