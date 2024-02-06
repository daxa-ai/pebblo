import { Table } from "./index.js";

const MEDIA_URL = document.scripts[0].getAttribute("staticURL");

export function Application_Details_List_Section(title, tableCol, tableData) {
  return `
    <div class="application-container flex flex-col gap-4">
      <div class="flex justify-between">
        <div class="inter surface-10 font-16 medium">${title}</div>
          <div class="search">
            <input type="text" />
            <img
              src="${MEDIA_URL}/static/search-icon.png"
              alt="Search Icon" />
          </div>
      </div>
      ${Table(tableCol, tableData)}
    </div>
    `;
}
