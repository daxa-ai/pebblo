import {
  CLIENT_VERSION,
  MEDIA_URL,
  SERVER_VERSION,
} from "../constants/constant.js";

export function Header() {
  return /*html*/ ` 
  <div id="header" class="flex items-center relative pt-4 pb-4 pl-6 pr-6">
    <img class="cursor-pointer" src="${MEDIA_URL}/static/pebblo-icon.png" alt="Pebblo Icon" />
    <div class="mask absolute top-0 h-59 w-full left-0 -z-1"></div>
    <div class="surface-white font-12 inter flex gap-2 ml-auto">
      ${
        SERVER_VERSION
          ? `<div>Server ${SERVER_VERSION}</div><div class="divider bg-main"></div>`
          : ""
      }  
      ${CLIENT_VERSION ? `<div>Client ${CLIENT_VERSION}</div>` : ""}
    </div>
  </div>`;
}
